from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, Integer, String, text,  DateTime, Float, Text, Enum as SAEnum
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import logging
from enum import Enum
from data.models import Laptop, status_enum
from constants.constants_manager import DB_USERNAME, DB_PASSWORD, DB_SERVER, DB_PORT, DB_NAME

logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
logger.info(f"Connecting to database at {DB_SERVER}:{DB_PORT}...")
engine = sqlalchemy.create_engine(DATABASE_URL)

Base = sqlalchemy.ext.declarative.declarative_base()

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

Base.metadata.create_all(engine)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()


def add_data(laptops: List[Laptop]):
    if not laptops:
        logger.info("No laptops to add.")
        return

    logger.info(f"Adding {len(laptops)} laptops to the database...")


    insert_query = text("""
        INSERT INTO laptops (
            marketplace_id, title, price, model, cpu, gpu, ram,
            storage, status, location, appearance_time,
            disappearance_time, link, description
        )
        VALUES (
            :marketplace_id, :title, :price, :model, :cpu, :gpu, :ram,
            :storage, :status, :location, :appearance_time,
            :disappearance_time, :link, :description
        )
        ON CONFLICT (marketplace_id) DO NOTHING
    """)

    parameters = []
    for laptop in laptops:
        status = laptop.status
        if isinstance(status, Enum):
            status_value = status.value
        elif isinstance(status, str):
            if status not in status_enum.__members__.values():
                logger.warning(f"Skipping laptop with unknown status: {status}")
                continue
            status_value = status
        else:
            logger.warning(f"Skipping laptop with invalid status type: {status}")
            continue

        logger.debug(f"Laptop status value: {status_value}")

        parameters.append({
            "marketplace_id": laptop.marketplace_id,
            "title": laptop.title,
            "price": laptop.price,
            "model": laptop.model,
            "cpu": laptop.cpu,
            "gpu": laptop.gpu,
            "ram": laptop.ram,
            "storage": laptop.storage,
            "status": status_value,
            "location": laptop.location,
            "appearance_time": laptop.appearance_time,
            "disappearance_time": laptop.disappearance_time,
            "link": laptop.link,
            "description": laptop.description,
        })

    if not parameters:
        logger.info("No valid laptops to insert after validation.")
        return

    session.execute(insert_query, parameters)
    session.commit()
    logger.info(f"Inserted {len(parameters)} laptops into the database.")


def get_data() -> List[Laptop]:
    logger.info("Retrieving laptops from database...")
    db_laptops = session.query(LaptopListing).all()

    laptops: List[Laptop] = []
    for laptop in db_laptops:
        laptops.append(
            Laptop(
                marketplace_id=laptop.marketplace_id,
                title=laptop.title,
                price=laptop.price,
                model=laptop.model,
                cpu=laptop.cpu,
                gpu=laptop.gpu,
                ram=laptop.ram,
                storage=laptop.storage,
                status=laptop.status,
                location=laptop.location,
                appearance_time=laptop.appearance_time,
                disappearance_time=laptop.disappearance_time,
                link=laptop.link,
                description=laptop.description
            )
        )

    logger.info(f"Retrieved {len(laptops)} laptops.")
    return laptops


def delete_data(marketplace_id: str):
    logger.info(f"Deleting listing with marketplace_id={marketplace_id}...")
    laptop = session.query(LaptopListing).filter_by(marketplace_id=marketplace_id).first()
    if laptop:
        session.delete(laptop)
        session.commit()
        logger.info(f"Deleted listing with marketplace_id={marketplace_id}.")
    else:
        logger.info(f"No listing found with marketplace_id={marketplace_id}.")

def modify_data(marketplace_id: str, modification_value: datetime):
    logger.info(f"Modifying data in the database for marketplace_id={marketplace_id}")

    laptop = session.query(LaptopListing).filter_by(marketplace_id=marketplace_id).first()

    if laptop:
        if laptop.disappearance_time is None:
            laptop.disappearance_time = modification_value
            session.commit()
            logger.info(f"Added disappearance time: {modification_value}, to the {laptop.title}")
        else:
            logger.info(f"Disappearance time is already existing.")
    else:
        logger.info(f"Can't find listing with marketplace_id={marketplace_id}")

