from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import aiohttp


class AbstractHtmlExtractor(ABC):
    @abstractmethod
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
        pass