from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import HttpUrl, field_validator
import logging
from typing import Optional, Literal
from enum import Enum
import re

logger = logging.getLogger(__name__)

class Status(str, Enum):
    NOWE = "Nowe"
    UZYWANE = "Używane"
    USZKODZONE = "Uszkodzone"

class Laptop(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    marketplace_id: Optional[str] = Field(default=None, index=True)
    title: str = Field(...)
    price: float = Field(...)
    status: Status = Field(...)
    location: str = Field(...)
    link: str
    description: Optional[str] = Field(default=None)
    appearance_time: Optional[datetime] = Field(default=None)
    disappearance_time: Optional[datetime] = Field(default=None)

#Validators

    @field_validator("price", mode="before")
    @classmethod
    def parse_price(cls, value):
        if value is None:
            raise ValueError("Price cannot be None")
        if isinstance(value, (float, int)):
            return float(value)
        value = value.replace("zł", "").replace(" ", "").replace(",", ".")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid price format: {value}")

    @field_validator("title", "location", mode="before")
    @classmethod
    def strip_required_strings(cls, value):
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        return value.strip()

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value):
        if value is None:
            return "NO DESCRIPTION"
        return value.strip()
    
    @field_validator("appearance_time", "disappearance_time", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        if value is None or isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except Exception:
            raise ValueError(f"Invalid datetime format: {value}")
        
#Factory Function

def create_laptop(data: dict) -> Laptop:
    return Laptop.model_validate(data)
