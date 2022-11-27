import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('https://en.mclarenf-1.com/2022/gp/s8978/lap_times/')
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.findAll('select')
formatted_links = []
#print(links)
names = []

for link in links:
	for i in range(len(str(link))):
		if str(link)[i:i+9] == "lap_times" and str(link)[i+10] != ">":
			formatted_links.append(str(link)[i+10:i+13])
			for j in range(20):
				if str(link)[i+23+j] == "<":
					names.append(str(link)[i+25:i+23+j])
					break
	#formatted_links.append(data)

driver_code = []
driver_names = []
for item in formatted_links:
	if item not in driver_code:
		driver_code.append(item)
for item in names:
	if item not in driver_names and str(item)[-1]!=">":
		driver_names.append(item)
#print(len(driver_code))
print(driver_code)
#print(len(driver_names))
print(driver_names)

r = requests.get('https://en.mclarenf-1.com/2022/gp/s8978/lap_times/'+str(driver_code[0])+"-821/")
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tbody')
formatted_links = []
#print(links)
time = []
end = 0
for link in links:
	for i in range(len(str(link))):
		if str(link)[i:i+4] == "time":
			for j in range(20):
				if str(link)[i+20+j:i+20+j+9] == "data-sort":
					#print(time)
					for k in range(12):
						if str(link)[i+31+j+k]=='"':
							end = k
							break
					time.append(str(link)[i+31+j:i+31+j+end])
					break
#print(links)
#print(formatted_links)
print(time)

#df = pd.DataFrame(lst)
#df.to_csv("F1.csv")