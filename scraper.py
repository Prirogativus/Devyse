from bs4 import BeautifulSoup
import requests


first_html_page = "https://www.olx.pl/elektronika/komputery/laptopy/krakow/?search%5Bdist%5D=30&search%5Border%5D=created_at:desc"
regular_html_page ="https://www.olx.pl/elektronika/komputery/laptopy/krakow/?page=2&search%5Border%5D=created_at%3Adesc"



def get_pagination_numbers(html: str):
    html_page = requests.get(html).text
    soup = BeautifulSoup(html_page, 'lxml')
    pagination = soup.find_all('a', class_ = "css-b6tdh7")

    print("Getting pagination numbers...")
    page_numbers = []
    for page in pagination:
        try:
            num = int(page.text.strip())
            page_numbers.append(num)
        except ValueError:
            continue
    print("Pagination numbers found.")
    return page_numbers

def get_listings(html: str):
    html_page = requests.get(html).text
    soup = BeautifulSoup(html_page, 'lxml')

    devices = []

    print("Starting to scrape listings...")
    listings = soup.find_all('a', class_ = "css-b6tdh7")

    for listing in listings:
        print("Working on listing...")
        #link = 'https://www.olx.pl' + listing.find('a', class_ = 'css-1tqlkj0').get('href')
        #description_page = requests.get(link).text
        #soup = BeautifulSoup(description_page, 'lxml')
        #description = soup.find('div', class_ = 'css-19duwlz').text

        laptop = {
            'title': listing.find('h4', class_ = 'css-1g61gc2').text,
            'price': listing.find('p', class_ = 'css-uj7mm0').text,
            'status': listing.find('span', class_ = 'css-iudov9').text,
            'location': listing.find('p', class_ = 'css-vbz67q').text,
            'link': link,
            #'descrption': description
        }
        devices.append(laptop)
        print("Adding laptop: ", laptop['title'])
    return devices
    

def main():
    laptops = []
    for number in range(max(get_pagination_numbers(first_html_page))):
        page_number = number + 1
        print ("Working on page: ", page_number)
        laptops = laptops + get_listings(regular_html_page.replace('page=2', f'page={page_number}')) 
    print("Finished scraping laptops.")


if __name__ == "__main__":
    main()

# class="css-1g5933j" - listings class