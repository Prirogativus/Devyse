olx_html_page = "https://www.olx.pl/elektronika/komputery/laptopy/krakow/?page=1&search%5Border%5D=created_at%3Adesc"
olx_description_selector = "div[data-cy='ad_description']"
olx_link_selector = "a[href^='/d/']"
olx_listing_selector = "div[data-cy='l-card']"
olx_location_selector = "[data-testid='location-date']"
olx_pagination_selector = "ul[data-testid='pagination-list'] li[data-testid='pagination-list-item'] a"
olx_price_selector = "[data-testid='ad-price']"
olx_status_selector = '[title="Nowe"], [title="Używane"], [title="Uszkodzone"]'
olx_title_selector = "a[href^='/d/'] h3, a[href^='/d/'] h4, a[href^='/d/'] h5, a[href^='/d/'] h6"


# Database configuration
DB_SERVER = "localhost"
DB_NAME = "postgres"
DB_PORT = 5432
DB_USERNAME = "postgres"
DB_PASSWORD = "1234"