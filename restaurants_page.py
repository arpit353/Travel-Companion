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

driver.get("https://www.tripadvisor.in/Restaurants-g304551-New_Delhi_National_Capital_Territory_of_Delhi.html")

src = driver.page_source
soup = BeautifulSoup(src, "lxml")

page_numbers = soup.find("div",{"class","pageNumbers"})
page_numbers.find_all('a')
last = page_numbers.find_all('a').pop()
size = int(last['data-page-number'])

restaurants_names = []
restaurants_links = []
restaurants_price = []

for j in range(1,size):
    
    tiles = soup.find_all("a",{"class":"property_title"})
     
    for i in range(0, len(tiles)):
        restaurants_names.append(tiles[i].text)    
        restaurants_links.append(tiles[i]['href'])
            
    driver.find_element_by_xpath("//a[@data-page-number='"+str(j+1)+"']").click();
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//span[@data-page-number='"+str(j+1)+"']")))
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    print j
        