"""
FastAPI Application Entry Point
This is a minimal FastAPI setup for the Job Portal backend.
More routes and functionality will be added later.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

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
        print("✅ Application startup complete")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        raise

    yield

    # Shutdown: Close MongoDB connection
    await close_mongodb_connection()
    print("👋 Application shutdown complete")


# Create FastAPI application instance
app = FastAPI(
    title="Job Portal API",
    description="Backend API for Job Portal application",
    version="0.1.0",
    lifespan=lifespan
)


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
