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

driver.get("https://www.tripadvisor.in/")
driver.find_element_by_xpath("//input[@tabindex='1']").clear()
driver.find_element_by_xpath("//input[@tabindex='1']").send_keys("Paris")
time.sleep(6)
driver.find_element_by_xpath("//input[@tabindex='1']").send_keys(Keys.ENTER)
driver.find_element_by_xpath("//span[@class='picker-label target']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-20']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-25']").click()
time.sleep(6)
driver.find_element_by_xpath("//button[@tabindex='5']").click()

