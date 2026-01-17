from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LaptopListing(Base):
    __tablename__  = "laptops"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    marketplace_id = Column(String(255), nullable=False, unique=True, index=True)
    title = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    model = Column(String(255))
    cpu = Column(String(255))
    gpu = Column(String(255))
    ram = Column(Integer)
    storage = Column(Integer)
    status = Column(String(255))
    location = Column(String(255), nullable=False)
    appearance_time = Column(DateTime(timezone=True), nullable=True)
    disappearance_time = Column(DateTime(timezone=True), nullable=True)
    link = Column(Text, nullable=False)
    description = Column(Text, nullable=True)