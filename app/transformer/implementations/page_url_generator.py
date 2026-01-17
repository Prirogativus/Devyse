from scraper.interfaces import AbstractPageUrlGenerator
import configs.scraper_config as scc

class PageUrlGenerator(AbstractPageUrlGenerator):
    def __init__(self, base_url: str = scc.olx_html_page):
        self.base_url = base_url

    def generate_page_urls(self, amount_of_pages: int) -> list[str]:
        """Generate a list of page URLs based on the base URL and the number of pages."""
        return [
            self.base_url.replace("page=1", f"page={page}")
            for page in range(1, amount_of_pages + 1)
            ]
    