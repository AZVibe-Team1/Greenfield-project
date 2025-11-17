#!/bin/bash
# Sync both ChromaDB seekers to MongoDB and MongoDB employers to ChromaDB
# This script copies both sync scripts to the backend container and runs them

set -e

echo "========================================"
echo "Starting Seeker Sync (ChromaDB -> MongoDB)"
echo "========================================"
echo

echo "Copying sync_chroma_mongo_seekers.py to backend container..."
docker compose cp ./scripts/sync_chroma_mongo_seekers.py backend:/app/sync_chroma_mongo_seekers.py

echo "Running seeker sync script in backend container..."
docker compose exec -w /app backend uv run ./sync_chroma_mongo_seekers.py

echo
echo "========================================"
echo "Seeker Sync Complete!"
echo "========================================"
echo
echo "========================================"
echo "Starting Employer Sync (MongoDB -> ChromaDB)"
echo "========================================"
echo

echo "Copying sync_chroma_mongo_employers.py to backend container..."
docker compose cp ./scripts/sync_chroma_mongo_employers.py backend:/app/sync_chroma_mongo_employers.py

echo "Running employer sync script in backend container..."
docker compose exec -w /app backend uv run ./sync_chroma_mongo_employers.py

echo
echo "========================================"
echo "All Syncs Complete!"
echo "========================================"

