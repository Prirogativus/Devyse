"""Regular expressions and CSS selectors for parsing OLX laptop listings.

This module defines HTML selectors and regex patterns for extracting
structured information from OLX laptop advertisements, including
title, description, price, location, pagination, condition, brand,
model, CPU, RAM, storage, and GPU.
"""

import re

# ================= HTML Selectors =================

olx_html_page = "https://www.olx.pl/elektronika/komputery/laptopy/krakow/?page=1&search%5Border%5D=created_at%3Adesc"
olx_description_selector = "div[data-cy='ad_description']"
olx_link_selector = "a[href^='/d/']"
olx_listing_selector = "div[data-cy='l-card']"
olx_location_selector = "[data-testid='location-date']"
olx_pagination_selector = "ul[data-testid='pagination-list'] li[data-testid='pagination-list-item'] a"
olx_price_selector = "[data-testid='ad-price']"
olx_status_selector = '[title="Nowe"], [title="Używane"], [title="Uszkodzone"]'
olx_title_selector = "a[href^='/d/'] h3, a[href^='/d/'] h4, a[href^='/d/'] h5, a[href^='/d/'] h6"

# ================= Laptop Brand Regex Pattern =================

laptop_brands = [
    "Apple", "Dell", "HP", "Lenovo", "Asus", "Acer", "MSI", "Razer",
    "Samsung", "Microsoft", "Huawei", "LG", "Toshiba", "Sony",
    "Panasonic", "Fujitsu", "Gigabyte", "Chuwi", "Xiaomi", "Realme",
    "Infinix", "Clevo", "Eluktronics", "Alienware", "System76",
    "Origin PC", "EVGA", "Medion", "Dynabook", "Eurocom",
    "Durabook", "Schneider", "Vaio", "iBall", "Avita",
    "Hasee", "Teclast", "Thunderobot", "Mechrevo"
]

# ================= Laptop Model Regex Pattern =================

laptop_models = {
    "Apple": ["MacBook Air", "MacBook Pro"],
    "Dell": ["XPS", "Inspiron", "Latitude", "Vostro", "Precision", "G Series"],
    "HP": ["Pavilion", "Envy", "Spectre", "OMEN", "Victus", "EliteBook", "ProBook", "ZBook", "Chromebook"],
    "Lenovo": ["ThinkPad", "ThinkBook", "IdeaPad", "Yoga", "Legion", "LOQ"],
    "Asus": ["Zenbook", "Vivobook", "ROG", "TUF Gaming", "ProArt Studiobook", "ExpertBook", "Chromebook"],
    "Acer": ["Aspire", "Swift", "Spin", "TravelMate", "Nitro", "Predator", "ConceptD", "Chromebook"],
    "MSI": ["Modern", "Prestige", "Summit", "Stealth", "Raider", "Vector", "Cyborg", "Sword", "Katana", "Titan", "Creator"],
    "Razer": ["Blade", "Blade Stealth", "Razer Book"],
    "Samsung": ["Galaxy Book", "Galaxy Book Pro", "Galaxy Book Flex", "Notebook 9", "Odyssey"],
    "Microsoft": ["Surface Laptop", "Surface Laptop Studio", "Surface Book", "Surface Pro", "Surface Go"],
    "Huawei": ["MateBook D", "MateBook 13/14/16", "MateBook X", "MateBook X Pro", "MateBook E"],
    "LG": ["Gram", "Gram Style", "Gram SuperSlim", "Ultra PC"],
    "Toshiba": ["Satellite", "Tecra", "Portégé", "Qosmio"],
    "Sony": ["VAIO"],
    "Panasonic": ["Toughbook", "Let's Note"],
    "Fujitsu": ["Lifebook", "UH Series", "Celsius"],
    "Gigabyte": ["Aero", "Aorus", "G5/G7"],
    "Chuwi": ["HeroBook", "LapBook", "AeroBook", "CoreBook", "GemiBook", "MiniBook", "FreeBook"],
    "Xiaomi": ["Mi Notebook", "Mi Notebook Pro", "Xiaomi Book", "RedmiBook", "Redmi G"],
    "Realme": ["Book", "Book Slim", "Book Prime"],
    "Infinix": ["INBook", "Zero Book"],
    "Clevo": ["P Series", "N Series", "X Series", "W Series"],
    "Eluktronics": ["MECH-15/17", "MAX-15/17", "Prometheus", "RP-15/17"],
    "Alienware": ["m Series", "x Series", "Area-51m"],
    "System76": ["Lemur Pro", "Galago Pro", "Gazelle", "Darter Pro", "Oryx Pro", "Pangolin", "Kudu", "Serval WS"],
    "Origin PC": ["EON", "NT", "NS"],
    "EVGA": ["SC15", "SC17"],
    "Medion": ["Akoya", "Erazer"],
    "Dynabook": ["Satellite Pro", "Tecra", "Portégé"],
    "Eurocom": ["Sky", "Nightsky", "Tornado", "Shark", "Electra"],
    "Durabook": ["S Series (S14/S15)", "Z Series (Z14)", "R Series (R11)"],
    "Schneider": [],
    "Vaio": ["SX", "S", "Z", "Pro", "Fit"],
    "iBall": ["CompBook Excelance", "CompBook Marvel", "CompBook Aer3", "CompBook Exemplaire"],
    "Avita": ["Liber", "Pura", "Admiror", "Essential", "Magus"],
    "Hasee": ["Z Series", "K Series", "G Series"],
    "Teclast": ["F Series", "X Series", "Tbook"],
    "Thunderobot": ["911", "911 Air", "Zero"],
    "Mechrevo": ["Deep Sea Ghost", "Z Series", "X Series", "Code"]
}

# ================= CPU Regex Patterns =================

cpu_pattern = re.compile(r"""
\b
(?:(?P<brand>Intel|AMD)\s*)?       # Optional CPU brand: Intel or AMD
(?:Core\s*)?                        # Optional 'Core' keyword before family
(?P<family>i[3579]|Ryzen\s*[3579]) # CPU family: i3/i5/i7/i9 or Ryzen 3/5/7/9
(?:\s*Core)?                        # Optional 'Core' keyword after family
[\s-]?                              # Optional space or dash separator
(?P<model>\d{3,5})?                 # Optional CPU model number (3 to 5 digits)
(?P<suffix>[A-Za-z]{1,3})?          # Optional CPU suffix like K, F, U, etc.
\b
""", re.IGNORECASE | re.VERBOSE)

cpu_minimal_pattern = re.compile(r"""
\b
(?:Core\s*)?                        # Optional 'Core' keyword
(?P<family>i[3579]|Ryzen\s*[3579]) # CPU family: i3/i5/i7/i9 or Ryzen 3/5/7/9
(?:\s*Core)?                        # Optional 'Core' keyword after family
[\s-]?                              # Optional space or dash separator
(?P<model>\d{3,5})?                 # Optional CPU model number
(?P<suffix>[A-Za-z]{1,3})?          # Optional CPU suffix
\b
""", re.IGNORECASE | re.VERBOSE)

cpu_apple_pattern = re.compile(r"""
\b
(?:(?P<brand>Apple)\s*)?           # Optional brand 'Apple'
(?P<model>M\d\s*(?:Pro|Max|Ultra)?) # Model like M1, M2 Pro, M2 Max, etc.
\b
""", re.IGNORECASE | re.VERBOSE)

#====================================================================

cpu_brands = [
    "Intel",
    "AMD",
    "Apple"
]
cpu_series_pattern = re.compile(r"""
\b
(                       
    i[3579]            
    |Core\s+i[3579]     
    |Ryzen\s*[3579]    
    |M[1-9]             
    |M[1-9]\s*(Pro|Max|Ultra)? 
)
\b
""", re.IGNORECASE | re.VERBOSE)

cpu_model_suffix_pattern = re.compile(r"""
\b
(?:i[3579]|Ryzen\s*[3579])  
[\s-]*                      
(?P<model_suffix>\d{3,5}[A-Za-z]{0,3})? 
\b
""", re.IGNORECASE | re.VERBOSE)

# ================= RAM Regex Pattern =================

ram_pattern = re.compile(r"""
\b
(?:ram|pamięć\s+operacyjna)        # Mandatory RAM keyword (English/Polish)
\s*
(?:ddr[1-5])?                      # Optional DDR type (DDR1-DDR5)
\s*[: ]?\s*                        # Optional separator (colon or space)
(?:[1-9]|[1-5]\d|6[0-4])           # RAM size: 1-64 GB
\s*gb                              # GB keyword
\b
|
\b
(?:[1-9]|[1-5]\d|6[0-4])           # RAM size at the start
\s*gb
\s*
(?:ddr[1-5])?                      # Optional DDR type
\s*(?:ram|pamięć\s+operacyjna)     # Mandatory RAM keyword at the end
\b
""", re.IGNORECASE | re.VERBOSE)

# ================= Storage Regex Pattern =================

storage_pattern = re.compile(r"""
\b
(?:ssd|hdd|m\.2|nvme|sata|pamięć)  # Mandatory storage keyword
\s*[: ]?\s*                        # Optional separator (colon or space)
(?:[1-9][0-9]{0,3}|1[0-5][0-9]{3}|16[0-3][0-9]|163[0-8]) # Storage size: 1-16384
\s*(?:gb|tb)                       # Size unit: GB or TB
\b
|
\b
(?:[1-9][0-9]{0,3}|1[0-5][0-9]{3}|16[0-3][0-9]|163[0-8]) # Storage size at start
\s*(?:gb|tb)
\s*(?:ssd|hdd|m\.2|nvme|sata|pamięć) # Mandatory storage keyword at the end
\b
""", re.IGNORECASE | re.VERBOSE)

# ================= GPU Regex Pattern =================

gpu_brands = ["NVIDIA", "AMD", "Intel"]

gpu_series_pattern = re.compile(r"""
\b
(
    GeForce|GTX|RTX|Radeon|RX|Quadro|Vega|Iris|UHD|HD\s*Graphics
)
\b
""", re.IGNORECASE | re.VERBOSE)

gpu_model_suffix_pattern = re.compile(r"""
\b
(?:GeForce|GTX|RTX|Radeon|RX|Quadro|Vega|Iris|UHD|HD\s*Graphics)  
[\s-]*                                                          
(?P<model_suffix>\d{3,4}[A-Za-z]{0,2})?                        
\b
""", re.IGNORECASE | re.VERBOSE)
