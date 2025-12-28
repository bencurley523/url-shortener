from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime
from typing import Optional
import re

class URLCreate(BaseModel):
    longUrl: HttpUrl = Field(..., description="The original long URL") # Ensures http(s) for security
    custom_alias: Optional[str] = Field(None, min_length=1, max_length=50, description="Custom short URL alias")

    @field_validator('custom_alias')
    @classmethod
    def validate_custom_alias(cls, v):
        if v is None:
            return v
        # Only allow alphanumeric characters, hyphens, and underscores
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Custom alias can only contain letters, numbers, hyphens, and underscores')
        # Reserve FastAPI routes
        reserved = {'docs', 'openapi.json', 'redoc', 'shorten'}
        if v.lower() in reserved:
            raise ValueError(f'Custom alias "{v}" is reserved')
        return v

class URLResponse(BaseModel):
    shortUrl: str
    longUrl: str
    createdAt: datetime

class URLStats(BaseModel):
    shortUrl: str
    longUrl: str
    clicks: int
    last_accessed: Optional[datetime] = None