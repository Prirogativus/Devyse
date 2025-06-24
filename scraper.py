from bs4 import BeautifulSoup
import requests
import re
import aiohttp
import asyncio


"""
This script serving to extract laptop data from the websites.
"""


html_page = "https://www.olx.pl/elektronika/komputery/laptopy/krakow/?page=1&search%5Border%5D=created_at%3Adesc"
headers = {
    "User-Agent": "Mozilla/5.0"  # This is a common user-agent string to mimic a browser request
} 

async def get_html_page(session, url: str):

    # Function to get HTML page from a given URL

    print("Getting HTML page...")

    async with session.get(url, headers=headers) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'lxml')

    print("HTML page retrieved.")

    return soup

async def get_pagination_numbers(session, url: str):
    
    soup =  await get_html_page(session, url)
    pagination = soup.find_all('a', class_ = "css-b6tdh7")
    print("Getting pagination numbers...")

    page_numbers = []

    for page in pagination:
        try:
            num = int(page.text.strip())
            page_numbers.append(num)
            print("Added page: ", num)
        except ValueError:
            continue

    print("Pagination numbers found.")

    return page_numbers

def get_ID_from_link(url: str):

    match = re.search(r"-ID([a-zA-Z0-9]+)\.html$", url)
    if match:
        id = match.group(1)
        return id

async def get_description(session, url: str):

    # Gets the desctiption of the Laptop from the given page

    soup = await get_html_page(session, url)
    description = soup.find('div', class_ = 'css-19duwlz').text
    return description    

async def get_listings(session, url: str):

    #Finds all listings on the given page 
    #Returns a list of dictionaries with laptop information and description

    soup = await get_html_page(session, url)
    devices = []

    print("Starting to scrape listings...")
    listings = soup.find_all('div', class_ = "css-l9drzq")
    outstanding_listings = soup.find_all('div', class_ = "css-l9drzq")
    listings += outstanding_listings

    for listing in listings:

        print("Working on listing...")

        link = 'https://www.olx.pl' + listing.find('a', class_ =  'css-1tqlkj0').get('href')

        laptop = {
            'marketplace_ID': get_ID_from_link(link),
            'title': listing.find('h4', class_ = 'css-1g61gc2').text,
            'price': listing.find('p', class_ = 'css-uj7mm0').text.strip(),
            'status': listing.find('span', class_ = 'css-iudov9').text,
            'location': listing.find('p', class_ = 'css-vbz67q').text,
            'link': link,
            'description': await get_description(session, link)
        }

        devices.append(laptop)
        
        print(f"marketplace_ID: {laptop['marketplace_ID']}, \n" 
              f"Laptop {laptop['title']} data: \n" 
              f"Price: {laptop['price']}, \n"
              f"Status: {laptop['status']}, \n"
              f"location: {laptop['location']}, \n"
              f"link: {laptop['link']}, \n"
              f"description: {laptop['description'][:300]}...\n\n\n")  # Print first 50 characters of description
        
    return devices

async def main():
 async with aiohttp.ClientSession() as session:
        page_numbers = await get_pagination_numbers(session, html_page)
        max_page = max(page_numbers)

        tasks = []
        for page in range(1, max_page + 1):
            url = html_page.replace("page=1", f"page={page}")
            tasks.append(get_listings(session, url))

        print(f"Scraping {max_page} pages asynchronously...")
        results = await asyncio.gather(*tasks)

        # Flatten the list of lists
        laptops = [item for sublist in results for item in sublist]

        print(f"Scraped {len(laptops)} laptops.")
        return laptops


if __name__ == "__main__":
    asyncio.run(main())