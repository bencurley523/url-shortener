import json
from datetime import datetime, timezone

from database import (
    counters_collection,
    url_collection,
    redis_client, 
    MACHINE_ID, 
    MACHINE_OFFSET,
    CACHE_KEY_PREFIX,
    CACHE_TTL
)

# Generator Function
async def get_next_sequence_id(sequence_name: str = "url_id") -> int:
    """
    Atomically increments a counter and combines it with Machine ID.
    Formula: (MACHINE_ID << MACHINE_OFFSET) | <seq_num>
    """
    # Get the next sequence number from the 'counters' collection
    counter = await counters_collection.find_one_and_update(
        {"_id": sequence_name},          # Look for the counter named "url_id"
        {"$inc": {"sequence_value": 1}}, # Increment by 1
        upsert=True,                     # Create if it doesn't exist
        return_document=True             # Return the NEW value
    )
    
    seq_num = counter["sequence_value"]
    unique_id = (MACHINE_ID << MACHINE_OFFSET) | seq_num
    
    return unique_id

async def update_stats(short_url: str):
    """
    Background task to update click counters (fire-and-forget)
    """
    try:
        await url_collection.update_one(
            {"shortUrl": short_url},
            {
                "$inc": {"clicks": 1},
                "$set": {"last_accessed": datetime.now(timezone.utc)}
            }
        )
    except Exception as e:
        print(f"❌ Error updating stats for {short_url}: {e}")

def get_cache_key(short_url: str) -> str:
    """Generate cache key for a short URL."""
    return f"{CACHE_KEY_PREFIX}{short_url}"

async def get_url_from_cache(short_url: str) -> dict | None:
    """
    Get URL data from Redis cache.
    Returns None if not found or on error.
    """
    try:
        cache_key = get_cache_key(short_url)
        cached_data = await redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        # Log error but don't fail - cache is optional
        print(f"⚠️ Cache read error: {e}")
    return None

async def set_url_in_cache(short_url: str, url_data: dict):
    """
    Store URL data in Redis cache.
    ttl defaults to CACHE_TTL if not provided.
    """
    try:
        cache_key = get_cache_key(short_url)
        # Convert datetime to ISO format string for JSON serialization
        cache_data = {
            "shortUrl": url_data["shortUrl"],
            "longUrl": url_data["longUrl"],
            "createdAt": url_data["createdAt"].isoformat() if isinstance(url_data["createdAt"], datetime) else url_data["createdAt"]
        }
        # await redis_client.setex(cache_key, CACHE_TTL, json.dumps(cache_data))
        await redis_client.set(cache_key, json.dumps(cache_data), ex=CACHE_TTL)
    except Exception as e:
        # Log error but don't fail - cache is optional
        print(f"⚠️ Cache write error: {e}")

async def delete_url_from_cache(short_url: str):
    """Delete URL data from Redis cache."""
    try:
        cache_key = get_cache_key(short_url)
        await redis_client.delete(cache_key)
    except Exception as e:
        # Log error but don't fail - cache is optional
        print(f"⚠️ Cache delete error: {e}")