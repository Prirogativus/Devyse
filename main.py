import scraper.network_main as scr
import data.data_manager as dm
from data.models import turn_into_laptops
import asyncio
import logging
from configs.logger_config import setup_logger

setup_logger()

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Workflow.")
    scraper = scr.DataScraper()
    laptops = turn_into_laptops(asyncio.run(scraper.scrape()))
    dm.sync_with_database(laptops)
    logger.info("Workflow completed.")
if __name__ == "__main__":
    main()


