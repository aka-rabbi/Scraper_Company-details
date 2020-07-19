# from fake_useragent import UserAgent
import siteFinder
import numpy as np
import re 		
import json									
from lxml import html
import urllib.request   							
from bs4 import BeautifulSoup  
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

start_time=time.time()
# options=webdriver.ChromeOptions()
# options.add_argument(r'--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(r'C:\Users\chrome driver\chromedriver.exe')
driver.get('https://www.allabolag.se/what/ytt')
# driver.get('https://www.allabolag.se/what/youth')
pbody=driver.find_element_by_css_selector(".font-weight--normal")
page=re.findall(r'(\d{1,4}\b)',str(pbody.text)) 
page_count= np.ceil(int(page[0])/20)
SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	time.sleep(SCROLL_PAUSE_TIME)

	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
		print("breaking")
		break
	last_height = new_height
tbody=driver.find_elements_by_css_selector(".search-results__item__title a")
url_allabolag=[]
url_allabolag_id=[]
company_name=[]
website=[]
for elem in tbody:
	body=elem.get_attribute("href")
	company_name.append(elem.text)
	website.append(siteFinder.siteFinder(elem.text))
	
	url_allabolag.append(body)
	print(url_allabolag)
	url_allabolag_id.append(re.findall(r'(https://www.allabolag.se/\d+[^/]*)',body)[0])

org_id=re.findall(r'(\d+[^\']*)',str(url_allabolag_id))
with open('myJson.txt', 'w') as outfile:
	json.dump({'url':url_allabolag,'url_trim':url_allabolag_id,'company':company_name,'org':org_id,'website':website},outfile)



