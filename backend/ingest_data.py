"""
ChromaDB Data Ingestion Script

This script ingests text documents from the chroma_data folder into a locally
persisted ChromaDB vector store. The vector store is used for RAG (Retrieval
Augmented Generation) to provide context-aware responses in the job portal.

Uses OpenAI's text-embedding-3-small model for generating embeddings.
Requires OPENAI_API_KEY to be set in the environment.

Usage:
    python backend/ingest_data.py
    or
    docker compose run backend python backend/ingest_data.py
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

# Add backend directory to Python path for imports
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


def load_environment():
    """Load environment variables from .env file."""
    # Look for .env file in project root (parent of backend/)
    env_path = backend_dir.parent / ".env"
    
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Loaded environment variables from {env_path}")
    else:
        print(f"⚠ Warning: .env file not found at {env_path}")
        print("  Using default values or existing environment variables")


def get_chroma_path() -> Path:
    """Get the ChromaDB persistence path from environment variable."""
    chroma_path_str = os.getenv("CHROMA_PC_PATH", "./chroma_db")
    
    # If running in Docker, the path might be relative to /app
    # If path is relative, make it relative to project root
    chroma_path = Path(chroma_path_str)
    
    if not chroma_path.is_absolute():
        # Make it relative to project root (parent of backend/)
        chroma_path = backend_dir.parent / chroma_path_str
    
    return chroma_path


def load_documents(data_dir: Path) -> List[Dict[str, str]]:
    """
    Load all text documents from the specified directory.
    
    Args:
        data_dir: Path to directory containing text files
        
    Returns:
        List of documents with content and metadata
    """
    print(f"\n📂 Loading documents from: {data_dir}")
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    documents = []
    txt_files = list(data_dir.glob("**/*.txt"))
    
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {data_dir}")
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():  # Only add non-empty files
                    documents.append({
                        "content": content,
                        "source": str(file_path),
                        "filename": file_path.name
                    })
                    print(f"  - {file_path.name}")
        except Exception as e:
            print(f"  ⚠ Warning: Failed to load {file_path.name}: {e}")
    
    print(f"✓ Loaded {len(documents)} documents")
    return documents


def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap.
    
    Args:
        text: Text to split
        chunk_size: Maximum characters per chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Find the end of this chunk
        end = start + chunk_size
        
        # If this isn't the last chunk, try to break at a sentence or paragraph
        if end < len(text):
            # Look for paragraph break
            paragraph_break = text.rfind('\n\n', start, end)
            if paragraph_break != -1 and paragraph_break > start:
                end = paragraph_break
            else:
                # Look for sentence break
                sentence_break = text.rfind('. ', start, end)
                if sentence_break != -1 and sentence_break > start:
                    end = sentence_break + 1
                else:
                    # Look for any newline
                    newline = text.rfind('\n', start, end)
                    if newline != -1 and newline > start:
                        end = newline
        
        chunks.append(text[start:end].strip())
        
        # Move start forward, accounting for overlap
        start = end - chunk_overlap if end < len(text) else end
        
        # Make sure we're making progress
        if start <= chunks[-1][:chunk_overlap].find(text[start:start+10]):
            start = end
    
    return chunks


def split_documents(documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Split documents into smaller chunks for better retrieval.
    
    Args:
        documents: List of documents to split
        
    Returns:
        List of document chunks with metadata
    """
    print("\n✂️  Splitting documents into chunks...")
    
    chunks = []
    for doc in documents:
        text_chunks = split_text(doc["content"])
        
        for i, chunk in enumerate(text_chunks):
            chunks.append({
                "content": chunk,
                "source": doc["source"],
                "filename": doc["filename"],
                "chunk_index": i
            })
    
    print(f"✓ Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks


class OpenAIEmbeddings:
    """Wrapper for OpenAI embeddings to provide a consistent interface."""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.dimension = 1536  # text-embedding-3-small dimension
    
    def encode(self, texts: List[str], show_progress_bar: bool = False) -> List[List[float]]:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of texts to embed
            show_progress_bar: Whether to show progress (ignored for OpenAI)
            
        Returns:
            List of embeddings
        """
        if show_progress_bar:
            print(f"  Calling OpenAI API for {len(texts)} embeddings...")
        
        # OpenAI has a limit on batch size, so we'll batch the requests
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            
            if show_progress_bar:
                print(f"    Progress: {min(i + batch_size, len(texts))}/{len(texts)}")
        
        return all_embeddings


def create_embeddings_function():
    """
    Create embeddings function for vectorization.
    Uses OpenAI's text-embedding-3-small model.
    
    Returns:
        OpenAIEmbeddings wrapper
    """
    print("\n🤖 Initializing OpenAI embeddings (text-embedding-3-small)...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    
    model = OpenAIEmbeddings(api_key=api_key)
    print("✓ OpenAI embeddings initialized")
    return model


def create_vectorstore(chunks: List[Dict[str, str]], embedding_model, persist_directory: Path):
    """
    Create and persist ChromaDB vector store.
    
    Args:
        chunks: List of document chunks
        embedding_model: SentenceTransformer model
        persist_directory: Path where ChromaDB will persist data
    """
    print(f"\n💾 Creating vector store at: {persist_directory}")
    
    # Create persist directory if it doesn't exist
    persist_directory.mkdir(parents=True, exist_ok=True)
    
    # Initialize ChromaDB client with persistence
    client = chromadb.PersistentClient(
        path=str(persist_directory),
        settings=Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
    )
    
    # Delete existing collection if it exists
    try:
        client.delete_collection(name="job_portal_knowledge")
        print("  ℹ Deleted existing collection")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name="job_portal_knowledge",
        metadata={"description": "Job portal knowledge base for RAG"}
    )
    
    # Prepare data for batch insertion
    print(f"  Generating embeddings for {len(chunks)} chunks...")
    texts = [chunk["content"] for chunk in chunks]
    embeddings = embedding_model.encode(texts, show_progress_bar=True)
    
    # Create unique IDs and metadata
    ids = [f"doc_{i}" for i in range(len(chunks))]
    metadatas = [{
        "source": chunk["source"],
        "filename": chunk["filename"],
        "chunk_index": chunk["chunk_index"]
    } for chunk in chunks]
    
    # Add to collection in batches
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        end_idx = min(i + batch_size, len(chunks))
        collection.add(
            ids=ids[i:end_idx],
            embeddings=embeddings[i:end_idx],
            documents=texts[i:end_idx],
            metadatas=metadatas[i:end_idx]
        )
    
    print(f"✓ Vector store created with {len(chunks)} chunks")
    print(f"✓ Data persisted to: {persist_directory}")
    
    return collection


def verify_vectorstore(persist_directory: Path, embedding_model):
    """
    Verify the vector store was created successfully by performing a test query.
    
    Args:
        persist_directory: Path to persisted ChromaDB
        embedding_model: OpenAIEmbeddings model
    """
    print("\n🔍 Verifying vector store...")
    
    try:
        # Load the persisted vector store with same settings as creation
        client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        collection = client.get_collection(name="job_portal_knowledge")
        
        # Get collection stats
        count = collection.count()
        print(f"✓ Vector store loaded successfully")
        print(f"✓ Collection contains {count} documents")
        
        # Perform a test similarity search
        test_query = "What are the requirements for a software engineer?"
        query_embedding = embedding_model.encode([test_query])[0]
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        if results['documents']:
            print(f"✓ Test query returned {len(results['documents'][0])} results")
            print(f"\n📄 Sample result (first 200 chars):")
            print(f"  {results['documents'][0][0][:200]}...")
        
        return True
    except Exception as e:
        print(f"✗ Error verifying vector store: {e}")
        return False


def main():
    """Main ingestion workflow."""
    print("=" * 80)
    print("ChromaDB Data Ingestion Script")
    print("=" * 80)
    
    try:
        # Step 1: Load environment variables
        load_environment()
        
        # Step 2: Get paths
        data_dir = backend_dir / "chroma_data"
        chroma_path = get_chroma_path()
        
        print(f"\n📍 Paths:")
        print(f"  Data directory: {data_dir}")
        print(f"  ChromaDB path: {chroma_path}")
        
        # Step 3: Load documents
        documents = load_documents(data_dir)
        
        if not documents:
            print("\n⚠ No documents found. Please add .txt files to the chroma_data directory.")
            return
        
        # Step 4: Split documents into chunks
        chunks = split_documents(documents)
        
        # Step 5: Create embeddings model
        embedding_model = create_embeddings_function()
        
        # Step 6: Create and persist vector store
        collection = create_vectorstore(chunks, embedding_model, chroma_path)
        
        # Step 7: Verify the vector store
        verify_vectorstore(chroma_path, embedding_model)
        
        print("\n" + "=" * 80)
        print("✅ Data ingestion completed successfully!")
        print("=" * 80)
        print(f"\n💡 The vector store is ready to use at: {chroma_path}")
        print("   You can now use this for RAG queries in your application.")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
