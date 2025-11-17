#!/usr/bin/env python3
"""List ChromaDB collections.

Usage:
    # From project root
    python backend/utils/list_chroma_collections.py
    
    # Using uv
    uv run python backend/utils/list_chroma_collections.py
    
    # From Docker
    docker compose exec backend uv run python backend/utils/list_chroma_collections.py
"""

import chromadb
import os
from pathlib import Path

# Get the project root directory (go up 3 levels from this file)
project_root = Path(__file__).parent.parent.parent

# Connect to ChromaDB
# Use environment variable if set, otherwise use default path relative to project root
chroma_path = os.getenv("CHROMA_PC_PATH")
if chroma_path is None:
    chroma_path = str(project_root / "chroma_db")

print(f"Connecting to ChromaDB at: {chroma_path}")
print("=" * 60)

try:
    client = chromadb.PersistentClient(path=chroma_path)
    
    # List all collections
    collections = client.list_collections()
    
    if not collections:
        print("No collections found in ChromaDB.")
    else:
        print(f"\nFound {len(collections)} collection(s):\n")
        for col in collections:
            print(f"  📦 {col.name}")
            # Get count
            count = col.count()
            print(f"     Documents: {count}")
            print()
    
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error connecting to ChromaDB: {e}")
    print("\nMake sure:")
    print("  1. ChromaDB is initialized")
    print("  2. The path is correct")
    print("  3. You have proper permissions")

