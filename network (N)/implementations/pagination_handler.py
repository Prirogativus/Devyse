from scraper.interfaces import AbstractPaginationHandler 
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from configs.scraper_config import olx_pagination_selector as ops
import logging

logger = logging.getLogger(__name__)


class PaginationHandler(AbstractPaginationHandler):
    def __init__(self, pagination_selector: str = ops):
        self.pagination_selector = pagination_selector

    def get_amount_of_pages(self, soup: BeautifulSoup) -> int:
        """
        Extract pagination numbers from the HTML soup and return the maximum number.
        The maximum number indicates the total number of pages available.
        """
        pagination_elements = self.find_a_pagination_elements(soup)
        page_numbers = []
        for page in pagination_elements:
            try:
                page_numbers.append(self.get_number_from_element(page))
            except ValueError:
                raise ValueError(f"No valid pagination numbers found: {page}")
        return self.get_max_number(page_numbers)

    def get_max_number(self, pagination_numbers: list[int]) -> int:
        """Return the maximum number from a list of pagination numbers."""
        amount_of_pages = max(pagination_numbers)
        return amount_of_pages

    def find_a_pagination_elements(self, soup: BeautifulSoup) -> list:
        """Search for pagination elements in the HTML."""
        pagination = soup.select(self.pagination_selector)
        return pagination

    def get_number_from_element(self, page: str) -> int:
        """Extract and return the integer from a pagination element."""
        num = int(page.text.strip())
        logger.info("Retrieved pagination number: ", num)
        return num
    