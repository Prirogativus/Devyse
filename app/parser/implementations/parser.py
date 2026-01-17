from bs4 import BeautifulSoup
from scraper.interfaces import AbstractHTMLParser
import configs.scraper_config as scc
import logging
import re

logger = logging.getLogger(__name__)

class OlxParser(AbstractHTMLParser):
    def __init__(self, 
                 listing_selector: str = scc.olx_listing_selector,
                 title_selector: str = scc.olx_title_selector,
                 price_selector: str = scc.olx_price_selector,
                 status_selector: str = scc.olx_status_selector,
                 location_selector: str = scc.olx_location_selector,
                 link_selector: str = scc.olx_link_selector,
                 ):
        self.listing_selector = listing_selector
        self.title_selector = title_selector
        self.price_selector = price_selector
        self.status_selector = status_selector
        self.location_selector = location_selector
        self.link_selector = link_selector

    def process_page(self, soup):
        """Process an OLX page and extract laptop data from all listings."""
        listings = self.get_listings(soup)
        laptops_data = []
        for listing in listings:
            try: 
                laptops_data.append(self.extract_laptop_data_from_listing(listing))
            except ValueError:
                raise ValueError(f"Could not extract data from listing: {listing}")
        return laptops_data

    def get_listings(self, soup: BeautifulSoup):
        """Select extract and return all listings from the HTML soup."""
        logger.info(f"Starting to scrape listings.")
        return soup.select(self.listing_selector)
    
    def extract_laptop_data_from_listing(self, listing) -> dict:
        """
        Extract and return all available laptop data from
        a single listing element.
        """
        return self.create_laptop_data_dict(
            marketplace_id=self.get_marketplace_id_from_link(self.get_link(listing)),
            title=self.get_title(listing),
            price=self.get_price(listing),
            status=self.get_status(listing),
            location=self.get_location(listing),
            link=self.get_link(listing),
        )
    
    def create_laptop_data_dict(self, 
                                marketplace_id, 
                                title, 
                                price, 
                                status,
                                location,
                                link,
                                ) -> dict:
        """Create and return a dictionary with laptop data."""
        return {
            'marketplace_id': marketplace_id,
            'title': title,
            'price': price,
            'status': status,
            'location': location,
            'link': link,
            'appearance_time': None,
            'disappearance_time': None,
            'description': None,
            'model': None,
            'cpu': None,
            'ram': None,
            'storage': None,
            'gpu': None,
        }

    def get_marketplace_id_from_link(self, link: str) -> str:
        """Extract and return the marketplace ID from a listing link."""
        logger.info(f"Getting ID from link {link}...")
        
        id_match = re.search(r"-ID([a-zA-Z0-9]+)\.html(?:\?|$)", link)
        
        if id_match:
            marketplace_id = id_match.group(1)
            logger.info(f"Successful ID match has been found in url: {link}, ID: {marketplace_id}")
            return marketplace_id
        else:
            raise ValueError(f"No ID found in link: {link}")
        
    def get_title(self, listing):
        """Extract and return the title from a listing element."""
        logger.info(f"Getting title from listing...")
        return listing.select_one(self.title_selector).text
    
    def get_price(self, listing):
        """Extract and return the price from a listing element."""
        logger.info(f"Getting price from listing...")
        return listing.select_one(self.price_selector).text.strip()
    
    def get_status(self, listing):
        """Extract and return the status from a listing element."""
        logger.info(f"Getting status from listing...")
        return listing.select_one(self.status_selector).text
    
    def get_location(self, listing):
        """Extract and return the location from a listing element."""
        logger.info(f"Getting location from listing...")
        return listing.select_one(self.location_selector).text
    
    def get_link(self, listing):
        """Extract and return the link from a listing element."""
        logger.info(f"Getting link from listing...")
        link = 'https://www.olx.pl' + listing.select_one(self.link_selector).get('href')
        return link

        


