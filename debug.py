from bs4 import BeautifulSoup 
import numpy as np
import re
import urllib.request
import time
from lxml import html
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

temp_url="https://www.allabolag.se/5590134747/we-sigtuna-ab"
# temp_url="https://www.allabolag.se/9164769193/tenton-handelsbolag"
temp_soup=BeautifulSoup(urllib.request.urlopen(temp_url).read(),'lxml') 

ibody=temp_soup('div',{"class":"company-info"})[0].find_all('p')
l1=[ele.get_text() for ele in ibody]
if l1:
	l1=l1[0].replace('\n','').strip().replace('            ',',')
	l1=re.findall(r'(\,[^/]*)',l1)[0].replace(',,','')
else:
	l1="N/A"
print(l1)