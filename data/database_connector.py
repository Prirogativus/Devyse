import logging
from datetime import datetime
from typing import List
from enum import Enum

from data.db_session import session
from data.db_models import LaptopListing
from data.models import Laptop, status_enum
from data.laptop_mapper import laptop_to_db, db_to_laptop

logger = logging.getLogger(__name__)

class DatabaseConnector:
    @staticmethod
    def add_data(laptops: List[Laptop]):
        """Add multiple laptops to the database."""
        if not laptops:
            logger.info("No laptops to add.")
            return

        logger.info(f"Adding {len(laptops)} laptops to the database...")

        parameters = []
        for laptop in laptops:
            status = laptop.status
            if isinstance(status, Enum):
                status_value = status.value
            elif isinstance(status, str):
                if status not in [s.value for s in status_enum]:
                    logger.warning(f"Skipping laptop with unknown status: {status}")
                    continue
                status_value = status
            else:
                logger.warning(f"Skipping laptop with invalid status type: {status}")
                continue

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

        from sqlalchemy import text
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
        try:
            session.execute(insert_query, parameters)
            session.commit()
            logger.info(f"Inserted {len(parameters)} laptops into the database.")
        except Exception as e:
            logger.error(f"Failed to insert laptops: {e}")
            session.rollback()

    @staticmethod
    def get_data() -> List[Laptop]:
        """Retrieve all laptops from the database."""
        logger.info("Retrieving laptops from database...")
        db_laptops = session.query(LaptopListing).all()
        laptops: List[Laptop] = [db_to_laptop(l) for l in db_laptops]
        logger.info(f"Retrieved {len(laptops)} laptops.")
        return laptops

    @staticmethod
    def delete_data(marketplace_id: str):
        """Delete a laptop from the database by its marketplace_id."""
        logger.info(f"Deleting listing with marketplace_id={marketplace_id}...")
        laptop = session.query(LaptopListing).filter_by(marketplace_id=marketplace_id).first()
        if laptop:
            session.delete(laptop)
            session.commit()
            logger.info(f"Deleted listing with marketplace_id={marketplace_id}.")
        else:
            logger.info(f"No listing found with marketplace_id={marketplace_id}.")

    @staticmethod
    def modify_data(marketplace_id: str, disappearance_time: datetime):
        """Set disappearance_time for a laptop identified by marketplace_id."""
        logger.info(f"Modifying data in the database for marketplace_id={marketplace_id}")
        laptop = session.query(LaptopListing).filter_by(marketplace_id=marketplace_id).first()
        if laptop:
            if laptop.disappearance_time is None:
                laptop.disappearance_time = disappearance_time
                session.commit()
                logger.info(f"Added disappearance time: {disappearance_time}, to the {laptop.title}")
            else:
                logger.info(f"Disappearance time is already existing.")
        else:
            logger.info(f"Can't find listing with marketplace_id={marketplace_id}")