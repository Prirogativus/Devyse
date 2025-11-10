from datetime import datetime
from typing import List, Dict
from data.models import Laptop
import logging
from data.database_connector import DatabaseConnector as dbc
import data.db_session as db_session

logger = logging.getLogger(__name__)

def fetch_database_laptops() -> List[Laptop]:
    """Return all laptops from the database or an empty list if none exist."""
    laptops = dbc.get_data()
    return laptops if laptops else []

def identify_changes(scraped_laptops: List[Laptop], db_laptops: List[Laptop]) -> Dict[str, List[Laptop]]:
    """
    Comparing all laptops from source (currently: data_scraper) website and the rest of laptops in the database.

    If laptops are in the scraped laptops list but not in the database laptops list, 
    that means they are new and should be added to a database, with timestamp of their appeaeance(appearance_time).

    If laptops are in the database but not at the website anymore, that means that their disappearance_time have to be timestamped.
     
    """
    logger.debug(scraped_laptops)
    scraped_map = {l.marketplace_id: l for l in scraped_laptops}
    db_map = {l.marketplace_id: l for l in db_laptops}

    scraped_ids = set(scraped_map.keys())
    db_ids = set(db_map.keys())

    new_ids = scraped_ids - db_ids
    removed_ids = db_ids - scraped_ids

    new_laptops = [scraped_map[_id] for _id in new_ids]
    removed_laptops = [db_map[_id] for _id in removed_ids]

    return {
        "new": new_laptops,
        "removed": removed_laptops
    }

def update_timestamps_for_new(laptops: List[Laptop]) -> None:
    """Timestamping appearance for a list of laptops"""
    now = datetime.now()
    for laptop in laptops:
        laptop.appearance_time = now
        logger.info(f"Timestamp appearance: {laptop.title}, ID: {laptop.marketplace_id}")

def update_timestamps_for_removed(laptops: List[Laptop]) -> None:
    """Timestamping dissapearance for a list of laptops"""
    now = datetime.now()
    for laptop in laptops:
        laptop.disappearance_time = now
        dbc.modify_data(laptop.marketplace_id, laptop.disappearance_time)
        logger.info(f"Timestamp disappearance: {laptop.title}, ID: {laptop.marketplace_id}")

def sync_with_database(scraped_laptops: List[Laptop]):
    """This function orchestrates all previous functions"""
    db_laptops = fetch_database_laptops()
    changes = identify_changes(scraped_laptops, db_laptops)

    if changes["new"]:
        update_timestamps_for_new(changes["new"])
        logger.info(f"Adding {len(changes['new'])} new laptops to the database.")
        dbc.add_data(changes["new"])

    if changes["removed"]:
        update_timestamps_for_removed(changes["removed"])
        logger.info(f"Processed disappearance for {len(changes['removed'])} laptops.")
    db_session.session.expire_all()
