from app.network.network_main import DataScraper as scr
import app.data.data_manager as dm
from app.data.models import turn_into_laptops
import config.scraper_config as scc
import asyncio
import logging
from config.logger_config import setup_logger


def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("Starting Workflow.")
    main_page = scr.fetch_main_page(scc.olx_html_page)
    laptops = turn_into_laptops(asyncio.run(scraper.scrape()))
    dm.sync_with_database(laptops)
    logger.info("Workflow completed.")
if __name__ == "__main__":
    main()


