#!/usr/bin/env python3
"""List ChromaDB collections."""

import chromadb
import os

# Connect to ChromaDB
chroma_path = os.getenv("CHROMA_PC_PATH", "./chroma_db")
client = chromadb.PersistentClient(path=chroma_path)

# List all collections
collections = client.list_collections()

print("ChromaDB Collections:")
for col in collections:
    print(f"  - {col.name}")
    # Get count
    count = col.count()
    print(f"    Count: {count}")

