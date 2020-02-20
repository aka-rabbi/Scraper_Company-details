def emailCrawler(website,names):	
	from bs4 import BeautifulSoup
	import requests
	import requests.exceptions
	from urllib.parse import urlsplit
	from collections import deque
	import re


	# new_urls = deque(['https://ackerman.harvard.edu/'])
	new_urls = deque(['http:'+website+'/'])

	m_url=new_urls[0]
	print(m_url)
	processed_urls = set()

	emails = set()
	mail=[]
	m=''
	while len(new_urls):

		url = new_urls.popleft()
		processed_urls.add(url)
		parts = urlsplit(url)
		base_url = "{0.scheme}://{0.netloc}".format(parts)
		
		path = url[:url.rfind('/')+1] if '/' in parts.path else url

		print("Processing %s" % url)
		try:
			response = requests.get(url)
		except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
			print('set khaise')
			continue
		if (re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I)):
			for mail in re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I):
				for nam in names:
					if nam==re.search(r'[^@]*',mail).group():
						m=mail
		
		print(m)
		new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
		
		#print(new_emails)
		emails.update(new_emails)

		soup = BeautifulSoup(response.text,'lxml')
		
		for anchor in soup.find_all("a"):
			# print(anchor)
			link = anchor.attrs["href"] if "href" in anchor.attrs else ''
			link=re.findall(r'%s[^/]*' %m_url,link)[0] if re.findall(r'%s[^/]*' %m_url,link) else ''
			# print(l)
			if not link.startswith(m_url):
				continue
				
			if link.startswith('/'):
				link = base_url + link
			elif not link.startswith('http'):
				link = path + link
			
			if not link in new_urls and not link in processed_urls:
				new_urls.append(link)
	#return m
	print(names)