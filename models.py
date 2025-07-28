from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import HttpUrl, validator

class Laptop(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    marketplace_id: str = Field(primary_key=True)
    title: str
    price: float
    status: str
    location: str
    link: str
    description: Optional[str] = None
    appearance_time: Optional[datetime] = None
    disappearance_time: Optional[datetime] = None

    @validator("price", pre=True)
    def parse_price(cls, value):

        if isinstance(value, (float, int)):
            return float(value)
        value = value.replace("zł", "").replace(" ", "").replace(",", ".")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid price format: {value}")

    @validator("title")
    def normalize_title(cls, v):
        return v.strip()

def create_laptop(data: dict) -> Optional[Laptop]:
    try:
        laptop = Laptop(**data)
        return laptop
    except Exception as e:
        print(f"[ERROR] Validation failed for laptop: {data.get('title', 'No title')}\n{e}")
        return None
