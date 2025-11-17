@echo off
REM Sync both ChromaDB seekers to MongoDB and MongoDB employers to ChromaDB
REM This script copies both sync scripts to the backend container and runs them

echo ========================================
echo Starting Seeker Sync (ChromaDB -^> MongoDB)
echo ========================================
echo.

echo Copying sync_chroma_mongo_seekers.py to backend container...
docker compose cp ./scripts/sync_chroma_mongo_seekers.py backend:/app/sync_chroma_mongo_seekers.py

if %ERRORLEVEL% NEQ 0 (
    echo Failed to copy seeker sync script to container
    exit /b 1
)

echo Running seeker sync script in backend container...
docker compose exec -w /app backend uv run ./sync_chroma_mongo_seekers.py

if %ERRORLEVEL% NEQ 0 (
    echo Seeker sync script execution failed
    exit /b 1
)

echo.
echo ========================================
echo Seeker Sync Complete!
echo ========================================
echo.
echo ========================================
echo Starting Employer Sync (MongoDB -^> ChromaDB)
echo ========================================
echo.

echo Copying sync_chroma_mongo_employers.py to backend container...
docker compose cp ./scripts/sync_chroma_mongo_employers.py backend:/app/sync_chroma_mongo_employers.py

if %ERRORLEVEL% NEQ 0 (
    echo Failed to copy employer sync script to container
    exit /b 1
)

echo Running employer sync script in backend container...
docker compose exec -w /app backend uv run ./sync_chroma_mongo_employers.py

if %ERRORLEVEL% NEQ 0 (
    echo Employer sync script execution failed
    exit /b 1
)

echo.
echo ========================================
echo All Syncs Complete!
echo ========================================

