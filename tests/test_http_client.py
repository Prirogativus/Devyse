import pytest
import aiohttp
from bs4 import BeautifulSoup
from aioresponses import aioresponses

from scraper.implementations.http_client import HttpClient

@pytest.mark.asyncio
async def test_fetch_success():
    """
    Test that HttpClient.fetch successfully retrieves HTML content
    and returns a BeautifulSoup object when response is 200 OK.
    """
    client = HttpClient()
    url = "http://example.com"
    html_content = "<html><body><h1>Hello</h1></body></html>"

    with aioresponses() as mocked:
        mocked.get(url, status=200, body=html_content)

        async with aiohttp.ClientSession() as session:
            result = await client.fetch(session, url)
    print(result)
    assert isinstance(result, BeautifulSoup)
    assert result.h1.text == "Hello"


@pytest.mark.asyncio
async def test_fetch_http_error():
    """
    Test that HttpClient.fetch returns None when an HTTP error
    (e.g., 404 Not Found) is encountered.
    """
    client = HttpClient()
    url = "http://example.com"

    with aioresponses() as mocked:
        mocked.get(url, status=404)

        async with aiohttp.ClientSession() as session:
            result = await client.fetch(session, url)
    assert result is None