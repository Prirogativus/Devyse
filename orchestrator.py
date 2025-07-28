import scraper as scr
import data_manager as dm
import database_connector as db
import config as cfg
import asyncio
import logging
from logger_config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Workflow.")
    dm.laptops = asyncio.run(scr.DataScraper.main())
    dm.sync_with_database(dm.laptops)
    db.add_data(dm.laptops)
    logger.info("Workflow completed.")
if __name__ == "__main__":
    main()
