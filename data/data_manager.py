from datetime import datetime
from typing import List
from data.models import Laptop
import logging
from data.database_connector import get_data, add_data, modify_data

logger = logging.getLogger(__name__)

def sync_with_database(scraped_laptops: List[Laptop]):
    db_laptops: List[Laptop] = get_data() or []

    if not db_laptops:
        for laptop in scraped_laptops:
            timestamp_laptop(True, laptop)
            logger.info(f"Adding new laptop to the database: {laptop.title}, ID: {laptop.marketplace_id}")
        add_data(scraped_laptops)
        return

    scraped_ids = {laptop.marketplace_id for laptop in scraped_laptops}
    db_ids = {laptop.marketplace_id for laptop in db_laptops}

    new_ids = scraped_ids - db_ids
    removed_ids = db_ids - scraped_ids

    scraped_map = {laptop.marketplace_id: laptop for laptop in scraped_laptops}
    db_map = {laptop.marketplace_id: laptop for laptop in db_laptops}

    new_laptops = []
    for id in new_ids:
        laptop = scraped_map[id]
        timestamp_laptop(True, laptop)
        logger.info(f"Adding new laptop to the database: {laptop.title}, ID: {laptop.marketplace_id}")
        new_laptops.append(laptop)

    if new_laptops:
        add_data(new_laptops)

    for id in removed_ids:
        laptop = db_map[id]
        timestamp_laptop(False, laptop)
        logger.info(f"Add disappearance time for: {laptop.title}, ID: {laptop.marketplace_id}")


def timestamp_laptop(appearance: bool, laptop: Laptop):
    now = datetime.now()
    if appearance:
        laptop.appearance_time = now
        logger.info(f"Timestamping appearance: {laptop.title}, ID: {laptop.marketplace_id}")
    else:
        laptop.disappearance_time = now
        modify_data(laptop.title, laptop.disappearance_time)
        logger.info(f"Timestamping disappearance: {laptop.title}, ID: {laptop.marketplace_id}")
