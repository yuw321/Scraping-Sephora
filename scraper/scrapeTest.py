from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.sephora.com/product/brightening-eye-cream-hydrate-depuff-P438619?skuId=2452050&icid2=products%20grid:p438619:product").text
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

soup = BeautifulSoup(source,headers=headers)

print(soup.prettify())