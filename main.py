# from fake_useragent import UserAgent
import AnalyzeData
import json
import time
start_time=time.time()

with open('myJson.txt') as json_file: 
	data=json.load(json_file)
data_all=AnalyzeData.AnalyzeData(data['url'],data['url_trim'],data['company'],data['org'],data['website'])

print("--- %s seconds ---" % (time.time() - start_time))