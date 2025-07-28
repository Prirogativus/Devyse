from datetime import datetime
from typing import List
from models import Laptop
from database_connector import get_data, add_data


def sync_with_database(scraped_laptops: List[Laptop]):
    db_laptops: List[Laptop] = get_data() or []

    scraped_ids = {laptop.marketplace_id for laptop in scraped_laptops}
    db_ids = {laptop.marketplace_id for laptop in db_laptops}

    new_ids = scraped_ids - db_ids
    removed_ids = db_ids - scraped_ids

    scraped_map = {laptop.marketplace_id: laptop for laptop in scraped_laptops}
    db_map = {laptop.marketplace_id: laptop for laptop in db_laptops}

    for id in new_ids:
        laptop = scraped_map[id]
        timestamp_laptop(True, laptop)
        print(f"Adding new laptop to the database: {laptop.title}, ID: {laptop.marketplace_id}")
        add_data([laptop])

    for id in removed_ids:
        laptop = db_map[id]
        timestamp_laptop(False, laptop)
        print(f"Add disappearance time for: {laptop.title}, ID: {laptop.marketplace_id}")


    if not db_laptops:
        for laptop in scraped_laptops:
            timestamp_laptop(True, laptop)
            print(f"Adding new laptop to the database: {laptop.title}, ID: {laptop.marketplace_id}")
        add_data(scraped_laptops)


def timestamp_laptop(appearance: bool, laptop: Laptop):
    now = datetime.now()
    if appearance:
        laptop.appearance_time = now
        print(f"Timestamping appearance: {laptop.title}, ID: {laptop.marketplace_id}")
    else:
        laptop.disappearance_time = now
        print(f"Timestamping disappearance: {laptop.title}, ID: {laptop.marketplace_id}")
