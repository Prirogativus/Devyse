from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import psycopg2
import logging
from models import Laptop 
from config import DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, DB_NAME

logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
logger.info(f"Connecting to database at {DB_SERVER}:{DB_PORT}...")
engine = sqlalchemy.create_engine(DATABASE_URL)

Base = sqlalchemy.ext.declarative.declarative_base()

class LaptopListing(Base):
    __tablename__  = "listings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    marketplace_id = Column(String, nullable=False, unique=True, index=True)
    title = Column(String(100), nullable=False)
    price = Column(String, nullable=False)
    status = Column(String, nullable=False)
    location = Column(String, nullable=False)
    link = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    appearance_time = Column(DateTime(timezone=True), nullable=True)
    disappearance_time = Column(DateTime(timezone=True), nullable=True)

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()


def add_data(laptops: List[Laptop]):
    logger.info(f"Adding {len(laptops)} laptops to the database...")
    for laptop in laptops:
        new_listing = LaptopListing(
            marketplace_id=laptop.marketplace_id,
            title=laptop.title,
            price=laptop.price,
            status=laptop.status,
            location=laptop.location,
            link=laptop.link,
            description=laptop.description,
            appearance_time=laptop.appearance_time,
            disappearance_time=laptop.disappearance_time
        )
        session.add(new_listing)
    session.commit()
    logger.info(f"Inserted {len(laptops)} laptops into the database.")


def get_data() -> List[Laptop]:
    logger.info("Retrieving laptops from database...")
    listings = session.query(LaptopListing).all()
    laptops = []
    for listing in listings:
        laptop = Laptop(
            marketplace_id=listing.marketplace_id,
            title=listing.title,
            price=listing.price,
            status=listing.status,
            location=listing.location,
            link=listing.link,
            description=listing.description,
            appearance_time=listing.appearance_time,
            disappearance_time=listing.disappearance_time
        )
        laptops.append(laptop)
    logger.info(f"Retrieved {len(laptops)} laptops.")
    return laptops


def delete_data(marketplace_id: str):
    logger.info(f"Deleting listing with marketplace_id={marketplace_id}...")
    listing = session.query(LaptopListing).filter_by(marketplace_id=marketplace_id).first()
    if listing:
        session.delete(listing)
        session.commit()
        logger.info(f"Deleted listing with marketplace_id={marketplace_id}.")
    else:
        logger.info(f"No listing found with marketplace_id={marketplace_id}.")
