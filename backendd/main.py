from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas, utils
from .database import engine, SessionLocal

# Create database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorturls", response_model=schemas.ShortURLResponse, status_code=201)
def create_short_url(data: schemas.ShortURLCreate, db: Session = Depends(get_db)):
    # Check custom shortcode or generate
    shortcode = data.shortcode if data.shortcode else utils.generate_shortcode()
    if db.query(models.ShortURL).filter(models.ShortURL.shortcode == shortcode).first():
        raise HTTPException(status_code=400, detail="Shortcode already exists")
    
    expiry_time = datetime.utcnow() + timedelta(minutes=data.validity)
    new_url = models.ShortURL(
        original_url=data.url,
        shortcode=shortcode,
        expiry=expiry_time
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "shortLink": f"http://localhost:8000/{shortcode}",
        "expiry": expiry_time
    }

@app.get("/shorturls/{shortcode}", response_model=schemas.URLStats)
def get_stats(shortcode: str, db: Session = Depends(get_db)):
    url = db.query(models.ShortURL).filter(models.ShortURL.shortcode == shortcode).first()
    if not url:
        raise HTTPException(status_code=404, detail="Shortcode not found")
    return {
        "original_url": url.original_url,
        "created_at": url.created_at,
        "expiry": url.expiry,
        "clicks": url.clicks
    }

@app.get("/{shortcode}")
def redirect(shortcode: str, db: Session = Depends(get_db)):
    url = db.query(models.ShortURL).filter(models.ShortURL.shortcode == shortcode).first()
    if not url:
        raise HTTPException(status_code=404, detail="Shortcode not found")
    if datetime.utcnow() > url.expiry:
        raise HTTPException(status_code=410, detail="Shortcode expired")

    url.clicks += 1
    db.commit()
    return {"message": f"Redirect to {url.original_url}"}  # Replace with actual RedirectResponse later
