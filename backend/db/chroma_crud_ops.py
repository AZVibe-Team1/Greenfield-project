"""
ChromaDB CRUD Operations Module

This module provides CRUD operations for ChromaDB collections including
add, update, delete, and query operations.
"""

from typing import Any

from chromadb import Collection
from loguru import logger


def write_collection(
    collection: Collection,
    collection_name: str,
    id_value: str,
    text_value: str,
    metadata: dict[str, Any] | None = None
) -> int:
    """
    Add a document to a ChromaDB collection.

    Args:
        collection: ChromaDB collection object
        collection_name: Name of the collection (for logging)
        id_value: Unique identifier for the document
        text_value: Text content to be added
        metadata: Optional metadata dictionary

    Returns:
        1 if successful, -1 if failed

    Example:
        >>> result = write_collection(
        ...     collection=my_collection,
        ...     collection_name="Seeker_Resume",
        ...     id_value="seeker_123",
        ...     text_value="Resume content here",
        ...     metadata={"updated": "2024-01-01"}
        ... )
    """
    try:
        if metadata:
            collection.add(
                ids=[id_value],
                documents=[text_value],
                metadatas=[metadata]
            )
            logger.debug(
                f"Successful Chroma add, with Collection name of {collection_name} and ID of {id_value}"
            )
            return 1

        collection.add(
            ids=[id_value],
            documents=[text_value]
        )
        logger.debug(
            f"Successful Chroma add, with Collection name of {collection_name} and ID of {id_value}"
        )
        return 1

    except Exception as e:
        logger.critical(
            f"Add FAILED to ChromaDB for collection {collection_name} and ID of {id_value}: {e}"
        )
        return -1


def update_collection(
    collection: Collection,
    collection_name: str,
    id_value: str,
    text_value: str,
    metadata: dict[str, Any] | None = None
) -> int:
    """
    Update a document in a ChromaDB collection.

    Args:
        collection: ChromaDB collection object
        collection_name: Name of the collection (for logging)
        id_value: Unique identifier for the document
        text_value: Updated text content
        metadata: Optional metadata dictionary

    Returns:
        1 if successful, -1 if failed

    Example:
        >>> result = update_collection(
        ...     collection=my_collection,
        ...     collection_name="Seeker_Resume",
        ...     id_value="seeker_123",
        ...     text_value="Updated resume content",
        ...     metadata={"updated": "2024-01-02"}
        ... )
    """
    try:
        if metadata:
            collection.update(
                ids=[id_value],
                documents=[text_value],
                metadatas=[metadata]
            )
            logger.debug(
                f"Successful Chroma Update, with Collection name of {collection_name} and ID of {id_value}"
            )
            return 1

        collection.update(
            ids=[id_value],
            documents=[text_value]
        )
        logger.debug(
            f"Successful Chroma Update, with Collection name of {collection_name} and ID of {id_value}"
        )
        return 1

    except Exception as e:
        logger.critical(
            f"Update FAILED to ChromaDB for collection {collection_name} and ID of {id_value}: {e}"
        )
        return -1


def delete_collection(
    collection: Collection,
    collection_name: str,
    id_value: str
) -> int:
    """
    Delete a document from a ChromaDB collection.

    Args:
        collection: ChromaDB collection object
        collection_name: Name of the collection (for logging)
        id_value: Unique identifier for the document to delete

    Returns:
        1 if successful, -1 if failed

    Example:
        >>> result = delete_collection(
        ...     collection=my_collection,
        ...     collection_name="Seeker_Resume",
        ...     id_value="seeker_123"
        ... )
    """
    try:
        collection.delete(
            ids=[id_value]
        )

    except Exception as e:
        logger.critical(
            f"Delete FAILED to ChromaDB for collection {collection_name} and ID of {id_value}: {e}"
        )
        return -1
    else:
        logger.debug(
            f"Successful Chroma Delete, with Collection name of {collection_name} and ID of {id_value}"
        )
        return 1


def query_collection(
    collection: Collection,
    collection_name: str,
    query_text: str,
    num_results: int = 25
) -> Any:
    """
    Query a ChromaDB collection for similar documents.

    Args:
        collection: ChromaDB collection object
        collection_name: Name of the collection (for logging)
        query_text: Text to search for
        num_results: Number of results to return (default: 25)

    Returns:
        Dictionary containing query results with keys: ids, embeddings, documents,
        metadatas, distances, or -1 if failed

    Result Structure:
        {
            'ids': List[List[str]] - IDs of matching documents
            'embeddings': Optional[List[List[float]]] - Embeddings of matches
            'documents': Optional[List[List[str]]] - Document text content
            'metadatas': Optional[List[List[dict]]] - Metadata of matches
            'distances': Optional[List[List[float]]] - Distance scores
        }

    Note:
        Results are returned in columnar form, indexed by input query.
        results["ids"][0] contains IDs for the first input query.

    Example:
        >>> results = query_collection(
        ...     collection=my_collection,
        ...     collection_name="Seeker_Resume",
        ...     query_text="Python developer with 5 years experience",
        ...     num_results=10
        ... )
        >>> if results != -1:
        ...     matching_ids = results["ids"][0]
        ...     documents = results["documents"][0]
    """
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=num_results
        )

    except Exception as e:
        logger.critical(
            f"Query FAILED to ChromaDB for collection {collection_name} and query_text of {query_text}: {e}"
        )
        return -1
    else:
        logger.debug(
            f"Successful Chroma Query, with Collection name of {collection_name} and query_text of {query_text}"
        )
        return results

