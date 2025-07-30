from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import HttpUrl, validator
import logging
from typing import Optional, Literal
import re

logger = logging.getLogger(__name__)

class Laptop(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    marketplace_id: Optional[str] = Field(default=None, index=True)
    title: str = Field(...)
    price: float = Field(...)
    status: Literal["Nowe", "Używane", "Uszkodzone"] = Field(..., description="This field showing a listing status scraped from OLX")
    location: str = Field(...)
    link: HttpUrl
    description: Optional[str] = Field(default=None)
    appearance_time: Optional[datetime] = Field(default=None)
    disappearance_time: Optional[datetime] = Field(default=None)

#Validators

    @validator("price", pre=True)
    def parse_price(cls, value):
        if isinstance(value, (float, int)):
            return float(value)
        value = value.replace("zł", "").replace(" ", "").replace(",", ".")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid price format: {value}")

    @validator("title", "location", pre=True)
    def strip_required_strings(cls, value):
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        return value.strip()

    @validator("description", pre=True)
    def normalize_description(cls, value):
        if value is None:
            return ("NO DESCRIPTION")
        return value.strip()
    
    @validator("appearance_time", "disappearance_time", pre=True)
    def parse_datetime(cls, value):
        if value is None or isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except Exception:
            raise ValueError(f"Invalid datetime format: {value}")

#Factory Function

def create_laptop(data: dict) -> Laptop:
    try:
        laptop = Laptop(**data)
        return laptop
    except Exception as e:
        logger.error(f"[ERROR] Validation failed for laptop: {data.get('title', 'No title')}\n{e}")
