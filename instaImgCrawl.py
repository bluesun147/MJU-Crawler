from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

baseUrl = 'https://www.instagram.com/explore/tags/'
#plusUrl = input('enter tag')
plusUrl = "java"
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome('C:\\Users\\blues\\Downloads\\chromedriver.exe')
driver.get(url)

time.sleep(3)

response = requests.get(url)

html = driver.page_source
soup = BeautifulSoup(html)

insta = soup.select('.v1Nh3.kIKUG._bz0w')

howmany = 5 # 포스트 몇개

n = 1
for i in insta:
    print('https://www.instagram.com' + i.a['href'])
    imgUrl = i.select_one('.KL4Bh').img['src']
    with urlopen(imgUrl) as f:
        with open('./img/' + plusUrl + str(n) + '.jpg', 'wb') as h:
            img = f.read()
            h.write(img)
    n += 1
    print(imgUrl)
    print()
    if n == howmany+1: break

driver.close()