from datetime import datetime
from typing import List
from data.models import Laptop
import logging
from data.database_connector import get_data, add_data, modify_data

logger = logging.getLogger(__name__)

def sync_with_database(scraped_laptops: List[Laptop]):
    db_laptops = fetch_laptops_from_db()
    new, removed = detect_changes(scraped_laptops, db_laptops)

    new = [timestamp_appearance(laptop) for laptop in new]
    removed = [timestamp_disappearance(laptop) for laptop in removed]

    save_new_laptops(new)
    update_removed_laptops(removed)

def  fetch_laptops_from_db() -> List[Laptop]:
    db_laptops: List[Laptop] = get_data() or []
    return db_laptops

def detect_changes(scraped_laptops: List[Laptop], db_laptops: List[Laptop]):
    new = scraped_laptops - db_laptops
    removed = db_laptops - scraped_laptops
    return new, removed

def timestamp_appearance(laptop: Laptop):
        now = datetime.now()
        laptop.appearance_time = now
        logger.info(f"Timestamping appearance: {laptop.title}, ID: {laptop.marketplace_id}")

def timestamp_disappearance(laptop: Laptop):
        now = datetime.now()
        laptop.disappearance_time = now
        logger.info(f"Timestamping disappearance: {laptop.title}, ID: {laptop.marketplace_id}")

def save_new_laptops(new_laptops: List[Laptop]):
    for laptop in new_laptops:
        timestamp_appearance(laptop)
        logger.info(f"Adding new laptop to the database: {laptop.title}, ID: {laptop.marketplace_id}")
    add_data(new_laptops)

def update_removed_laptops(removed_laptops: List[Laptop]):
    for laptop in removed_laptops:
        timestamp_disappearance(laptop)
        modify_data(laptop.title, laptop.disappearance_time)
        logger.info(f"Add disappearance time for: {laptop.title}, ID: {laptop.marketplace_id}")




