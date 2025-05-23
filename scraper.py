from bs4 import BeautifulSoup
import requests


html_page = requests.get("https://www.olx.pl/elektronika/komputery/laptopy/krakow/?search%5Bdist%5D=30&search%5Border%5D=created_at:desc").text
soup = BeautifulSoup(html_page, 'lxml')
listings = soup.find_all('div', class_ = 'css-1g5933j')
for listing in listings:
    link = 'https://www.olx.pl' + listing.find('a', class_ = 'css-1tqlkj0').get('href')
    description_page = requests.get(link).text
    soup = BeautifulSoup(description_page, 'lxml')
    description = soup.find('div', class_ = 'css-19duwlz').text
    laptop = {
        'title': listing.find('h4', class_ = 'css-1g61gc2').text,
        'price': listing.find('p', class_ = 'css-uj7mm0').text,
        'status': listing.find('span', class_ = 'css-iudov9').text,
        'location': listing.find('p', class_ = 'css-vbz67q').text,
        'link': link,
        'descrption': description
    }
    print(laptop)
    print('-----------------------------------')






    





# class="css-1g5933j" - listings class