from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio
import logging
import configs.scraper_config as scraper_config

from data.models import Laptop, create_laptop
"""
This script serves to extract laptop data from the websites.
"""

logger = logging.getLogger(__name__)

class DataScraper:

    html_page = scraper_config.olx_html_page
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async def main():
        laptops = await DataScraper.fetch_all_laptops()
        return laptops
    
    @staticmethod
    async def fetch_all_laptops() -> list:
        async with aiohttp.ClientSession() as session:
            amount_of_pages = await DataScraper.get_amount_of_pages(session)
            urls =  DataScraper.generate_page_urls(amount_of_pages)
            tasks = DataScraper.create_scrape_tasks(session, urls)
            logger.info(f"Scraping {amount_of_pages} pages asynchronously...")
            results = await asyncio.gather(*tasks)
            return DataScraper.unite_scraping_results(results)
        
    @staticmethod
    async def get_amount_of_pages(session):
        page_numbers = await DataScraper.get_pagination_numbers(session, DataScraper.html_page)
        amount_of_pages = max(page_numbers)
        return amount_of_pages
    
    @staticmethod
    async def get_pagination_numbers(session, url: str):
        soup = await DataScraper.get_html_page(session, url)
        pagination = soup.select(scraper_config.olx_pagination_selector)
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
    async def get_html_page(session, url: str):
        logger.info(f"Getting HTML page from: {url}...")
        async with session.get(url, headers=DataScraper.headers) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'lxml')
        logger.info("HTML page retrieved.")
        return soup

    @staticmethod
    def generate_page_urls(amount_of_pages: int) -> list[str]:
        base_url = DataScraper.html_page
        return [
            base_url.replace("page=1", f"page={page}")
            for page in range(1, amount_of_pages + 1)
        ]

    @staticmethod
    def create_scrape_tasks(session, urls: list[str]) -> list:
        tasks = []
        for i, url in enumerate(urls, start=1):
            logger.info(f"Appending process_page task nr {i} asynchronously...")
            tasks.append(DataScraper.process_page(session, url))
        return tasks    
    
    @staticmethod
    async def process_page(session, url: str):
        listings = await DataScraper.get_listings(session, url)
        laptops_data = await DataScraper.get_data_from_listings(session, listings)
        laptop_models = DataScraper.turn_data_into_laptop_model(laptops_data)
        return laptop_models

    @staticmethod
    async def get_listings(session, url: str):
        soup = await DataScraper.get_html_page(session, url)
        logger.info(f"Starting to scrape listings from: {url}")
        listings = soup.select(scraper_config.olx_listing_selector)
        return listings

    @staticmethod
    async def get_data_from_listings(session, listings):
        laptop_data_list = []
        for listing in listings:
            logger.info(f"Working on listing: {str(listing)[:100]}...")

            link = 'https://www.olx.pl' + listing.select_one(scraper_config.olx_link_selector).get('href')
            description = await DataScraper.get_description(session, link)

            laptop_data = {
                'marketplace_id': DataScraper.get_id_from_link(link),
                'title': listing.select_one(scraper_config.olx_title_selector).text,
                'price': listing.select_one(scraper_config.olx_price_selector).text.strip(),
                'status': listing.select_one(scraper_config.olx_status_selector).text,
                'location': listing.select_one(scraper_config.olx_location_selector).text,
                'link': link,
                'appearance_time': None,
                'disappearance_time': None,
                'description': description,
                'model': DataScraper.get_laptop_components_from_description("model", description),
                'cpu': DataScraper.get_laptop_components_from_description("cpu", description),
                'ram': DataScraper.get_laptop_components_from_description("ram", description),
                'storage': DataScraper.get_laptop_components_from_description("storage", description),
                'gpu': DataScraper.get_laptop_components_from_description("gpu", description),
            }
            laptop_data_list.append(laptop_data)
        return laptop_data_list
    
    @staticmethod
    async def get_description(session, url: str):
        soup = await DataScraper.get_html_page(session, url)
        description_element = soup.select_one(scraper_config.olx_description_selector)
        description = description_element.get_text(separator="\n") if description_element else ""
        logger.info(f"Description has been retrieved successfully: {description[:100]} from {url}.")
        return description
    
    @staticmethod
    def get_id_from_link(url: str):
        logger.info(f"Getting ID from link {url}...")
        match = re.search(r"-ID([a-zA-Z0-9]+)\.html$", url)
        if match:
            logger.info(f"Successful ID match has been found in url: {match}")
            return match.group(1)

    @staticmethod
    def get_laptop_components_from_description(component_type, description):
        regex_map = scraper_config.regex_selectors
        pattern = regex_map.get(component_type)
        if pattern:
            match = re.search(pattern, description)
            if match:
                return match.group(1)
        return ""

    @staticmethod
    def turn_data_into_laptop_model(laptops_data):
        devices = []
        for laptop_data in laptops_data:
            validated_laptop = create_laptop(laptop_data)
            devices.append(validated_laptop)

            logger.info("WORK ON LISTING DONE. RESULTS:\n\n"
            f"marketplace_id: {laptop_data['marketplace_id']}, \n" 
            f"laptop {laptop_data['title']} data: \n" 
            f"price: {laptop_data['price']}, \n"
            f"status: {laptop_data['status']}, \n"
            f"model: {laptop_data['model']}\n"
            f"cpu: {laptop_data['cpu']}\n"
            f"ram: {laptop_data['ram']}\n"
            f"storage: {laptop_data['storage']}\n"
            f"gpu: {laptop_data['gpu']}\n"
            f"location: {laptop_data['location']}, \n"
            f"link: {laptop_data['link']}, \n"
            f"description: {laptop_data['description'][:300]}...\n\n\n")
        return devices
         
    @staticmethod 
    def unite_scraping_results(results):
        laptops = [item for sublist in results for item in sublist]
        logger.info(f"Scraped {len(laptops)} laptops.")
        return laptops

if __name__ == "__main__":
    asyncio.run(DataScraper.main())
