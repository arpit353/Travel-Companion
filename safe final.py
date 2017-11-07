import os
import sys
import time
import wget

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


print "Opening Trip Advisor"

driver = webdriver.Firefox(executable_path=r'C:\Program Files\geckodriver.exe')

location = raw_input("Enter Location ")
#start_date = raw_input("Start Date")
#end_date = raw_input("End Date")

driver.get("https://www.tripadvisor.in/")
driver.find_element_by_xpath("//input[@tabindex='1']").clear()
driver.find_element_by_xpath("//input[@tabindex='1']").send_keys(location)
time.sleep(6)
# driver.find_element_by_xpath("//input[@tabindex='1']").send_keys(Keys.ENTER)
driver.find_element_by_xpath("//span[@class='picker-label target']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-20']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-25']").click()
time.sleep(6)
driver.find_element_by_xpath("//button[@tabindex='5']").click()

time.sleep(10)

print "Extracting Hotels Data"

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

size = 10 #remove this after demo

for j in range(1,size):
    tiles = soup(attrs={'class': 'prw_rup prw_meta_hsx_three_col_listing'})
    
    prices = soup(attrs={'class': 'priceBlock'}) 

    for i in range(0, len(tiles)):
        hotel_names.append(tiles[i].find_all("div",{"class","listing_title"})[0].find_all("a")[-1].text)    
        hotel_links.append(tiles[i].find_all("div",{"class","listing_title"})[0].a['href'])
        if len(tiles[i].find_all("div",{"class","priceBlock"})) > 0 :
            if str(tiles[i].find_all("div",{"class","priceBlock"})[0].find_all("div",{"class","price"})[0].text[2:]) == "" :
                hotel_price.append("Not Available")
            else:
                hotel_price.append(str(tiles[i].find_all("div",{"class","priceBlock"})[0].find_all("div",{"class","price"})[0].text[2:]))
        else:
            hotel_price.append("Not Available")
    
    print len(hotel_names)," ",len(hotel_links)," ",len(hotel_price)    
            
    driver.find_element_by_xpath("//a[@data-page-number='"+str(j+1)+"']").click();
    WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//span[@data-page-number='"+str(j+1)+"']")))
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    print j
    
time.sleep(10)

driver.find_element_by_xpath("//a[@id='global-nav-restaurants']").click();
time.sleep(10)
driver.find_element_by_xpath("//a[@id='global-nav-restaurants']").click();
print "Extracting Restaurants Data"
time.sleep(10)

src = driver.page_source
soup = BeautifulSoup(src, "lxml")

page_numbers = soup.find("div",{"class","pageNumbers"})
page_numbers.find_all('a')
last = page_numbers.find_all('a').pop()
size = int(last['data-page-number'])

restaurants_names = []
restaurants_links = []

size = 50 #remove this after demo

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

complete_hotel_data = []

print "Extracting Particular Hotel Data"
time.sleep(10)

for l in hotel_links:
    
    driver.get("https://www.tripadvisor.in"+l)
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    
    name = soup.find("h1",{"id":"HEADING"})
    print name.text
    
    locality = soup.find_all("span",{"class":"locality"})[0].text
    if(len(soup.find_all("span",{"class":"extended-address"})) > 0):
        extended_address = soup.find_all("span",{"class":"extended-address"})[0].text
    else:
        extended_address = "Not Available"
    #street_address = soup.find_all("span",{"class":"street-address"})[0].text
    
    #phone_number = str(soup.find_all("div",{"class":"blEntry phone"})[0].contents[1].text)
    
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
    
    page_length = 3    
    
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
        
        
    particular_hotel_data = [name,locality,extended_address,rank,outoff,rating,excellent,very_good,average,poor,terrible,reviews,reviews_head]
    
    complete_hotel_data.append(particular_hotel_data)
    
    
complete_restaurants_data = []

print "Extracting Particular Restaurants Data"
time.sleep(10)

for l in restaurants_links:
    driver.get("https://www.tripadvisor.in"+l)
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
    
    name = soup.find("h1",{"id":"HEADING"})
    print name.text
    
    locality = soup.find_all("span",{"class":"locality"})[0].text
    
    if( len(soup.find_all("span",{"class":"extended-address"})) >0):
        extended_address = soup.find_all("span",{"class":"extended-address"})[0].text
    else:
        extended_address = "Not available"
        
    if len(soup.find_all("span",{"class":"street-address"})) > 0:    
        street_address = soup.find_all("span",{"class":"street-address"})[0].text
    else:
        street_address = "Not available"

    if(len(soup.find_all("div",{"class":"blEntry phone"})) > 0):
        
        phone_number = str(soup.find_all("div",{"class":"blEntry phone"})[0].contents[1].text)
    
    else:
        phone_number = "Not available"
    
    outoff = str(soup.find_all("span",{"class":"header_popularity popIndexValidation"})[0].contents[1]
    )
    
    rank = str(soup.find_all("span",{"class":"header_popularity popIndexValidation"})[0].contents[0].contents[0].text[1:])
    
    rating  = str(soup.find_all("span",{"class":"overallRating"})[0].text)
    
    excellent = soup.find_all("li",{"data-idx":"5"})[0].find("span",{"class":"row_count row_cell"}).text
    very_good = soup.find_all("li",{"data-idx":"4"})[0].find("span",{"class":"row_count row_cell"}).text
    average = soup.find_all("li",{"data-idx":"3"})[0].find("span",{"class":"row_count row_cell"}).text
    poor = soup.find_all("li",{"data-idx":"2"})[0].find("span",{"class":"row_count row_cell"}).text
    terrible = soup.find_all("li",{"data-idx":"1"})[0].find("span",{"class":"row_count row_cell"}).text
    
    features = []
    
    cuisines = str(soup.find_all("div",{"class":"ui_icon restaurants"})[0].nextSibling.text)
    
    page_length = int(soup("div","pageNumbers")[0].find_all("span",{"class": "separator"})[0].nextSibling.text)
    
    reviews=[]
    reviews_head =[]

    page_length = 3    
    
    for i in range(0,page_length-1):    
    
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
        
    src = driver.page_source
    soup = BeautifulSoup(src, "lxml")
        
    for i in soup.find_all("span",{"class":"noQuotes"}):
        reviews.append(i.parent.parent.nextSibling.find_all("p",{"class":"partial_entry"})[0].text)
        reviews_head = reviews_head + soup.find_all("span",{"class","noQuotes"})

    
    particular_restaurants_data = [name,locality,extended_address,street_address,phone_number,rank,outoff,rating,excellent,very_good,average,poor,terrible,reviews,reviews_head,cuisines]
    
    complete_restaurants_data.append(particular_restaurants_data)
    
    



    




        
    
