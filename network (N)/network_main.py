import asyncio
import logging
import scraper.interfaces as infs
from configs import scraper_config as scc
from scraper.implementations.http_client import HttpClient
from scraper.implementations.pagination_handler import PaginationHandler
from scraper.implementations.page_url_generator import PageUrlGenerator
from scraper.implementations.parser import OlxParser
from scraper.implementations.description_parser import DescriptionParser


class DataScraper:
    """Coordinates scraping operations using abstracted components for HTTP, pagination, parsing, and enrichment."""

    def __init__(
        self,
        http_client: infs.AbstractHttpClient = HttpClient(),
        pagination_handler: infs.AbstractPaginationHandler = PaginationHandler(),
        page_url_generator: infs.AbstractPageUrlGenerator = PageUrlGenerator(),
        html_parser: infs.AbstractHTMLParser = OlxParser(),
        description_parser: infs.AbstractDescriptionParser = DescriptionParser(),
    ):
        """
        Initialize the DataScraper manager.

        Args:
            http_client: An instance implementing AbstractHttpClient for async HTML fetching.
            pagination_handler: An instance implementing AbstractPaginationHandler for page count extraction.
            page_url_generator: An instance implementing AbstractPageUrlGenerator for generating page URLs.
            html_parser: An instance implementing AbstractHTMLParser to extract listings from page HTML.
            description_parser_cls: Class implementing AbstractDescriptionParser for detail extraction.
        """
        self.http_client = http_client
        self.pagination_handler = pagination_handler
        self.page_url_generator = page_url_generator
        self.html_parser = html_parser
        self.description_parser = description_parser
        self.logger = logging.getLogger(__name__)

    async def scrape(self, base_url: str = scc.olx_html_page):
        """
        Orchestrates the full scraping workflow: pagination, page fetch, listing parse, and detail enrichment.

        Args:
            base_url (str): The starting URL for scraping (should be page 1).

        Returns:
            list[dict]: A list of dictionaries, each representing a fully enriched item.
        """
        async with self.http_client.session() as session:
            first_page_soup = await self.http_client.fetch(session, base_url)
            num_pages = self.pagination_handler.get_amount_of_pages(first_page_soup)
            self.logger.info(f"Found {num_pages} pages.")

            page_urls = self.page_url_generator.generate_page_urls(num_pages)

            page_tasks = [self.http_client.fetch(session, url) for url in page_urls]
            soups = await asyncio.gather(*page_tasks)

            listings = []
            for soup in soups:
                listings.extend(self.html_parser.process_page(soup))

            description_data_tasks = [self.enrich_laptop(session, laptop) for laptop in listings]
            laptops = await asyncio.gather(*description_data_tasks)
            return laptops

    async def enrich_laptop(self, session, laptop_data: dict):
        """
        Fetches and enriches a single laptop dictionary using its discription page.
        Args:
            session: The aiohttp client session for requests.
            laptop_data (dict): The basic listing data to be enriched.
        Returns:
            dict: The enriched laptop data with details parsed from the discription page.
        """
        description_page_soup = await self.http_client.fetch(session, laptop_data['link'])
        description_parser = self.description_parser
        return description_parser.enrich_laptop_data_dict(laptop_data=laptop_data, description_page=description_page_soup)