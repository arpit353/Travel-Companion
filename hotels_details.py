# The standard library modules
import os
import sys

# The wget module
import wget
import time

# The BeautifulSoup module
from bs4 import BeautifulSoup

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox(executable_path=r'C:\Program Files\geckodriver.exe')
driver.get("https://www.tripadvisor.in/Hotel_Review-g187147-d188729-Reviews-Le_Bristol_Paris-Paris_Ile_de_France.html")
src = driver.page_source
soup = BeautifulSoup(src, "lxml")

name = soup.find("h1",{"id":"HEADING"})
print name.text

locality = soup.find_all("span",{"class":"locality"})[0].text
extended_address = soup.find_all("span",{"class":"extended-address"})[0].text
street_address = soup.find_all("span",{"class":"street-address"})[0].text

phone_number = str(soup.find_all("div",{"class":"blEntry phone"})[0].contents[1].text)

outoff = str(soup.find_all("span",{"class":"header_popularity popIndexValidation"})[0].contents[1]
)

rank = str(soup.find_all("span",{"class":"header_popularity popIndexValidation"})[0].contents[0].text[1:])

rating  = str(soup.find_all("span",{"class":"overallRating"})[0].text)

excellent = soup.find_all("li",{"data-idx":"5"})[0].find("span",{"class":"row_count row_cell"}).text
very_good = soup.find_all("li",{"data-idx":"4"})[0].find("span",{"class":"row_count row_cell"}).text
average = soup.find_all("li",{"data-idx":"3"})[0].find("span",{"class":"row_count row_cell"}).text
poor = soup.find_all("li",{"data-idx":"2"})[0].find("span",{"class":"row_count row_cell"}).text
terrible = soup.find_all("li",{"data-idx":"1"})[0].find("span",{"class":"row_count row_cell"}).text

features = []

#for i in soup.find_all("div",{"class","detailsMid"})[0]:
#   features.append(str(i.text))

page_length = int(soup("div","pageNumbers")[0].find_all("span",{"class": "separator"})[0].nextSibling.text)

reviews=[]
reviews_head =[]

for i in range(0,page_length):    

    time.sleep(2)
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='taLnk ulBlueLinks']")))
    driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()
    time.sleep(2)
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    
    for i in soup.find_all("span",{"class":"noQuotes"}):
        reviews.append(i.parent.parent.nextSibling.find_all("p",{"class":"partial_entry"})[0].text)
    
    reviews_head = reviews_head + soup.find_all("span",{"class","noQuotes"})
    time.sleep(1)
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='nav next taLnk ']")))    
    driver.find_element_by_xpath("//span[@class='nav next taLnk ']").click()
    print i
    



