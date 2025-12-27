import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load and validate environment variables
load_dotenv()

uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME", "shortener_db")

if not uri:
    raise ValueError("MONGO_URI environment variable is required")
if not db_name:
    raise ValueError("DB_NAME environment variable is required")

# Configuration for link ID generation
# Default to Machine ID 1 if not set in .env
machine_id_str = os.getenv("MACHINE_ID", "1")
try:
    MACHINE_ID = int(machine_id_str)
except ValueError:
    raise ValueError(f"MACHINE_ID must be an integer, got: {machine_id_str}")

# Shift of 20 bits allows ~1 million sequence numbers per machine before rolling over
# (Machine ID takes the upper bits, Sequence takes the lower 20 bits)
MACHINE_OFFSET = 20 

params = {
    "server_api": ServerApi('1')
}
# Only force SSL if connecting to Cloud (Atlas)
if "mongodb+srv" in uri:
    params["tlsCAFile"] = certifi.where()

client = AsyncIOMotorClient(uri, **params)

# Redis configuration
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(redis_url, decode_responses=True)

# Cache configuration
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # Default 1 hour
CACHE_KEY_PREFIX = "url:"

# Define Database and Collections
db = client[db_name]
url_collection = db["urls"]
counters_collection = db["counters"]

async def verify_connection():
    """Verify connection to MongoDB."""
    try:
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

async def verify_redis_connection():
    """Verify connection to Redis."""
    try:
        await redis_client.ping()
        print("✅ Successfully connected to Redis")
    except Exception as e:
        print(f"⚠️ Redis connection failed: {e}")

async def close_redis():
    """Close Redis connection."""
    try:
        await redis_client.close()
        print("✅ Redis connection closed")
    except Exception as e:
        print(f"⚠️ Error closing Redis connection: {e}")

async def create_indexes():
    """Create indexes on application startup."""
    try:
        await url_collection.create_index("shortUrl", unique=True)
    except Exception as e:
        print(f"Index creation warning: {e}")