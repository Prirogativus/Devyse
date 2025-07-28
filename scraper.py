from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio
import logging
import config

from models import Laptop, create_laptop
"""
This script serves to extract laptop data from the websites.
"""

logger = logging.getLogger(__name__)

class DataScraper:

    html_page = config.olx_html_page
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    @staticmethod
    async def get_html_page(session, url: str):
        logger.info(f"Getting HTML page from: {url}...")
        async with session.get(url, headers=DataScraper.headers) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')
        logger.info("HTML page retrieved.")
        return soup

    @staticmethod
    async def get_pagination_numbers(session, url: str):
        soup = await DataScraper.get_html_page(session, url)
        pagination = soup.select(config.olx_pagination_selector)
        logger.info(f"Getting pagination numbers from {url}...")

        page_numbers = []
        for page in pagination:
            try:
                num = int(page.text.strip())
                page_numbers.append(num)
                logger.info("Retrieved pagination number: ", num)
            except ValueError:
                continue

        logger.info(f"Pagination numbers found: {page_numbers}")
        return page_numbers

    @staticmethod
    def get_id_from_link(url: str):
        logger.info(f"Getting ID from link {url}...")
        match = re.search(r"-ID([a-zA-Z0-9]+)\.html$", url)
        if match:
            logger.info(f"Successful ID match has been found in url: {match}")
            return match.group(1)

    @staticmethod
    async def get_description(session, url: str):
        soup = await DataScraper.get_html_page(session, url)
        description = soup.select_one(config.olx_description_selector).text
        logger.info(f"Description has been retrieved successfully: {description[:100]} from {url}.")
        return description

    @staticmethod
    async def get_listings(session, url: str):
        soup = await DataScraper.get_html_page(session, url)
        devices = []

        logger.info(f"Starting to scrape listings from: {url}")
        listings = soup.select(config.olx_listing_selector)

        for listing in listings:

            logger.info(f"Working on listing: {listing}...")

            link = 'https://www.olx.pl' + listing.select_one(config.olx_link_selector).get('href')

            laptop_data = {
                'marketplace_id': DataScraper.get_id_from_link(link),
                'title': listing.select_one(config.olx_title_selector).text,
                'price': listing.select_one(config.olx_price_selector).text.strip(),
                'status': listing.select_one(config.olx_status_selector).text,
                'location': listing.select_one(config.olx_location_selector).text,
                'link': link,
                'description': await DataScraper.get_description(session, link),
                'appearance_time': None,
                'disappearance_time': None,
            }
            validated_laptop = create_laptop(laptop_data)

            devices.append(validated_laptop)

            logger.info("WORK ON LISTING DONE. RESULTS:\n\n"
                  f"marketplace_id: {laptop_data['marketplace_id']}, \n" 
                  f"Laptop {laptop_data['title']} data: \n" 
                  f"Price: {laptop_data['price']}, \n"
                  f"Status: {laptop_data['status']}, \n"
                  f"location: {laptop_data['location']}, \n"
                  f"link: {laptop_data['link']}, \n"
                  f"description: {laptop_data['description'][:300]}...\n\n\n")

        return devices

    async def main():
        async with aiohttp.ClientSession() as session:
            page_numbers = await DataScraper.get_pagination_numbers(session, DataScraper.html_page)
            max_page = max(page_numbers)

            tasks = []

            for page in range(1, max_page + 1):
                url = DataScraper.html_page.replace("page=1", f"page={page}")
                tasks.append(DataScraper.get_listings(session, url))
                logger.info(f"Appending get_listings task nr {page} asynchronously...")

            logger.info(f"Scraping {max_page} pages asynchronously...")
            results = await asyncio.gather(*tasks)

            laptops = [item for sublist in results for item in sublist]

            logger.info(f"Scraped {len(laptops)} laptops.")
            return laptops


if __name__ == "__main__":
    asyncio.run(DataScraper.main())
