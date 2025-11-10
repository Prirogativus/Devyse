from bs4 import BeautifulSoup
import asyncio
import aiohttp
import logging
from scraper.interfaces import AbstractHttpClient

logger = logging.getLogger(__name__)

class HttpClient(AbstractHttpClient):
    def __init__(self, headers = None, semaphore: asyncio.Semaphore = asyncio.Semaphore(10)):
        self.headers = headers or {"User-Agent": "Mozilla/5.0"}
        self.semaphore = semaphore

    def session(self):
        return aiohttp.ClientSession(headers=self.headers)


    async def fetch(self, session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
        """Fetch the HTML content from the given URL and return a BeautifulSoup object."""
        logger.info(f"Getting HTML page from: {url}...")
        
        async with self.semaphore:
            try:
                async with session.get(url, headers=self.headers) as response:
                    text = await response.text()
                    logger.info("HTML page retrieved.")
                    return BeautifulSoup(text, 'lxml')
            except aiohttp.ClientPayloadError as e:
                raise aiohttp.ClientPayloadError(f"Failed to fetch {url}: {e}")
        

