from sqlalchemy import Column, String, Integer, DateTime
from .database import Base
import datetime

class ShortURL(Base):
    __tablename__ = "shorturls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    shortcode = Column(String, unique=True, index=True, nullable=False)
    expiry = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    clicks = Column(Integer, default=0)
