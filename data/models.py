from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import HttpUrl, field_validator
import logging
from typing import Optional, Literal
from enum import Enum
import re

logger = logging.getLogger(__name__)

class status_enum(str, Enum):
    NOWE = "Nowe"
    UZYWANE = "Uzywane"
    USZKODZONE = "Uszkodzone"

class Laptop(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    marketplace_id: Optional[str] = Field(default=None, index=True)
    title: str = Field(...)
    price: float = Field(...)
    model: Optional[str] = Field(default="", description="Laptop manufacturer and model")
    cpu: Optional[str] = Field(default="")
    gpu: Optional[str] = Field(default="")
    ram: Optional[int] = Field(default=0, description="Amount of GB of RAM in the laptop")
    storage: Optional[int] = Field(default=0, description="Amount of GB of storage")
    status: status_enum = Field(...)
    location: str = Field(...)
    appearance_time: Optional[datetime] = Field(default=None)
    disappearance_time: Optional[datetime] = Field(default=None)
    link: str = Field(...)
    description: Optional[str] = Field(default=None)

#Validators

    @field_validator("title", "location", mode="before")
    @classmethod
    def strip_required_strings(cls, value):
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        return value.strip()

    @field_validator("price", mode="before")
    @classmethod
    def parse_price(cls, value):
        if value is None:
            raise ValueError("Price cannot be None")
        
        if isinstance(value, (float, int)):
            return float(value)
        
        if value == "Zamienię" or value == "Za darmo":
            return 0.0
        
        match = re.search(r"[\d\s.,]+", value)
        if not match:
            raise ValueError(f"Invalid price format: {value}")
        numeric_str = match.group(0)
        numeric_str = numeric_str.replace(" ", "").replace(",", ".")
        try:
            return float(numeric_str)
        except ValueError:
            raise ValueError(f"Invalid price format after cleaning: {numeric_str}")
        
    @field_validator("ram", mode="before")
    @classmethod
    def parse_ram(cls, value):
        if value is None:
            return 0
        if isinstance(value, (int, float)):
            return int(value)
        match = re.search(r"(\d{1,4})\s*GB", str(value), re.IGNORECASE)
        return int(match.group(1)) if match else 0
    
    @field_validator("storage", mode="before")
    @classmethod
    def parse_storage(cls, value):
        if value is None:
            return 0
        if isinstance(value, (int, float)):
            return int(value)
        match = re.search(r"(\d{1,4})\s*(GB|TB)", str(value), re.IGNORECASE)
        if not match:
            return 0
        size = int(match.group(1))
        unit = match.group(2).upper()
        return size * 1000 if unit == "TB" else size
    
    @field_validator("status", mode="before")
    @classmethod
    def parse_status(cls, value):
        if isinstance(value, status_enum):
            return value

        if isinstance(value, str):
            normalized = value.strip().lower()

            mapping = {
                "nowe": status_enum.NOWE,
                "używane": status_enum.UZYWANE,
                "uzywane": status_enum.UZYWANE,  # fallback
                "uszkodzone": status_enum.USZKODZONE,
            }

            if normalized in mapping:
                return mapping[normalized]

        logger.error(f"Invalid status value: {value}")
        raise ValueError(f"Invalid status: {value}")

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
