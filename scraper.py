from bs4 import BeautifulSoup
import requests
import re


"""
This script serving to extract laptop data from the websites.
"""


html_page ="https://www.olx.pl/elektronika/komputery/laptopy/krakow/?page=1&search%5Border%5D=created_at%3Adesc"


def get_pagination_numbers(html: str):
    
    soup = get_html_page(html)
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

def get_listings(html: str):

    #Finds all listings on the given page 
    #Returns a list of dictionaries with laptop information and description

    soup = get_html_page(html)
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
            'description': get_description(link)
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

def get_ID_from_link(url: str):

    match = re.search(r'ID([a-zA-Z0-9]+)', url)
    if match:
        id = match.group(1)
        return id

def get_description(url: str):

    # Gets the desctiption of the Laptop from the given page

    soup = get_html_page(url)
    description = soup.find('div', class_ = 'css-19duwlz').text
    return description

def get_html_page(url: str):

    # Function to get HTML page from a given URL

    print("Getting HTML page...")

    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, 'lxml')

    print("HTML page retrieved.")

    return soup
    

def main():
    laptops = []
    for number in range(max(get_pagination_numbers(html_page))):
        page_number = number + 1
        print (f"Page: {page_number}\n")
        laptops = laptops + get_listings(html_page.replace('page=1', f'page={page_number}')) 
    print("Finished scraping laptops.")
    return laptops


if __name__ == "__main__":
    main()