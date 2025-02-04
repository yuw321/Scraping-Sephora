import re
import time

import pandas as pd
from pygments import highlight
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

def get_data(product_link, px_list=None):
    #"""Get product information"""
    print('0%')
    data_dic = {'pd_link':product_link,'pd_name':[],'pd_id': [], 'pd_brand':[],'pd_category': [],
                'size_and_item': [],'price': [], 'love_count': [],
                'reviews_count': [],'rating':[],'highlights':[],'description':[],'ingredients':[]}
    px_idx = 0
    proxy = None if px_list is None else px_list[px_idx]
    print("10%")
    #while True:
    driver = webdriver.Chrome("/Users/testadmin/Desktop/Desktop/CS445/GitHub/Scraping-Sephora/scraper/chromedriver")
    
    #try:
    #response = requests.get(product_link, headers=headers,timeout=10)
    print('15%')
    #except:
        # if px_idx == len(px_list) - 1:
        #     px_idx = 0
        # else:
        #     px_idx += 1
        # proxy = px_list[px_idx]
        # continue
    print('20%')
    html = driver.get(product_link) #response.text
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #as of 02/18/22, class label for pd_name is css-1pgnl76 eanm77i0 
    data_dic['pd_name']= soup.find('span',attrs={'data-at':"product_name"}).text.strip()

    data_dic['pd_id'] = re.findall(R'P[0-9]{3,6}', product_link)[0]
    
    #as of 02/18/22, class label for pd_brand is css-1gyh3op e65zztl0
    data_dic['pd_brand']= soup.find('a',attrs={'data-at':"brand_name"}).text.strip()

    print('40%')
    try:
        data_dic['pd_category'] = soup.find(attrs={'data-comp':"ProductBreadCrumbs BreadCrumbs BreadCrumbs "}).text.strip()
    except:
        data_dic['pd_category'] = "location mismatch"
    # Size and Content
    try:
        size_and_item = soup.find('div',attrs={"data-at": "sku_name_label"}).get_text()
        #print(size_and_item)
    except:
        size_and_item = None

    # Get Price
    try:
        price = soup.find(attrs={'class':"css-1oz9qb"}).get_text()
        #print(price)
    except:
        price = None
    print('60%')

    # Get love counts
    try:
        love_count = soup.find( attrs={"class": "css-jk94q9"}).get_text()
        #print(love_count)
    except:
        love_count = None

    # review nums(unmodified)
    try:
        reviews_count = soup.find(attrs={"class": "css-1coslxg"}).get_text()
        #print(reviews_count)
    except:
        reviews_count = None

    #rating
    #as of 02/18/22, class label for ratings is css-1tbjoxk
    try:
        rating = soup.find(attrs={'class': 'css-1tbjoxk'})
        rating = rating['aria-label']
    except:
        rating = None
    
    #highlights
    #as of 02/18/22, class label for highlights is css-aiipho eanm77i0
    try:
        highlights = soup.find('div',attrs={'class':"css-16qu4bq eanm77i0"}).text
        #print(highlights)
    except:
        highlights = None
    
    #description
    #as of 02/18/22, class label for description is css-1h78hvu eanm77i0
    try:
        description = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/main/div[1]/div[6]/div[2]/div')
    except:
        try:
            description = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/main/div[1]/div[4]/div[2]/div')

        except:
            description = None
     

    #ingredients
    #as of 02/18/22, class label for ingredients is css-1ue8dmw eanm77i0
    try:
        ingredients = soup.find(attrs = {'id': 'ingredients'}).get_text()
        #print(ingredients)
    except:
        ingredients = None  
    print('80%')      

    data_dic['size_and_item'] = size_and_item
    data_dic['price'] = price
    data_dic['love_count'] = love_count
    data_dic['reviews_count'] = reviews_count
    data_dic['rating'] = rating
    data_dic['highlights'] = highlights
    if description!= None:
        data_dic['description'] = description.text
    else:
        data_dic['description'] = 'Location mismatch'
    data_dic['ingredients'] = ingredients
    print('90%')
    #break
    print('100%')
    return data_dic


#px_list_ = ['140.227.211.47:8080', '98.12.195.129:443','149.19.224.49:3128']
http_proxy  = "http://107.151.182.247:80"
https_proxy = "https://140.227.211.47:8080"
proxyDict = {
    "http"  : http_proxy, 
    "https" : https_proxy
}
pd_links_df = pd.read_csv('/Users/testadmin/Desktop/Desktop/CS445/GitHub/Scraping-Sephora/data/product_links.csv')
product_links = pd_links_df['product_links']#need to manually add "product_links" to cell A1 before running

result = []
for i, link in enumerate(product_links[:]):
    result.append(get_data(link))
    pd_df = pd.DataFrame(result)
    pd_df.to_csv('data/pd_info.csv', index=False)
    print(f'{i + 1:04d} / {len(product_links)} || {link}')


