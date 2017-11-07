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

location = raw_input("Enter the destination Location ")
current  = raw_input("Enter current location ")
#start_date = raw_input("Start Date")
#end_date = raw_input("End Date")

driver.get("https://www.tripadvisor.in/")
driver.find_element_by_xpath("//input[@tabindex='1']").clear()
driver.find_element_by_xpath("//input[@tabindex='1']").send_keys(location)
time.sleep(3)
# driver.find_element_by_xpath("//input[@tabindex='1']").send_keys(Keys.ENTER)
driver.find_element_by_xpath("//span[@class='picker-label target ui_picker_arrow_target']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-20']").click()
driver.find_element_by_xpath("//span[@data-date='2017-10-25']").click()
time.sleep(2)
driver.find_element_by_xpath("//button[@tabindex='5']").click()

time.sleep(3)

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

size = 2 #remove this after demo

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
    
time.sleep(3)

driver.find_element_by_xpath("//a[@id='global-nav-restaurants']").click();
time.sleep(3)
driver.find_element_by_xpath("//a[@id='global-nav-restaurants']").click();
print "Extracting Restaurants Data"
time.sleep(3)

src = driver.page_source
soup = BeautifulSoup(src, "lxml")

page_numbers = soup.find("div",{"class","pageNumbers"})
page_numbers.find_all('a')
last = page_numbers.find_all('a').pop()
size = int(last['data-page-number'])

restaurants_names = []
restaurants_links = []

size = 2 #remove this after demo

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
time.sleep(3)

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
        
    if(len(soup.find_all("span",{"class":"ib_price price"})) > 0):
        price = int(soup.find_all("span",{"class":"ib_price price"})[0].text[2:].replace(",",""))
    else :
        price = 999999
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
    
    if( len(soup("div","pageNumbers")[0].find_all("span",{"class": "separator"})) >0 ):
        page_length = int(soup("div","pageNumbers")[0].find_all("span",{"class": "separator"})[0].nextSibling.text)
        page_length = 2 #remove this
    else:
        page_length = 1
        
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
        
        
    particular_hotel_data = [name,locality,extended_address,rank,outoff,rating,excellent,very_good,average,poor,terrible,reviews,reviews_head,price]
    
    complete_hotel_data.append(particular_hotel_data)
    
    
complete_restaurants_data = []

print "Extracting Particular Restaurants Data"
time.sleep(3)

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
    
    if(len(soup.find_all("div",{"class":"ui_icon restaurants"})) > 0):
        cuisines = str(soup.find_all("div",{"class":"ui_icon restaurants"})[0].nextSibling.text)
    else:
        cuisines = "Not Available"
    
    if( len(soup("div","pageNumbers")[0].find_all("span",{"class": "separator"})) >0 ):
        page_length = int(soup("div","pageNumbers")[0].find_all("span",{"class": "separator"})[0].nextSibling.text)
        page_length = 2 #remove this
    else:
        page_length = 1
        
    reviews=[]
    reviews_head =[]    
    
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
    
import csv

for i in complete_restaurants_data:
    write_row = [x.encode('utf-8') for x in i[13]]
    h_name = str(i[0].text.encode("utf-8")).replace("/","")
    
    with open("restaurants_reviews/"+h_name+".csv","w") as review_head:
        csv_writer = csv.writer(review_head)
        csv_writer.writerow(write_row)
        
for i in complete_restaurants_data:
    reviews_write = list(set(i[14]))
    write_row = [x.text.encode('utf-8') for x in reviews_write]
    h_name = str(i[0].text.encode("utf-8")).replace("/","")
    
    with open("restaurants_reviews_head/"+h_name+".csv","w") as review_head:
        csv_writer = csv.writer(review_head)
        csv_writer.writerow(write_row)
        
for i in complete_hotel_data:
    write_row = [x.encode('utf-8') for x in i[11]]
    h_name = str(i[0].text.encode("utf-8")).replace("/","")
    
    with open("hotels_reviews/"+h_name+".csv","w") as review_head:
        csv_writer = csv.writer(review_head)
        csv_writer.writerow(write_row)
        
for i in complete_hotel_data:
    reviews_write = list(set(i[12]))
    write_row = [x.encode('utf-8') for x in reviews_write]
    h_name = str(i[0].text.encode("utf-8")).replace("/","")
    
    with open("hotels_reviews_head/"+h_name+".csv","w") as review_head:
        csv_writer = csv.writer(review_head)
        csv_writer.writerow(write_row)
        
#for i in complete_hotel_data:
#    i[0] = i[0].text
    
for i in complete_restaurants_data:
    i[0] = i[0].text

for i in complete_hotel_data:
    write_row = [x.encode('utf-8') for x in i[0:10]]
    h_name = str(i[0].text.encode("utf-8")).replace("/","")
    
    with open("hotels_details/"+h_name+".csv","w") as hotels_details:
        csv_writer = csv.writer(hotels_details)
        csv_writer.writerow(write_row)
        
for i in complete_restaurants_data:
    write_row = [x.encode('utf-8') for x in i[0:12]]
    h_name = str(i[0].encode("utf-8")).replace("/","")
    
    with open("restaurants_details/"+h_name+".csv","w") as restaurants_details:
        csv_writer = csv.writer(restaurants_details)
        csv_writer.writerow(write_row)
  
from textblob import TextBlob

import glob

for i in glob.glob("hotels_reviews/*.csv"):
    print i
    with open(i,"r") as sample:
        csv_reader = csv.reader(sample)
        sentiment = 0
        confidence = 0
        for line in csv_reader:
            for item in line:
                nlpblob = TextBlob(item.decode('utf-8'))
                sentiment += nlpblob.sentiment[0]
                confidence += nlpblob.sentiment[1]
            append_sentiment =  sentiment/len(line)
            append_confidence = confidence/len(line)
        
    with open(i,"a") as write_sample:
        csv_writer = csv.writer(write_sample)
        s = []
        t = []
        s.append(append_sentiment)
        t.append(append_confidence)
        csv_writer.writerow(s)
        csv_writer.writerow(t)
        
for i in glob.glob("restaurants_reviews/*.csv"):
    print i
    with open(i,"r") as sample:
        csv_reader = csv.reader(sample)
        sentiment = 0
        confidence = 0
        for line in csv_reader:
            for item in line:
                nlpblob = TextBlob(item.decode('utf-8'))
                sentiment += nlpblob.sentiment[0]
                confidence += nlpblob.sentiment[1]
            append_sentiment =  sentiment/len(line)
            append_confidence = confidence/len(line)
        
    with open(i,"a") as write_sample:
        csv_writer = csv.writer(write_sample)
        s = []
        t = []
        s.append(append_sentiment)
        t.append(append_confidence)
        csv_writer.writerow(s)
        csv_writer.writerow(t)
        
for i in glob.glob("hotels_reviews_head/*.csv"):
    print i
    with open(i,"r") as sample:
        csv_reader = csv.reader(sample)
        sentiment = 0
        confidence = 0
        for line in csv_reader:
            for item in line:
                nlpblob = TextBlob(item.decode('utf-8'))
                sentiment += nlpblob.sentiment[0]
                confidence += nlpblob.sentiment[1]
            append_sentiment =  sentiment/len(line)
            append_confidence = confidence/len(line)
        
    with open(i,"a") as write_sample:
        csv_writer = csv.writer(write_sample)
        s = []
        t = []
        s.append(append_sentiment)
        t.append(append_confidence)
        csv_writer.writerow(s)
        csv_writer.writerow(t)
        
for i in glob.glob("restaurants_reviews_head/*.csv"):
    print i
    with open(i,"r") as sample:
        csv_reader = csv.reader(sample)
        sentiment = 0
        confidence = 0
        for line in csv_reader:
            for item in line:
                nlpblob = TextBlob(item.decode('utf-8'))
                sentiment += nlpblob.sentiment[0]
                confidence += nlpblob.sentiment[1]
            append_sentiment =  sentiment/len(line)
            append_confidence = confidence/len(line)
        
    with open(i,"a") as write_sample:
        csv_writer = csv.writer(write_sample)
        s = []
        t = []
        s.append(append_sentiment)
        t.append(append_confidence)
        csv_writer.writerow(s)
        csv_writer.writerow(t)


# sentiment analysis api
# use it after deleting all entries
# from aylienapiclient import textapi
# client = textapi.Client("bd80ddd1", "f73ad48645160c8a2fab07fb5d4ce904")
# sentiment = client.Sentiment({'text': 'John is a very good football player!'})
# sentiment
# sentiment['polarity']
# sentiment['polarity_confidence']

        
driver.get("https://www.tripadvisor.in/CheapFlightsHome")

driver.find_element_by_xpath("//input[@tabindex='4']").clear()
driver.find_element_by_xpath("//input[@tabindex='4']").send_keys(current)
time.sleep(6)
driver.find_element_by_xpath("//input[@tabindex='4']").send_keys(Keys.ENTER)
driver.find_element_by_xpath("//input[@tabindex='5']").clear()
driver.find_element_by_xpath("//input[@tabindex='5']").send_keys(location)
time.sleep(6)
driver.find_element_by_xpath("//input[@tabindex='5']").send_keys(Keys.ENTER)
time.sleep(6)
driver.find_element_by_xpath("//span[@class='picker-label target']").click()
driver.find_element_by_xpath("//span[@data-date='2017-11-15']").click()
time.sleep(3)
driver.find_element_by_xpath("//span[@data-date='2017-11-25']").click()
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
    
for i in range(0,len(airlines)):
    print airlines_name[i]
    print airports[i]
    print airplanes_prices[i]
    print "\n"

import glob

restaurants_reviews_rating = []
    
for i in glob.glob("restaurants_reviews/*.csv"):
    temp = []
    temp.append(i.split("\\")[1].split(".")[0])
    csv_path = i
    with open(csv_path, "rb") as f_obj:
        reader = csv.reader(f_obj)
        reader.next()
        temp.append(float(reader.next()[0]))
        temp.append(float(reader.next()[0]))
        restaurants_reviews_rating.append(temp)

hotels_reviews_rating = []
    
for i in glob.glob("hotels_reviews/*.csv"):
    temp = []
    temp.append(i.split("\\")[1].split(".")[0])
    csv_path = i
    with open(csv_path, "rb") as f_obj:
        reader = csv.reader(f_obj)
        reader.next()
        temp.append(float(reader.next()[0]))
        temp.append(float(reader.next()[0]))
        hotels_reviews_rating.append(temp)
        

hotels_reviews_head_rating = []
    
for i in glob.glob("hotels_reviews_head/*.csv"):
    temp = []
    temp.append(i.split("\\")[1].split(".")[0])
    csv_path = i
    with open(csv_path, "rb") as f_obj:
        reader = csv.reader(f_obj)
        reader.next()
        temp.append(float(reader.next()[0]))
        temp.append(float(reader.next()[0]))
        hotels_reviews_head_rating.append(temp)
        
restaurants_reviews_head_rating = []
    
for i in glob.glob("restaurants_reviews_head/*.csv"):
    temp = []
    temp.append(i.split("\\")[1].split(".")[0])
    csv_path = i
    with open(csv_path, "rb") as f_obj:
        reader = csv.reader(f_obj)
        reader.next()
        temp.append(float(reader.next()[0]))
        temp.append(float(reader.next()[0]))
        restaurants_reviews_head_rating.append(temp)
        
hotels_reviews_rating.sort(key = lambda hotels_reviews_rating : hotels_reviews_rating[1]*hotels_reviews_rating[2])
hotels_reviews_head_rating.sort(key = lambda hotels_reviews_head_rating : hotels_reviews_head_rating[1]*hotels_reviews_head_rating[2])
restaurants_reviews_rating.sort(key = lambda restaurants_reviews_rating : restaurants_reviews_rating[1]*restaurants_reviews_rating[2])
restaurants_reviews_head_rating.sort(key = lambda restaurants_reviews_head_rating : restaurants_reviews_head_rating[1]*restaurants_reviews_head_rating[2])

        
