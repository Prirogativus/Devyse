import pytest
from unittest.mock import AsyncMock, patch
from bs4 import BeautifulSoup

from scraper.data_scraper import DataScraper
from data.data_manager import Laptop


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.olx.pl/d/oferta/laptop-15-IDabc123.html", "abc123"),
        ("https://olx.pl/laptop-IDZ9X8.html", "Z9X8"),
        ("https://www.olx.pl/item-no-id.html", None),
        ("", None),
    ]
)
def test_get_id_from_link(url, expected):
    assert DataScraper.get_id_from_link(url) == expected


@pytest.mark.asyncio
async def test_get_pagination_numbers():
    html = """
        <span class="page">1</span>
        <span class="page">2</span>
        <span class="page">3</span>
    """
    soup = BeautifulSoup(html, "lxml")

    with patch.object(DataScraper, 'get_html_page', return_value=soup), \
         patch("configs.scraper_config.olx_pagination_selector", "span.page"):
        session = AsyncMock()
        result = await DataScraper.get_pagination_numbers(session, "http://test.com")
        assert result == [1, 2, 3]



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "html, expected",
    [
        ("<div class='desc'>Great condition</div>", "Great condition"),
        ("<div class='desc'>Used laptop with warranty</div>", "Used laptop with warranty")
    ]
)
async def test_get_description(html, expected):
    soup = BeautifulSoup(html, "lxml")

    with patch.object(DataScraper, 'get_html_page', return_value=soup), \
         patch("configs.scraper_config.olx_description_selector", "div.desc"):
        session = AsyncMock()
        description = await DataScraper.get_description(session, "http://dummy-url.com")
        assert description == expected


@pytest.mark.asyncio
async def test_get_listings():
    listing_html = """
    <div class="listing">
        <a class="link" href="/d/oferta/laptop-dell-ID123abc.html"></a>
        <h3 class="title">Dell Laptop</h3>
        <p class="price">1500 zł</p>
        <span class="status">Używane</span>
        <div class="location">Warszawa</div>
    </div>
    """
    soup = BeautifulSoup(listing_html, "lxml")

    with patch.object(DataScraper, 'get_html_page', return_value=soup), \
         patch.object(DataScraper, 'get_description', return_value="Opis laptopa"), \
         patch("configs.scraper_config.olx_listing_selector", "div.listing"), \
         patch("configs.scraper_config.olx_link_selector", "a.link"), \
         patch("configs.scraper_config.olx_title_selector", "h3.title"), \
         patch("configs.scraper_config.olx_price_selector", "p.price"), \
         patch("configs.scraper_config.olx_status_selector", "span.status"), \
         patch("configs.scraper_config.olx_location_selector", "div.location"), \
         patch("data.models.create_laptop", side_effect=lambda x: Laptop(**x)):  # возвращаем объект Laptop
        
        session = AsyncMock()
        listings = await DataScraper.get_listings(session, "http://test.com")
        
        assert len(listings) == 1
        laptop = listings[0]
        assert laptop.marketplace_id == "123abc"
        assert laptop.title == "Dell Laptop"
        assert laptop.price == "1500 zł"
        assert laptop.status == "Używane"
        assert laptop.location == "Warszawa"
        assert laptop.description == "Opis laptopa"


@pytest.mark.asyncio
async def test_main():
    fake_laptops_page_1 = [{"title": "Laptop 1"}]
    fake_laptops_page_2 = [{"title": "Laptop 2"}]

    with patch.object(DataScraper, 'get_pagination_numbers', return_value=[1, 2]), \
         patch.object(DataScraper, 'get_listings', side_effect=[fake_laptops_page_1, fake_laptops_page_2]):
        
        result = await DataScraper.main()
        assert len(result) == 2
        assert result[0]["title"] == "Laptop 1"
        assert result[1]["title"] == "Laptop 2"