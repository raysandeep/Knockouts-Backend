from motor.motor_asyncio import AsyncIOMotorClient
import logging
# import import_env_file
from pymongo.errors import AutoReconnect
from core import settings

class MonogDB:
    client: AsyncIOMotorClient = True


db = MonogDB()

async def get_nosql_db() -> AsyncIOMotorClient:
    return db.client


async def get_mongo_connection():
    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL), 
        maxPoolSize=int(settings.MAX_POOL_SIZE),
        minPoolSize=int(settings.MIN_POOL_SIZE),
    )
    logging.info("Connected to Mongo Client")


async def close_mongo_connection():
    db.client.close()
    logging.info("Closed Mongo Client")