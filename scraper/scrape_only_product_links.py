import requests
from bs4 import BeautifulSoup
print("finished import")
# Get Response of "brandlist" Website from Sephora
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
product_lst_link = "https://www.sephora.com/products-sitemap.xml"
response = requests.get(product_lst_link,headers=headers)

# Use BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Scraping brand links and save them into a list
prdct_link_lst = []
main_box = soup.find_all('url')

for x in range(len(main_box)):
    prdct_link_lst.append(main_box[x].find('loc').text)

# Write brand links into a file:
with open('data/product_links.csv', 'w') as f:
    for item in prdct_link_lst:
        f.write(f"{item}\n")

# Indicate scraping completion
print(f'Got All product Links! There are {len(prdct_link_lst)} products in total.')
