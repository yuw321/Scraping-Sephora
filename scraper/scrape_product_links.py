import requests
from bs4 import BeautifulSoup
import pandas as pd


def scape_product(link, proxy=None):
    """
    A function to scape all the product links from a given brand link.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
    try:
        
        response = requests.get(link, proxies={
                                "http": proxy, "https": proxy}, timeout=15,headers=headers)
    except:
        print(f'\r Unsuccessfully get data for {link.split("/")[4]}', end="")
        return None
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        productLinkList = soup.find_all("a",attrs={"data-comp": "ProductTile "})
        productLinkListLazy = soup.find_all("a",attrs={"data-comp": "LazyLoad ProductTile "})
    # There might be no products for that brand
    except IndexError:
        return []
    
    product_link_lst = []
    loop =0
    for x in range(len(productLinkList)):
        # use function split to remove text like "grid p12345"
        productInfo = [productLinkList[x].find('span',attrs={"data-comp": "StyledComponent BaseComponent "}).text.strip()
                                                ,productLinkList[x]['href']]
        product_link_lst.append(productInfo)

    print(len(productLinkListLazy))
    for x in range(len(productLinkListLazy)):
        # use function split to remove text like "grid p12345"
        print(productLinkListLazy[x])

        #productInfo = [productLinkListLazy[x].find('span',attrs={"data-comp": "StyledComponent BaseComponent "}).text.strip()
        #                                        ,productLinkListLazy[x]['href']]
        #product_link_lst.append(productInfo)
        print("Number of products added")
        print(loop)
        loop+=1        
    return product_link_lst


# Read brand links file
product_link_dic = {'brand': [], 'product_links': []}
num_lines = sum(1 for line in open("data/brand_link.txt", "r"))

# Scape all the product links from all the brands links.
# This will take some time!
ct = 1

# Get proxies from http://www.freeproxylists.net/zh/?c=US&pr=HTTPS&u=80&s=ts
px = ['98.12.195.129:443', '140.227.211.47:8080', '45.42.177.72:3128']
px_idx = 0
brandCount =0
while brandCount <1:
    for brand_link in open("data/brand_link.txt", "r"):
        brand_name = brand_link.split('/')[4]
        brandCount+=1
        product_link_list = scape_product(brand_link[:-1], proxy=px[px_idx])
        brandCount+=1
        # If one proxy does not work, use another
        while product_link_list is None:
            px_idx += 1
            if px_idx == 3:
                px_idx = 0
            product_link_list = scape_product(brand_link[:-1], proxy=px[px_idx])

        print(f'\r === {ct} / {num_lines} ===  {brand_name} === {px[px_idx]}',
            end="")
        product_link_dic['brand'] += [brand_name] * len(product_link_list)
        product_link_dic['product_links'] += product_link_list
        ct += 1

# Write the result into csv file
product_link_df = pd.DataFrame(product_link_dic)
product_link_df.to_csv('data/product_links.csv', index=False)

# Indicate scraping completion
print(f'Got All product Links! There are {len(product_link_df)} products in '
      f'total.')
