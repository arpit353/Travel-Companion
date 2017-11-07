# The standard library modules
import os
import sys
import time
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

driver.get("https://www.tripadvisor.in/CheapFlightsHome")

driver.find_element_by_xpath("//input[@tabindex='4']").clear()
driver.find_element_by_xpath("//input[@tabindex='4']").send_keys("Mumbai")
time.sleep(6)
driver.find_element_by_xpath("//input[@tabindex='4']").send_keys(Keys.ENTER)
driver.find_element_by_xpath("//input[@tabindex='5']").send_keys("Paris")
time.sleep(6)
driver.find_element_by_xpath("//input[@tabindex='5']").send_keys(Keys.ENTER)
time.sleep(6)
driver.find_element_by_xpath("//span[@class='picker-label target']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-15']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-25']").click()
time.sleep(6)
driver.find_element_by_xpath("//button[@tabindex='9']").click()
driver.switch_to_window(driver.window_handles[1])

WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='awEmail']")))

driver.find_element_by_xpath("//input[@id='awEmail']").click();
driver.find_element_by_xpath("//input[@id='awEmail']").send_keys("hello@world.com")
driver.find_element_by_xpath("//div[@class='create-alert-btn']").click()

src = driver.page_source
soup = BeautifulSoup(src, "lxml")

airlines = soup.find_all("div",{"class":"mainFlightInfo"})
airlines_number = len(airlines)

airlines_name = []

for i in range(0,airlines_number):
    names = airlines[i].find_all("div",{"class","airlineName"})

    temp_name = []    
    
    for j in names :
        temp_name.append(str(j.text))
        
    airlines_name.append(temp_name)
    
    
airports = []

for i in range(0,airlines_number):    
    
    depart = soup.find_all("div",{"class":"segments"})[i].find_all("div",{"class":"departureDescription airportDescription"})
    arrival = soup.find_all("div",{"class":"segments"})[i].find_all("div",{"class":"arrivalDescription airportDescription"})

    depart_airports = []
    arrival_airports = []    
    
    for j in depart:
        depart_airports.append(str(j.text))
        
    for j in arrival:
        arrival_airports.append(str(j.text))
        
    current_airports = [depart_airports,arrival_airports]
    
    airports.append(current_airports)
    
airplanes_prices = []

prices  = soup.find_all("span",{"class","viewDealPrice"})

for i in prices:
    airplanes_prices.append(i.text[2:])
    
