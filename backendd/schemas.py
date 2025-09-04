from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShortURLCreate(BaseModel):
    url: str
    validity: Optional[int] = 30  # default 30 minutes
    shortcode: Optional[str] = None

class ShortURLResponse(BaseModel):
    shortLink: str
    expiry: datetime

class URLStats(BaseModel):
    original_url: str
    created_at: datetime
    expiry: datetime
    clicks: int
