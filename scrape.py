import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import fastf1
obj = pd.read_pickle(r'weather_data.ff1pkl')
print(obj)
for key in obj.items() :
    print(key)
#data = response = requests.get('https://ergast.com/api/f1/2022/1/racewinner')
#print(data)
'''
fastf1.Cache.enable_cache('cache')  # replace with your cache directory

session = fastf1.get_session(2021, 'Austrian Grand Prix', 'Q')
session.load()
lap = session.laps.pick_fastest()
tel = lap.get_telemetry()
print(tel)
x = tel.iloc[:1]
print(x)
x = np.array(tel['X'].values)
y = np.array(tel['Y'].values)

#print(x)

'''
'''

r = requests.get('https://en.mclarenf-1.com/2022/gp/s8978/lap_times/')
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.findAll('select')
formatted_links = []
#print(links)
names = []

for link in links:
	link = str(link)
	for i in range(len(str(link))):
		if str(link)[i:i+9] == "lap_times" and str(link)[i+10] != ">":
			formatted_links.append(str(link)[i+10:i+13])
			for j in range(20):
				if str(link)[i+23+j] == "<":
					names.append(str(link)[i+25:i+23+j])
					break
	#formatted_links.append(data)

driver_codes = []
driver_names = []
for item in formatted_links:
	if item not in driver_codes:
		driver_codes.append(item)
for item in names:
	if item not in driver_names and str(item)[-1]!=">":
		driver_names.append(item)
#print(len(driver_code))
print(driver_codes)
print(driver_names[0])
#print(len(driver_names))
print(driver_names)
print("length:")
print(len(driver_codes))
print(len(driver_names))
time = []
tyres = []
driver = []
for a in range(len(driver_codes)):
	r = requests.get('https://en.mclarenf-1.com/2022/gp/s8978/lap_times/'+str(driver_codes[a])+"-"+str(driver_codes[a])+"/")
	soup = BeautifulSoup(r.text, 'html.parser')
	links = soup.findAll('tbody')
	formatted_links = []
	time.append([])
	tyres.append([])
	driver.append([])
	#print(links)
	end = 0
	for link in links:
		link = str(link)
		for i in range(len(link)):
			if str(link)[i:i+4] == "time":
				for j in range(20):
					#print(str(link)[i+j:i+j+11])
					if str(link)[i+j:i+j+15] == "pe-4 tire tire-":
						tyres[a].append(str(link)[i+j+15])
						#print(tyres)
					if str(link)[i+20+j:i+20+j+9] == "data-sort":
						#print(time)
						for k in range(16):
							if str(link)[i+31+j+k]=='"':
								end = k
								continue
						time[a].append(str(link)[i+31+j:i+31+j+end])
						driver[a].append(driver_names[0])
						#print(time)
						continue

max = 0
for i in range(len(time)):
	if len(time[i]) >max:
		max = len(time[i])
print("max: "+str(max))
for i in range(max):
	for j in range(len(time)):
		if i >= len(time[j]):
			time[j].append("-")
			tyres[j].append("-")
#print(links)
#print(formatted_links)
#print(time)
#print(len(time))
for i in range(len(time)):
	print(len(time[i]))
#print(len(driver))
#print(len(tyres))
result = {}
for a in range(len(driver_codes)):
	result[str(driver_names[a])] = time[a]
	result["Tyres - "+str(driver_names[a])] = tyres[a]

#result = {
#	"driver" : driver,
#	"lap times" : time,
#	"Tyres":tyres
#}

df = pd.DataFrame(result)
df.to_csv("F1.csv")
'''
'''
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-bahrain-grand-prix.1ujvtAi6sFWLar32ibuX6m.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-saudi-arabian-grand-prix.3U71Mamk4Xb0hPHuZIJwLl.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-australian-grand-prix.5EtCYXM98LYF9b4EtO2DL6.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-italian-grand-prix.3c3QJWeUTK9AAqIlKM4zEC.html
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-miami-grand-prix.7JBlaDA20JNR4c6qpRxWGR.html
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-spanish-grand-prix.2yJS7kt9Kv3FrZszrMJgN0.html
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-monaco-grand-prix.Dq6DPWSxs3baxBGgels01.html#:~:text=The%20weather%20forecast%20shows%20that,for%20the%20race%20on%20Sunday.
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-azerbaijan-grand-prix.XUdDwVxWtY3dEFEFMybuh.html#:~:text=The%20weather%20forecast%20shows%20that,all%20three%20days%20of%20action.

no canadian gp
https://www.sportskeeda.com/f1/news-what-weather-forecast-2022-f1-canadian-gp
might as well just copy and paste the values of this site

https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-british-grand-prix.4DwRdZwmCdTM82vrpemvOs.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-austrian-grand-prix-and-sprint.2ZBrhuIRiTHxEDvuWoHaCE.html
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-french-grand-prix.2BljkeaEMS3obT4f4OApRQ.html
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-hungarian-grand-prix.33J29tarz7eungJEEiW6TU.html
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-belgian-grand-prix.4BLBEyugwjBggyXtOLhPzT.html#:~:text=2022%20Belgian%20Grand%20Prix%20weekend%20weather%20forecast&text=Conditions%3A%20Mostly%20cloudy%20day%20and%20also%20unsettled%20from%209am.
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-dutch-grand-prix.333HJKh1RrUBXiZayhXBk2.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-italian-grand-prix.3c3QJWeUTK9AAqIlKM4zEC.html#:~:text=2022%20Italian%20Grand%20Prix%20weekend%20weather%20forecast&text=Conditions%3A%20Cloudy%20with%20a%20significant,%2F%2F%20FP2%3A%2024%C2%B0C.
https://www.formula1.com/en/latest/article.what-is-the-weather-forecast-for-the-2022-singapore-grand-prix.2Lz4JauBL4yHeZ60bh7Hr.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-japanese-grand-prix.2WLsNjOrBOYLzoik6QaWXo.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-united-states-grand-prix.5xFPka5PlmcdqANDqET7kJ.html#:~:text=2022%20United%20States%20Grand%20Prix%20weekend%20weather%20forecast&text=Conditions%3A%20Hot%20and%20sunny%20throughout,around%2020%2D30km%2Fh.&text=Conditions%3A%20Very%20similar%20to%20Friday,to%20a%20north%20easterly%20direction.
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-mexico-city-grand-prix.5G3wz1RU5TUf9Zb7GRslWt.html#:~:text=2022%20Mexico%20City%20Grand%20Prix%20weekend%20weather%20forecast&text=Conditions%3A%20A%20partly%20cloudy%20morning,of%20rain%20in%20the%20afternoon.&text=Conditions%3A%20Sunny%20spells%20are%20expected,of%20rain%20during%20the%20race.
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-sao-paulo-grand-prix-and-sprint.6ga1mUvpAkYUnTUA3TTwrR.html
https://www.formula1.com/en/latest/article.whats-the-weather-forecast-for-the-2022-abu-dhabi-grand-prix.57vWzqWgy0ktCBCrBGY1pQ.html#:~:text=The%20weather%20forecast%20in%20Abu,expected%20over%20the%20race%20weekend.
'''
