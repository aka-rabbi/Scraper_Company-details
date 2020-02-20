def siteFinder(company):
	# from fake_useragent import UserAgent
	import re 		
	import json														
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from difflib import SequenceMatcher

	def similar(a, b):
		max=SequenceMatcher(None, a[0], b).ratio()
		url=a[0]
		for ele in a:
			if SequenceMatcher(None, ele, b).ratio()>max:
				max=SequenceMatcher(None, ele, b).ratio()
				url=ele
		
		if (url=='//www.facebook.com' or url== '//www.hitta.se'):
			url=''
		return max,url	
		#return SequenceMatcher(None, a, b).ratio()


	driver = webdriver.Chrome(r'C:\Users\chrome driver\chromedriver.exe')

	com=company
	driver.get('http://www.google.com')

	search=driver.find_element_by_name('q')
	search.send_keys(com)
	search.send_keys(Keys.RETURN)
	firstPage=driver.find_elements_by_css_selector(".r a")
	body=[]
	for elem in firstPage:
		temp=elem.get_attribute("href")
		body.append(re.search(r'//[^/]*',temp).group())

	search=driver.find_element_by_css_selector("#nav .fl")

	driver.get(search.get_attribute("href"))
	nextPage=driver.find_elements_by_css_selector(".r a")

	for elem in nextPage:
		temp=elem.get_attribute("href")
		body.append(re.search(r'//[^/]*',temp).group())

	ratio,url=similar(body,com)
	print(url)
	driver.quit()
	return url





