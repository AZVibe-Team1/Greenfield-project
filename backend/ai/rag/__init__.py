"""
RAG (Retrieval Augmented Generation) Module

This module provides vector store and retrieval functionality
for AI-powered matching in the job portal.
"""

from backend.ai.rag.vector_store import VectorStore, get_vector_store

__all__ = ["VectorStore", "get_vector_store"]

