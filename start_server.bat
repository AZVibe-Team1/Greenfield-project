@echo off
cd backend
uv run uvicorn main:app --reload --port 8000

