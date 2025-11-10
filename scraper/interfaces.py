from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import aiohttp

class AbstractHttpClient(ABC):
    @abstractmethod
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
        pass

class AbstractPaginationHandler(ABC):
    @abstractmethod
    def get_amount_of_pages(self, soup: BeautifulSoup) -> list[int]:
        pass

class AbstractHTMLParser(ABC):
    @abstractmethod
    def process_page(self, soup: BeautifulSoup) -> list[dict]:
        pass

class AbstractDescriptionParser(ABC):
    @abstractmethod
    def enrich_laptop_data_dict(self, laptop_data: dict, title: str, description: str) -> dict:
        pass

class AbstractPageUrlGenerator(ABC):
    @abstractmethod
    def generate_page_urls(self, amount_of_pages: int) -> list[str]:
        pass



