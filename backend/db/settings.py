"""
Database Settings and Connection Module

This module handles MongoDB connection configuration using environment variables
and provides connection initialization and verification functionality.
"""

import os
from typing import Any

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from backend.schemas.seeker import Seeker
from backend.schemas.employer import Employer


# Load environment variables from .env file
load_dotenv()


class MongoDBSettings:
    """
    MongoDB connection settings from environment variables.

    Attributes:
        MONGO_DB_USER: MongoDB username
        MONGO_DB_PASSWORD: MongoDB password
        MONGO_DB_URL: MongoDB connection URL
        MONGO_DB_NAME: Database name
        MONGO_SEEKER_NAME: Seeker collection name
        MONGO_EMPLOYER_NAME: Employer collection name
    """

    def __init__(self):
        """Initialize MongoDB settings from environment variables."""
        self.MONGO_DB_USER = os.getenv("MONGO_DB_USER")
        self.MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
        self.MONGO_DB_URL = os.getenv("MONGO_DB_URL")
        self.MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "job-portal").strip("'\"")
        self.MONGO_SEEKER_NAME = os.getenv("MONGO_SEEKER_NAME", "seeker").strip("'\"")
        self.MONGO_EMPLOYER_NAME = os.getenv("MONGO_EMPLOYER_NAME", "employer").strip("'\"")

        # Validate required environment variables
        self._validate_settings()

    def _validate_settings(self):
        """Validate that all required settings are present."""
        required_vars = {
            "MONGO_DB_USER": self.MONGO_DB_USER,
            "MONGO_DB_PASSWORD": self.MONGO_DB_PASSWORD,
            "MONGO_DB_URL": self.MONGO_DB_URL,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please ensure your .env file is properly configured."
            )

    def get_connection_string(self) -> str:
        """
        Get the formatted MongoDB connection string.

        Returns:
            Formatted connection string with credentials

        Example:
            mongodb+srv://username:password@cluster.mongodb.net/?appName=job-portal
        """
        # Replace placeholders in URL with actual credentials
        connection_string = self.MONGO_DB_URL
        if "${MONGO_DB_USER}" in connection_string:
            connection_string = connection_string.replace("${MONGO_DB_USER}", self.MONGO_DB_USER)
        if "${MONGO_DB_PASSWORD}" in connection_string:
            connection_string = connection_string.replace("${MONGO_DB_PASSWORD}", self.MONGO_DB_PASSWORD)

        return connection_string

    def __repr__(self) -> str:
        """String representation (hiding password)."""
        return (
            f"MongoDBSettings("
            f"user='{self.MONGO_DB_USER}', "
            f"db='{self.MONGO_DB_NAME}', "
            f"url='***hidden***')"
        )


# Global settings instance
settings = MongoDBSettings()


# Global MongoDB client
mongodb_client: AsyncIOMotorClient | None = None


async def connect_to_mongodb() -> AsyncIOMotorClient:
    """
    Establish connection to MongoDB and initialize Beanie ODM.

    Returns:
        AsyncIOMotorClient instance

    Raises:
        Exception: If connection fails
    """
    global mongodb_client

    try:
        print("🔌 Connecting to MongoDB...")
        print(f"   Database: {settings.MONGO_DB_NAME}")
        print(f"   User: {settings.MONGO_DB_USER}")

        # Create MongoDB client
        connection_string = settings.get_connection_string()
        mongodb_client = AsyncIOMotorClient(connection_string)

        # Get database
        database = mongodb_client[settings.MONGO_DB_NAME]

        # Initialize Beanie with document models
        await init_beanie(
            database=database,
            document_models=[Seeker, Employer]
        )

        # Verify connection by pinging the server
        await mongodb_client.admin.command('ping')

        print("✅ MongoDB connection established successfully!")
        print(f"   Collections: {settings.MONGO_SEEKER_NAME}, {settings.MONGO_EMPLOYER_NAME}")

        return mongodb_client

    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_mongodb_connection():
    """Close the MongoDB connection."""
    global mongodb_client

    if mongodb_client:
        try:
            mongodb_client.close()
            print("🔌 MongoDB connection closed")
        except Exception as e:
            print(f"⚠️  Error closing MongoDB connection: {e}")


async def verify_mongodb_connection() -> dict[str, Any]:
    """
    Verify MongoDB connection and return connection status.

    Returns:
        Dictionary with connection status and database info
    """
    try:
        if not mongodb_client:
            return {
                "connected": False,
                "error": "No active connection"
            }

        # Ping the database
        await mongodb_client.admin.command('ping')

        # Get database info
        db = mongodb_client[settings.MONGO_DB_NAME]
        collections = await db.list_collection_names()

        return {
            "connected": True,
            "database": settings.MONGO_DB_NAME,
            "user": settings.MONGO_DB_USER,
            "collections": collections,
            "seeker_collection": settings.MONGO_SEEKER_NAME,
            "employer_collection": settings.MONGO_EMPLOYER_NAME,
        }

    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }


# Example usage and testing
if __name__ == "__main__":
    import asyncio

    async def test_connection():
        """Test the MongoDB connection."""
        print("=== MongoDB Connection Test ===\n")

        # Display settings (without sensitive data)
        print(f"Settings: {settings}\n")

        # Connect to MongoDB
        try:
            await connect_to_mongodb()

            # Verify connection
            status = await verify_mongodb_connection()
            print("\n=== Connection Status ===")
            print(f"Connected: {status['connected']}")
            if status['connected']:
                print(f"Database: {status['database']}")
                print(f"Collections: {status['collections']}")
                print(f"Seeker Collection: {status['seeker_collection']}")
                print(f"Employer Collection: {status['employer_collection']}")
            else:
                print(f"Error: {status['error']}")

            # Close connection
            await close_mongodb_connection()

        except Exception as e:
            print(f"\n❌ Connection test failed: {e}")

    # Run the test
    asyncio.run(test_connection())

