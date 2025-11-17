#!/usr/bin/env bash
# Works on macOS (bash/zsh) and Linux

echo "Running all ingestions..."
docker compose run backend uv run python backend/db/ingestion/ingest_seeker.py --test-data
docker compose run backend uv run python backend/db/ingestion/ingest_employer.py --test-data
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_seeker.py
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_employer.py
echo "Done! Checking ChromaDB..."
docker compose run backend uv run python backend/db/ingestion/check_chroma_data.py
echo "Done. Cleaning up containers..."
docker compose down -v --remove-orphans