from bs4 import BeautifulSoup
import aiohttp
import logging
from app.network.abstractions.http_client import AbstractHttpClient
from app.network.implementations.session import SessionManager

logger = logging.getLogger(__name__)

class HttpClient(AbstractHttpClient):
    def __init__(self, session_manager: SessionManager):
        self.session = session_manager

    async def fetch_html(self, url: str) -> BeautifulSoup:
        """Fetch the HTML content from the given URL and return a BeautifulSoup object."""
        logger.info(f"Getting HTML page from: {url}...")
        async with self.session.semaphore:
            try:
                async with self.session.get(url, headers=self.session.headers) as response:
                    raw_html = await response.text()
                    logger.info("HTML page retrieved.")
                    return raw_html
            except aiohttp.ClientPayloadError as e:
                raise aiohttp.ClientPayloadError(f"Failed to fetch {url}: {e}")

# FUTURE IMPROVEMENTS:
# 1. More exeption handling
# 2. Status code checking (404 etc.)
# 3. No retries

