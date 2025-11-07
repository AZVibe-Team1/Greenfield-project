"""
FastAPI Application Entry Point
This is a minimal FastAPI setup for the Job Portal backend.
More routes and functionality will be added later.
"""
from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="Job Portal API",
    description="Backend API for Job Portal application",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {"message": "Job Portal API is running", "status": "ok"}


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
