@echo off
echo Running all ingestions...
docker compose run --rm backend uv run python backend/db/ingestion/ingest_seeker.py --test-data
docker compose run --rm backend uv run python backend/db/ingestion/ingest_employer.py --test-data
docker compose run --rm backend uv run python backend/db/ingestion/ingest_mongo_seeker.py
docker compose run --rm backend uv run python backend/db/ingestion/ingest_mongo_employer.py
echo Done! Checking ChromaDB...
docker compose run --rm backend uv run python backend/db/ingestion/check_chroma_data.py
echo Complete.
@REM docker compose down -v --remove-orphans
pause