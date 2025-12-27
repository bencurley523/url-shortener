from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Path
from fastapi.background import BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError, PyMongoError

from .database import (
    url_collection,
    verify_connection, 
    create_indexes,
    verify_redis_connection,
    close_redis,
)
from .crud import get_next_sequence_id, update_stats, get_url_from_cache, set_url_in_cache
from .models import URLCreate, URLResponse
from .utils import base62_encode

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify connections and create indexes
    await verify_connection()
    await create_indexes()
    await verify_redis_connection()
    yield
    # Shutdown: cleanup connections
    await close_redis()
    # Motor handles MongoDB connection cleanup automatically

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5500",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(url: URLCreate):
    """Create a shortened URL."""
    short_url = url.custom_alias if url.custom_alias else base62_encode(await get_next_sequence_id())

    # Convert HttpUrl to string for storage
    long_url_str = str(url.longUrl)
    
    new_url = {
        "shortUrl": short_url,
        "longUrl": long_url_str,
        "createdAt": datetime.now(timezone.utc)
    }
    
    try:
        await url_collection.insert_one(new_url)
        
        # Cache the new URL after successful insertion
        await set_url_in_cache(short_url, new_url)
        
        return URLResponse(
            shortUrl=new_url["shortUrl"],
            longUrl=new_url["longUrl"],
            createdAt=new_url["createdAt"]
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Short code already taken"
        )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}"
        )

@app.get("/{short_url}")
async def redirect_to_url(
    background_tasks: BackgroundTasks,
    short_url: str = Path(..., description="The short URL code", min_length=1, max_length=50)
):
    """Redirect to the original URL."""
    try:
        # Try to get from cache first
        url_data = await get_url_from_cache(short_url)

        # Uncomment for testing without cache
        # url_data = None
        
        if not url_data:
            # Cache miss - get from MongoDB
            url_data = await url_collection.find_one({"shortUrl": short_url})
            
            if not url_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
            
            # Cache the result for future requests
            await set_url_in_cache(short_url, url_data)
            print("No Cache Hit :(")
        else:
            print(f"⚡ Cache Hit")
        
        # Extract long URL from cached or database result
        long_url = url_data["longUrl"]

        # Update stats
        background_tasks.add_task(update_stats, short_url)
        
        return RedirectResponse(
            url=long_url,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}"
        )