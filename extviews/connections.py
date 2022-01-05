
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


__all__ = ['PymongoConnection', 'MotorConnection']

class PymongoConnection:
    def __init__(self, host="127.0.0.1", port="27017", db="default", user=None, password=None):
        """Create database connection."""
        if user and password:
            self.db_client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
        else:
            self.db_client = MongoClient(f"mongodb://{host}:{port}")
        self.db_name = db

    def get_db_client(self) -> MongoClient:
        """Return database client instance."""
        return self.db_client

    def get_db(self):
        """Return database instance."""
        return self.get_db_client()[self.db_name]

    def close_db(self):
        """Close database connection."""
        self.db_client.close()


class MotorConnection:
    def __init__(self, host="127.0.0.1", port="27017", db="default", user=None, password=None):
        """Create database connection."""
        if user and password:
            self.db_client = AsyncIOMotorClient(f"mongodb://{user}:{password}@{host}:{port}")
        else:
            self.db_client = AsyncIOMotorClient(f"mongodb://{host}:{port}")
        self.db_name = db

    def get_db_client(self) -> AsyncIOMotorClient:
        """Return database client instance."""
        return self.db_client
    
    def get_db(self):
        """Return database instance."""
        return self.get_db_client()[self.db_name]
    
    def close_db(self):
        """Close database connection."""
        self.db_client.close()