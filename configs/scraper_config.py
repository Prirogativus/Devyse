olx_html_page = "https://www.olx.pl/elektronika/komputery/laptopy/krakow/?page=1&search%5Border%5D=created_at%3Adesc"
olx_description_selector = "div[data-cy='ad_description']"
olx_link_selector = "a[href^='/d/']"
olx_listing_selector = "div[data-cy='l-card']"
olx_location_selector = "[data-testid='location-date']"
olx_pagination_selector = "ul[data-testid='pagination-list'] li[data-testid='pagination-list-item'] a"
olx_price_selector = "[data-testid='ad-price']"
olx_status_selector = '[title="Nowe"], [title="Używane"], [title="Uszkodzone"]'
olx_title_selector = "a[href^='/d/'] h3, a[href^='/d/'] h4, a[href^='/d/'] h5, a[href^='/d/'] h6"

#RegExes
regex_selectors = {
    "model": r"(Dell|Lenovo|HP|Asus|Acer|MSI|Apple)[\s\-]*([A-Za-z0-9\s\-]{2,})",
    "cpu": r"(Intel|AMD)\s*(Core\s*)?(i[3579]|Ryzen\s*[3579]|Athlon|Pentium|Celeron)[\s\-]*([A-Za-z0-9\-]+)?",
    "ram": r"(RAM|Pamięć RAM|Pamięć operacyjna)[\s:\-]*([\d]{1,2})\s*(GB|G[Bb])",
    "storage": r"(Dysk|Pamięć(?!\s*RAM))[\s:\-]*([\d]{3,4})\s*(GB|TB)\s*(SSD|HDD|NVMe|M\.2)?",
    "gpu": r"(NVIDIA|AMD|Intel)\s*(GeForce|Radeon|UHD|Iris)?\s*([A-Za-z0-9\s\-]+)?"
}
