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
print(driver_names[0])
#print(len(driver_names))
print(driver_names)

r = requests.get('https://en.mclarenf-1.com/2022/gp/s8978/lap_times/'+str(driver_code[0])+"-821/")
soup = BeautifulSoup(r.text, 'html.parser')
links = soup.findAll('tbody')
formatted_links = []
#print(links)
time = []
tyres = []
driver = []
end = 0
list = []
list = links
#print("List")
for link in list:
	for i in range(len(str(link))):
		if str(link)[i:i+4] == "time":
			for j in range(20):
				#print(str(link)[i+j:i+j+11])
				if str(link)[i+j:i+j+5] == "tire-":
					tyres.append(str(link)[i+j+5])
					print(tyres)
				if str(link)[i+20+j:i+20+j+9] == "data-sort":
					print(time)
					for k in range(12):
						if str(link)[i+31+j+k]=='"':
							end = k
							continue
					time.append(str(link)[i+31+j:i+31+j+end])
					if i = 0:
						driver.append(driver_names[0])
					#print(time)
					continue
#print(links)
#print(formatted_links)
print(time)
print(len(time))
print(len(driver))
print(len(tyres))
result = {
	"driver" : driver,
	"lap times" : time,
	"Tyres":tyres
}

df = pd.DataFrame(result)
df.to_csv("F1.csv")