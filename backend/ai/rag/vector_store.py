"""
Vector Store Module

This module provides an interface to ChromaDB for vector similarity search
operations used in AI-powered job matching.
"""

from typing import Any

from loguru import logger

from backend.db.settings import (
    Employer_JobDescr_collection,
    Seeker_Resume_collection,
)


class VectorStore:
    """
    Interface to ChromaDB for vector operations.
    
    Provides methods for retrieving embeddings and performing
    similarity searches for job seekers and employers.
    """
    
    def __init__(self):
        """Initialize vector store with ChromaDB collections."""
        self.seeker_collection = Seeker_Resume_collection
        self.job_collection = Employer_JobDescr_collection
    
    def get_seeker_by_id(self, seeker_id: str) -> dict[str, Any] | None:
        """
        Retrieve seeker embedding and metadata from ChromaDB.
        
        Args:
            seeker_id: Seeker's MongoDB ObjectId as string
        
        Returns:
            Dictionary with embedding and metadata, or None if not found
        """
        try:
            result = self.seeker_collection.get(
                ids=[seeker_id],
                include=["embeddings", "metadatas", "documents"]
            )
            
            if not result or not result["ids"]:
                logger.warning(f"Seeker not found in ChromaDB: {seeker_id}")
                return None
            
            return {
                "id": result["ids"][0],
                "embedding": result["embeddings"][0] if result.get("embeddings") else None,
                "metadata": result["metadatas"][0] if result.get("metadatas") else {},
                "document": result["documents"][0] if result.get("documents") else None
            }
        
        except Exception as e:
            logger.error(f"Error retrieving seeker from ChromaDB: {e}")
            return None
    
    def get_job_by_id(self, job_id: str) -> dict[str, Any] | None:
        """
        Retrieve job embedding and metadata from ChromaDB.
        
        Args:
            job_id: Job's MongoDB ObjectId as string
        
        Returns:
            Dictionary with embedding and metadata, or None if not found
        """
        try:
            result = self.job_collection.get(
                ids=[job_id],
                include=["embeddings", "metadatas", "documents"]
            )
            
            if not result or not result["ids"]:
                logger.warning(f"Job not found in ChromaDB: {job_id}")
                return None
            
            return {
                "id": result["ids"][0],
                "embedding": result["embeddings"][0] if result.get("embeddings") else None,
                "metadata": result["metadatas"][0] if result.get("metadatas") else {},
                "document": result["documents"][0] if result.get("documents") else None
            }
        
        except Exception as e:
            logger.error(f"Error retrieving job from ChromaDB: {e}")
            return None
    
    def search_similar_jobs(
        self,
        query_embedding: list[float],
        n_results: int = 20
    ) -> dict[str, Any]:
        """
        Search for jobs similar to the given embedding.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
        
        Returns:
            Dictionary with search results (ids, distances, metadatas)
        """
        try:
            results = self.job_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["distances", "metadatas", "documents"]
            )
            
            logger.debug(f"Found {len(results['ids'][0]) if results['ids'] else 0} similar jobs")
            return results
        
        except Exception as e:
            logger.error(f"Error searching similar jobs: {e}")
            return {"ids": [], "distances": [], "metadatas": [], "documents": []}
    
    def search_similar_seekers(
        self,
        query_embedding: list[float],
        n_results: int = 20
    ) -> dict[str, Any]:
        """
        Search for seekers similar to the given embedding.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
        
        Returns:
            Dictionary with search results (ids, distances, metadatas)
        """
        try:
            results = self.seeker_collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["distances", "metadatas", "documents"]
            )
            
            logger.debug(f"Found {len(results['ids'][0]) if results['ids'] else 0} similar seekers")
            return results
        
        except Exception as e:
            logger.error(f"Error searching similar seekers: {e}")
            return {"ids": [], "distances": [], "metadatas": [], "documents": []}


# Global vector store instance
_vector_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    """Get or create the global vector store instance."""
    global _vector_store  # noqa: PLW0603
    
    if _vector_store is None:
        _vector_store = VectorStore()
    
    return _vector_store

