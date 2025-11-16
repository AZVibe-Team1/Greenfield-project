# ChromaDB ingestion
docker compose run backend uv run python backend/db/ingestion/ingest_seeker.py --test-data
docker compose run backend uv run python backend/db/ingestion/ingest_employer.py --test-data

# MongoDB ingestion
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_seeker.py
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_employer.py

# Ingest all (from root project dir)
./ingest_all.bat (Windows)
./ingest_all.sh (macOS/Linux)