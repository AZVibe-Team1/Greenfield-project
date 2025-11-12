"""
FastAPI Application Entry Point
This is the main FastAPI application for the Job Portal backend.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.routes import auth_router, employer_router, seeker_router
from backend.db.settings import (
    close_mongodb_connection,
    connect_to_mongodb,
    settings,
    verify_mongodb_connection,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events for MongoDB connection.
    """
    # Startup: Connect to MongoDB
    try:
        await connect_to_mongodb()
    except Exception:
        raise

    yield

    # Shutdown: Close MongoDB connection
    await close_mongodb_connection()


# Create FastAPI application instance
app = FastAPI(
    title="Job Portal API",
    description="Backend API for Job Portal application",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://frontend:3000",   # Docker frontend service
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(seeker_router.router, prefix="/api/v1")
app.include_router(employer_router.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "Job Portal API is running",
        "status": "ok",
        "database": settings.MONGO_DB_NAME
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy"}


@app.get("/db-status")
async def database_status():
    """Database connection status endpoint"""
    return await verify_mongodb_connection()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
