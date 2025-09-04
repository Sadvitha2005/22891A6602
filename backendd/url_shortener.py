from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timedelta, timezone
import string, random

app = FastAPI(title="URL Shortener Service")

# In-memory storage (replace with DB in production)
url_store = {}

# Base domain for short links
BASE_URL = "http://localhost:8000/"

# -----------------------------
# Pydantic Models
# -----------------------------
class ShortenRequest(BaseModel):
    url: HttpUrl
    validity: int | None = 30  # minutes
    shortcode: str | None = None

class ShortenResponse(BaseModel):
    shortlink: str
    expiry: datetime

# -----------------------------
# Utility function
# -----------------------------
def generate_shortcode(length: int = 6) -> str:
    """Generate a random shortcode."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

# -----------------------------
# Main Route
# -----------------------------
@app.post("/shorturls", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest):
    # Calculate expiry time
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=request.validity)

    # Handle shortcode
    shortcode = request.shortcode
    if shortcode:
        if shortcode in url_store:
            raise HTTPException(status_code=409, detail="Shortcode already in use")
    else:
        # generate until unique
        shortcode = generate_shortcode()
        while shortcode in url_store:
            shortcode = generate_shortcode()

    # Save mapping
    url_store[shortcode] = {
        "url": request.url,
        "expiry": expiry_time
    }

    return ShortenResponse(
        shortlink=f"{BASE_URL}{shortcode}",
        expiry=expiry_time
    )

# -----------------------------
# Redirection route
# -----------------------------
@app.get("/{shortcode}")
def redirect_to_url(shortcode: str):
    entry = url_store.get(shortcode)
    if not entry:
        raise HTTPException(status_code=404, detail="Shortcode not found")

    if datetime.now(timezone.utc) > entry["expiry"]:
        raise HTTPException(status_code=410, detail="Short link has expired")

    return {"original_url": entry["url"]}
