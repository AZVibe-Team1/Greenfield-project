"""
Database Settings and Connection Module

This module handles MongoDB connection configuration using environment variables
and provides connection initialization and verification functionality.
"""

import os
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import chromadb
from beanie import init_beanie
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from backend.schemas.employer import Employer
from backend.schemas.seeker import Seeker


# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key for ChromaDB embedding function
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure loguru logging
logger.remove(0)
logger.add("Logs/Debug_log.log", level="DEBUG", format="{time} {level} {message}", rotation="50MB")
logger.add("Logs/Error_log.log", level="ERROR", format="{time} {level} {message}", rotation="50MB")

# Initialize ChromaDB client
# Validating that the db exists.  If not, it will be created, per ChromaDB documentation
try:
    client = chromadb.PersistentClient(path="./chroma_db")
    logger.debug("Persistent client initialized successfully")
except PermissionError:
    logger.critical("Error: Insufficient permissions to create database directory")
    raise
except Exception as e:
    logger.critical(f"Initialization failed: {e}")
    raise

# Get or create collections, using the OpenAI embedder "text-embedding-3"
try:
    Seeker_Resume_collection = client.get_or_create_collection(
    name="Seeker_Resume",
    embedding_function=OpenAIEmbeddingFunction(  # type: ignore[arg-type]
        model_name="text-embedding-3-small",
        api_key=OPENAI_API_KEY
    ),
    metadata={
        "description": "Contains Resume of Seeker",
        "created": str(datetime.now(ZoneInfo("America/Denver")))
    }
)
except Exception as e:
    logger.critical(f"Error getting or creating Seeker_Resume collection: {e}")
    raise

try:
    Seeker_Skill_collection = client.get_or_create_collection(
    name="Seeker_Skills",
    embedding_function=OpenAIEmbeddingFunction(  # type: ignore[arg-type]
        model_name="text-embedding-3-small",
        api_key=OPENAI_API_KEY
    ),
        metadata={
        "description": "Contains Skills of Seeker",
        "created": str(datetime.now(ZoneInfo("America/Denver")))
    }
)
except Exception as e:
    logger.critical(f"Error getting or creating Seeker_Skills collection: {e}")
    raise
try:
    Employer_JobDescr_collection = client.get_or_create_collection(
    name="Employer_JobDescr",
    embedding_function=OpenAIEmbeddingFunction(  # type: ignore[arg-type]
        model_name="text-embedding-3-small",
        api_key=OPENAI_API_KEY
    ),
        metadata={
        "description": "Contains Job Description of Employer",
        "created": str(datetime.now(ZoneInfo("America/Denver")))
    }
)
except Exception as e:
    logger.critical(f"Error getting or creating Employer_JobDescr collection: {e}")
    raise
try:
    Employer_Skillswish_collection = client.get_or_create_collection(
    name="Employer_Skillswish",
    embedding_function=OpenAIEmbeddingFunction(  # type: ignore[arg-type]
        model_name="text-embedding-3-small",
        api_key=OPENAI_API_KEY
    ),
    metadata={
        "description": "Contains Desired skills of Employer",
        "created": str(datetime.now(ZoneInfo("America/Denver")))
    }
)
except Exception as e:
    logger.critical(f"Error getting or creating Employer_Skillswish collection: {e}")
    raise

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
            error_message = (
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please ensure your .env file is properly configured."
            )
            logger.critical(error_message)
            raise ValueError(error_message)

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
        if not connection_string:
            error_msg = "MONGO_DB_URL is not set"
            logger.critical(error_msg)
            raise ValueError(error_msg)

        if "${MONGO_DB_USER}" in connection_string:
            if not self.MONGO_DB_USER:
                error_msg = "MONGO_DB_USER is not set"
                logger.critical(error_msg)
                raise ValueError(error_msg)
            connection_string = connection_string.replace("${MONGO_DB_USER}", self.MONGO_DB_USER)

        if "${MONGO_DB_PASSWORD}" in connection_string:
            if not self.MONGO_DB_PASSWORD:
                error_msg = "MONGO_DB_PASSWORD is not set"
                logger.critical(error_msg)
                raise ValueError(error_msg)
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


class _MongoDBClient:
    """Internal singleton to manage MongoDB client connection."""

    def __init__(self):
        self._client: AsyncIOMotorClient | None = None

    def set_client(self, client: AsyncIOMotorClient) -> None:
        """Set the MongoDB client."""
        self._client = client

    def get_client(self) -> AsyncIOMotorClient | None:
        """Get the MongoDB client."""
        return self._client

    def close_client(self) -> None:
        """Close the MongoDB client."""
        if self._client:
            self._client.close()
            self._client = None


# Module-level client manager
_client_manager = _MongoDBClient()


def get_mongodb_client() -> AsyncIOMotorClient | None:
    """Get the current MongoDB client instance."""
    return _client_manager.get_client()


async def connect_to_mongodb() -> AsyncIOMotorClient:
    """
    Establish connection to MongoDB and initialize Beanie ODM.

    Returns:
        AsyncIOMotorClient instance

    Raises:
        Exception: If connection fails
    """
    try:
        logger.debug("🔌 Connecting to MongoDB...")
        logger.debug(f"   Database: {settings.MONGO_DB_NAME}")
        logger.debug(f"   User: {settings.MONGO_DB_USER}")

        # Create MongoDB client
        connection_string = settings.get_connection_string()
        client = AsyncIOMotorClient(connection_string)

        # Get database
        database = client[settings.MONGO_DB_NAME]

        # Initialize Beanie with document models
        await init_beanie(
            database=database,  # type: ignore[arg-type]
            document_models=[Seeker, Employer]
        )

        # Verify connection by pinging the server
        await client.admin.command("ping")

        logger.debug("✅ MongoDB connection established successfully!")
        logger.debug(f"   Collections: {settings.MONGO_SEEKER_NAME}, {settings.MONGO_EMPLOYER_NAME}")

        # Store the client in the manager
        _client_manager.set_client(client)

    except Exception as e:
        logger.critical(f"❌ Failed to connect to MongoDB: {e}")
        raise
    else:
        return client


async def close_mongodb_connection():
    """Close the MongoDB connection."""
    client = _client_manager.get_client()
    if client:
        try:
            _client_manager.close_client()
            logger.debug("🔌 MongoDB connection closed")
        except Exception as e:
            logger.critical(f"⚠️  Error closing MongoDB connection: {e}")


async def verify_mongodb_connection() -> dict[str, Any]:
    """
    Verify MongoDB connection and return connection status.

    Returns:
        Dictionary with connection status and database info
    """
    try:
        client = _client_manager.get_client()
        if not client:
            return {
                "connected": False,
                "error": "No active connection"
            }

        # Ping the database
        await client.admin.command("ping")

        # Get database info
        db = client[settings.MONGO_DB_NAME]
        collections = await db.list_collection_names()

    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }
    else:
        return {
            "connected": True,
            "database": settings.MONGO_DB_NAME,
            "user": settings.MONGO_DB_USER,
            "collections": collections,
            "seeker_collection": settings.MONGO_SEEKER_NAME,
            "employer_collection": settings.MONGO_EMPLOYER_NAME,
        }


# Example usage and testing
if __name__ == "__main__":
    import asyncio

    async def test_connection():
        """Test the MongoDB connection."""
        logger.debug("=== MongoDB Connection Test ===\n")

        # Display settings (without sensitive data)
        logger.debug(f"Settings: {settings}\n")

        # Connect to MongoDB
        try:
            await connect_to_mongodb()

            # Verify connection
            status = await verify_mongodb_connection()
            logger.debug("\n=== Connection Status ===")
            logger.debug(f"Connected: {status['connected']}")
            if status["connected"]:
                logger.debug(f"Database: {status['database']}")
                logger.debug(f"Collections: {status['collections']}")
                logger.debug(f"Seeker Collection: {status['seeker_collection']}")
                logger.debug(f"Employer Collection: {status['employer_collection']}")
            else:
                logger.critical(f"Error: {status['error']}")

            # Close connection
            await close_mongodb_connection()

        except Exception as e:
            logger.critical(f"\n❌ Connection test failed: {e}")

    # Run the test
    asyncio.run(test_connection())

