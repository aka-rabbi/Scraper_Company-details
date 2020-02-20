from bs4 import BeautifulSoup 
import emailCrawler
import numpy as np
import re
import urllib.request
import time
from lxml import html
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def Contact_person(soup,temp_soup):
	ibody=soup('div',{"box flex-grid__cell flex-grid__cell company-info"})[0].find('dd')
	i2body=soup('div',{"box flex-grid__cell flex-grid__cell company-info"})[0].find('dt')
	l1=[]
	l2=[]
	ibody=ibody.get_text()
	contact_person=ibody.strip()
	i2body=i2body.get_text()
	position=i2body.strip()
	position=position.replace("\n","")
	position=position.replace(" ","")
	position=position.replace(",","-")
	if position=="Bolagsform":
		ibody=temp_soup('div',{"class":"list--personnel__info"})[0]
		try:
			a=re.findall(r'(\s{2}\w+\s\w+\s\w+|\s{2}\w+\s\w+|\s{2}\w+\-\w+\s\w+)', str(ibody))
			#print(a)
			contact_person=a[0]						#######
			contact_person=contact_person.strip()
			l1=contact_person
			position=a[1]							#######
			position=position.strip()
			l2=position
		except IndexError:
			l1=None
			l2=None
	else:
		l2=position								########
		l1=contact_person
	# print(l1)
	# print(l2)
	
	return l1,l2

def Financial_stats(soup):
	l1=[]
	l2=[]
	l3=[]
	l4=[]
	try:
		test=soup('th',{"class":"company-table__pager-button-cell"})[0].find('div')
		test=re.findall(r'(\s\w+\b)',str(test))
		test=test[0]
		if test==" nyckeltal":
			ybody=soup('td',{"class":"number--positive data-pager__page data-pager__page--0"})[1] 
			hbody=soup('td',{"class":"number--positive data-pager__page data-pager__page--0"})[0]
			ybody=ybody.get_text()
			hbody=hbody.get_text()
			ant=hbody.strip()
			l2=ant												##########
			om_this_year=ybody.strip()
			l1=om_this_year
			
			ybody=soup('td',{"class":"number--positive data-pager__page data-pager__page--1"})[1]
			hbody=soup('td',{"class":"number--positive data-pager__page data-pager__page--1"})[0]
			ybody=ybody.get_text()
			hbody=hbody.get_text()
			ant=hbody.strip()
			l4=ant
			om_previous_year=ybody.strip()            							#########
			l3=om_previous_year
		
	except IndexError:
		l3=None
		l4=None
	return l1,l2,l3,l4

def Company_status(temp_soup,status_ref):
	branch=[]
	stat_temp=["N/A"]*len(status_ref)
	bbody=temp_soup('ul',{"class":"accordion-body"})
	branch=[ele.get_text() for ele in bbody]
	branch=branch[0].replace('\n','').strip()
	branch=re.sub(' +',' ',branch)
	# try:
		# ibody=temp_soup('dl',{"class":"accordion-body display-none"})[1].find_all('dd')
		# hbody=temp_soup('dl',{"class":"accordion-body display-none"})[1].find_all('dt')
		# hbody=[ele.text.strip() for ele in hbody]
		# status=[ele.text.strip() for ele in ibody]
		

		# for item in hbody:
			# if item in status_ref:
				# indexx=status_ref.index(item)
				# item_id=hbody.index(item)
				# stat_temp[indexx]=status[item_id]
		# l2=stat_temp
		# l2=[item.replace(",","-") for item in l2]

	# except IndexError:
		# ibody=temp_soup('dl',{"class":"accordion-body display-none"})[0].find_all('dd')
		# hbody=temp_soup('dl',{"class":"accordion-body display-none"})[0].find_all('dt')
		# rbody=temp_soup('dl',{"class":"accordion-body display-none"})[0].find_all('li')
		# hbody=[ele.text.strip() for ele in hbody]
		# status=[ele.text.strip() for ele in ibody]

		# for item in hbody:
				# if item in status_ref:
					# indexx=status_ref.index(item)
					# item_id=hbody.index(item)
					# stat_temp[indexx]=status[item_id]
		
		# l2=stat_temp
		# l2=[item.replace(",","-") for item in l2]
	ibody=temp_soup('dl',{"class":"accordion-body"})
	try:
		ibody=ibody[2].get_text().replace('\n',',').strip()
		l2=re.search(r'Status,([^,]*)',ibody).group(1)
		l3=re.search(r'Bolaget registrerat,([^,]*)',ibody).group(1)
		l4=re.search(r'F-Skatt,([^,]*)',ibody).group(1)
		l5=re.search(r'Moms,([^,]*)',ibody).group(1)
		l6=re.search(r'Bolagsform,,([^,]*)',ibody).group(1).strip()
		#l7=re.search(r'Moderbolag,,,([^,]*)',ibody).group(1).strip()
		l8=re.search(r'Länsäte,([^,]*)',ibody).group(1)
		l9=re.search(r'Kommunsäte,([^,]*)',ibody).group(1)

	except IndexError:
		ibody=ibody[1].get_text().replace('\n',',').strip()
		l2=re.search(r'Status,([^,]*)',ibody).group(1)
		l3=re.search(r'Bolaget registrerat,([^,]*)',ibody).group(1)
		l4=re.search(r'F-Skatt,([^,]*)',ibody).group(1)
		l5=re.search(r'Moms,([^,]*)',ibody).group(1)
		l6=re.search(r'Bolagsform,,([^,]*)',ibody).group(1).strip()
		#l7=re.search(r'Moderbolag,,,([^,]*)',ibody).group(1).strip()
		l8=re.search(r'Länsäte,([^,]*)',ibody).group(1)
		l9=re.search(r'Kommunsäte,([^,]*)',ibody).group(1)

	return l2,l3,l4,l5,l6,l8,l9,branch
# def Company_addresses(temp_soup):
	# ibody=temp_soup('div',{"class":"flex-grid__cell"})[4]
	# ibody=ibody.get_text()
	# ibody=ibody.replace(" ","")
	# address2=ibody.split()
	# l1=[]
	# l2=[]
	# l3=[]
	# if len(address2)==0:
		# ibody=temp_soup('div',{"class":"flex-grid__cell"})[3]
		# bbody=temp_soup('div',{"class":"flex-grid__cell"})[5]
		# ibody=ibody.get_text()
		# bbody=bbody.get_text()
		# ibody=ibody.replace(" ","")
		# address1=ibody.split()
		# del address1[0:2]
		# l1=address1

		# address2=['N/A','N/A','N/A']
		# l2=address2

		# bbody=bbody.replace(" ","")
		# address3=bbody.split()
		# del address3[0]
		# if len(address3)==3:
			# address3.append('N/A')
			# l3=address3
		# elif len(address3)==2:
			# address3.append('N/A','N/A')
			# l3=address3 
		# else:
			# l3=address3

		
		
	# else:
		
		# del address2[0]
		# l2=address2
		# abody=temp_soup('div',{"class":"flex-grid__cell"})[3]
		# bbody=temp_soup('div',{"class":"flex-grid__cell"})[5]
		
		# abody=abody.get_text()
		# abody=abody.replace(" ","")
		# address1=abody.split()

		# bbody=bbody.get_text()
		# bbody=bbody.replace(" ","")
		# address3=bbody.split()
		
		
		# if len(address1)==0:
			# l1=['N/A','N/A','N/A','N/A']
		# else:	
			# del address1[0:2]
			# l1=address1
		
		# if len(address3)==0:
			# l3=['N/A','N/A','N/A']
		# else:
			
			
			# del address3[0]
			# if len(address3)==3:
				# address3.append('N/A')
				# l3=address3
			# elif len(address3)==2:
				# address3.append('N/A','N/A')
				# l3=address3 	
			# else:
				# l3=address3
	# return l1,l2,l3
	# ibody=temp_soup('div',{"class":"company-info"})[0].find_all('p')
	# l1=[ele.get_text() for ele in ibody]
	# l1=l1[0].replace('\n','').strip().replace('            ',',')
	# l1=re.findall(r'(\,[^/]*)',l1)[0].replace(',,','')
	# return l1
	
def Fordon_count(temp_soup):
	l1=[]
	ibody=temp_soup('div',{"class":"flex-grid__cell flex-grid__cell--wide product-description"})[0].find('p')
	fordon=re.findall(r'(\d+\S|\s\d\s)',str(ibody))					#######
	l1=fordon
	return l1[0]





def AnalyzeData(url,url_trim,c_name,org_id,website):
	json_key = json.load(open('creds.json')) # json credentials you downloaded earlier
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
	file = gspread.authorize(credentials)
	global sheet
	sheet = file.open("test_sheet2").get_worksheet(0)
	print('got sheet')
	lenth=len(url)
	Org_id=org_id
	#print(org_id)
	#org_id=numpy.array(org_id)
	#emp=[" "]*len(url)
	#remark,c,org_id,o1,o2,s,add1,add2,add3,f,employee1,employee2=[None]*len(url)
	# for i in range(1,13):
		# obj['l'+str(i)]=[None]*len(url)
	c=[None]*len(url)
	br=[None]*len(url)
	p=[None]*len(url)
	remark=[None]*len(url)
	o1=[None]*len(url)
	o2=[None]*len(url)
	employee1=[None]*len(url)
	employee2=[None]*len(url)
	s=[None]*len(url)
	add1=[None]*len(url)
	# add2=[None]*len(url)
	# add3=[None]*len(url)
	f=[None]*len(url)
	phn=[None]*len(url)
	add_num=[None]*len(url)
	remark=[None]*len(url)
	C_name=c_name
	status_ref=['Status','Bolaget registrerat','F-Skatt','Anledning till avregistrering','Startdatum för F-Skatt','Slutdatum för F-Skatt','Moms','Startdatum för moms','Slutdatum för moms','Bolagsform','Moderbolag','Ägandeförhållande','Länsäte','Kommunsäte']
	
	for column in url:
		time.sleep(2)
		
		id=url.index(column)
		print(id)
		print(C_name[id])
		soup= BeautifulSoup(urllib.request.urlopen(column).read(),'lxml')
		try:	
			ibody=soup('a',{"p-tel"})[0]
			phn[id]=ibody.get_text()
		except IndexError:
			phn[id]="N/A"
		#print(ibody.get_text())
		
		try:	
			k="/"+str(org_id[id])+"/adresser"
			#print(k)
			ibody=soup('a',attrs={'href':k})[0]
			add_num[id]=re.findall(r'(\d+)',ibody.get_text())[0]
		except IndexError:
			add_num[id]="N/A"
			
		ibody=soup('div',{"class":"company-info"})[0].find_all('p')
		l1=[ele.get_text() for ele in ibody]
		if l1:
			l1=l1[0].replace('\n','').strip().replace('            ',',')
			add1[id]=re.findall(r'(\,[^/]*)',l1)[0].replace(',,','')
		else:
			add1[id]="N/A"
			
		try:
			ibody=soup('ul',{"remarks"})[0]
			remark[id]=ibody.get_text()
			print(remark[id])
		except IndexError:
			remark[id]="No remark"
		
		temp_url=url_trim[id]+"/befattningar"

		temp_soup=BeautifulSoup(urllib.request.urlopen(temp_url).read(),'lxml')
		
		c[id],p[id]=Contact_person(soup,temp_soup)
		nam=c[id].lower().split()
		nam.append(nam[0]+'.'+nam[-1])
		emailCrawler.emailCrawler(website[id],nam)
		
		o1[id],employee1[id],o2[id],employee2[id]=Financial_stats(soup)
		
		temp_url=url_trim[id]+"/verksamhet"
		temp_soup=BeautifulSoup(urllib.request.urlopen(temp_url).read(),'lxml') 
		s1,s2,s3,s4,s5,s7,s8,br[id]=Company_status(temp_soup,status_ref)
		

		# temp_url=url_trim[id]+"/adresser"
		# temp_soup=BeautifulSoup(urllib.request.urlopen(temp_url).read(),'lxml') 
		# add1[id]=Company_addresses(temp_soup)
		
		
		temp_url=url_trim[id]+"/fordon"
		temp_soup=BeautifulSoup(urllib.request.urlopen(temp_url).read(),'lxml') 
		f[id]=Fordon_count(temp_soup)
		
		# li=[str(C_name[id]),str(Org_id[id]),c[id],p[id],str(o1[id]),str(employee1[id]),str(o2[id]),str(employee2[id]),str(phn[id]),add1[id],str(add_num[id]),str(br[id]),str(remark[id]),f[id]]
		li=[s1,s2,s3,s4,s5,s7,s8,br[id]]
		sheet.append_row(li)
		if id==lenth-1:
			break
	# print(len(C_name))
	# print(len(org_id))
	# print(len(c))
	# print(len(org_id))
	# print(len(employee1))
	# print(len(employee2))
	# print(len(o1))
	# print(len(o2))
	# print(len(add1))
	# print(len(add2))
	# print(len(add3))
	# print(len(f))
	# print(len(remark))
	# print(len(s))
	list=np.column_stack((C_name,Org_id,c,p,phn,add_num,remark))
	#print(list)
	#list=numpy.vstack((header,list))

	return list
	
	
	
