# ChromaDB ingestion
docker compose run backend uv run python backend/db/ingestion/ingest_seeker.py --test-data
docker compose run backend uv run python backend/db/ingestion/ingest_employer.py --test-data

# MongoDB ingestion
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_seeker.py
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_employer.py