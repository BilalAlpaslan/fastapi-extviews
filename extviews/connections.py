
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


__all__ = ['PymongoConnection', 'MotorConnection']

class PymongoConnection:

    def __init__(self) -> None:
        self.db_client: AsyncIOMotorClient = None

    def get_db_client(self) -> MongoClient:
        """Return database client instance."""
        if self.db_client is None:
            self.connect_db()
        return self.db_client

    def connect_db(self, host="127.0.0.1", port="27017", db="default", user=None, password=None):
        """Create database connection."""
        if user and password:
            self.db_client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
        else:
            self.db_client = MongoClient(f"mongodb://{host}:{port}")
        self.db_name = db
    
    def get_db(self):
        """Return database instance."""
        return self.get_db_client()[self.db_name]

    def close_db(self):
        """Close database connection."""
        self.db_client.close()


class MotorConnection:
    
    
    # !: not implemented yet
    
    db_client:AsyncIOMotorClient = None

    @classmethod
    async def get_db_client(cls) -> AsyncIOMotorClient:
        """Return database client instance."""
        return cls.db_client

    @classmethod
    async def connect_db(cls, host="127.0.0.1", port="27017", db="default", user=None, password=None):
        """Create database connection."""
        if user and password:
            cls.client = AsyncIOMotorClient(f"mongodb://{user}:{password}@{host}:{port}")
        else:
            cls.db_client = AsyncIOMotorClient(f"mongodb://{host}:{port}")

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        cls.db_client.close()