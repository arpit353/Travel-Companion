# The standard library modules
import os
import sys

# The wget module
import wget

# The BeautifulSoup module
from bs4 import BeautifulSoup

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(executable_path=r'C:\Program Files\geckodriver.exe')

driver.get("https://www.tripadvisor.in/Hotels-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Hotels.html")

src = driver.page_source

soup = BeautifulSoup(src, "lxml")

page_numbers = soup.find("pageNumbers")

page_numbers = soup.find("div",{"class","pageNumbers"})
page_numbers.find_all('a')
last = page_numbers.find_all('a').pop()
size = int(last['data-page-number'])

hotel_names = []
hotel_links = []
hotel_price = []

for j in range(1,size):
    tiles = soup(attrs={'class': 'prw_rup prw_meta_hsx_three_col_listing'})

    
    prices = soup(attrs={'class': 'priceBlock'}) 

    for i in range(0, len(tiles)):
        hotel_names.append(tiles[i].find_all("div",{"class","listing_title"})[0].find_all("a")[-1].text)    
        hotel_links.append(tiles[i].find_all("div",{"class","listing_title"})[0].a['href'])
        if len(tiles[i].find_all("div",{"class","priceBlock"})) > 0:         
            hotel_price.append(str(tiles[i].find_all("div",{"class","priceBlock"})[0].find_all("div",{"class","price"})[0].text[2:]))
        else:
            hotel_price.append("Not Available")
    
    print len(hotel_names)," ",len(hotel_links)," ",len(hotel_price)    
            
    driver.find_element_by_xpath("//a[@data-page-number='"+str(j+1)+"']").click();
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//span[@data-page-number='"+str(j+1)+"']")))
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    print j
        