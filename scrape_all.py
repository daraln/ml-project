import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import json

# Grid position spans 5:name, 7:team , 9:quali time

# LINK = ('https://en.mclarenf-1.com/2022/gp/s8973/lap_times/')
LINK = 'https://en.mclarenf-1.com/'
YEARS = {'2022': 8973}
RACES = {'2022': 22}

CATEGORIES = ['lapcharts', 'sector_times', 'results', 'grid', 'sector_speeds']
GRID = 'grid'
GRID_CLASS = 'grid-pos'

# SCRIPT_TAG = '(.*)var chart = am4core.createFromConfig\('
# SCRIPT_TAG = '(.*)data":'
SCRIPT_TAG = '(.*)data":(.*?)}, "chartdiv'

N = 'name'
T = 'team'
G = 'grid_position'
Q = 'quali_time'
D = 'id'
S = 'short_name'
P = 'position'
U = 'number'
C = 'chassis'
E = 'engine'
L = 'laps'
TI = 'time'
PO = 'points'
FS1 = 'fastest_s1'
FS2 = 'fastest_s2'
FS3 = 'fastest_s3'
IDE = 'ideal_time'
S1S = 's1_speed'
S2S = 's2_speed'
S3S = 's3_speed'
ST = 'speed_trap'

# def getIdFromValue(table, value, value_type):
#     for k, v in table.items():
#         if v[value_type] == name:
#             return k


def getDataJson(year, race, category, regex=SCRIPT_TAG):
    time.sleep(2)
    script_tag_regex = re.compile(regex, re.MULTILINE | re.DOTALL)
    link = LINK + year + '/gp/s' + str(race) + '/' + category
    r = requests.get(link)
    html_j = BeautifulSoup(r.text, 'html.parser')
    scripts = html_j.findAll('script')
    for script in scripts:
        if script_tag_regex.match(str(script.string)):
            data = script_tag_regex.match(str(script.string))
            data = data.groups()[1]
            return json.loads(data)


def main():

    driver_id_table = {}
    table = {}
    grid_table = {}
    # script_tag_regex = re.compile(SCRIPT_TAG + '(.*?)}, "chartdiv"', re.MULTILINE | re.DOTALL)
    # test = "\nvar chart = aslkdjlaksjd;"
    # if script_tag_regex.match(test):
    # # if re.match(SCRIPT_TAG, test, re.MULTILINE):
    #     print("success")
    #     exit(1)
    # else:
    #     exit(1)
    # print(script_tag_regex)

    # Loop through years
    for year, first_race_id in YEARS.items():
        link = LINK + year + '/gp/'

        # Loop through races
        for i in range(22):
            race_id = first_race_id + (i * 5)
            r_data_for_drivers = {}
            race_link = link + 's' + str(race_id) + '/'

            # Results
            r = requests.get(race_link + 'results')
            html_results = BeautifulSoup(r.text, 'html.parser')
            table = html_results.find('tbody')
            rows = table.findAll('tr')
            results = []
            for row in rows:
                cols = row.findAll('td')
                cols = [e.text.strip() for e in cols]
                results.append([e for e in cols if e])
            for result in results:
                short_name = result[2][:3]
                r_data_for_drivers[short_name] = {P: result[0].replace('=', ''), U: result[1], C: result[4], E: result[5], L: result[7], TI: result[8], PO: result[9]}
            print(r_data_for_drivers)
            time.sleep(2)

            # Sector times
            r = requests.get(race_link + 'sector_times')
            html_stimes = BeautifulSoup(r.text, 'html.parser')
            table = html_stimes.find('tbody')
            rows = table.findAll('tr')
            stimes = []
            for row in rows:
                cols = row.findAll('td')
                cols = [e.text.strip() for e in cols]
                stimes.append([e for e in cols if e])
            for stime in stimes:
                short_name = stime[1][:3]
                r_data_for_drivers[short_name][FS1] = stime[6]
                r_data_for_drivers[short_name][FS2] = stime[7]
                r_data_for_drivers[short_name][FS3] = stime[8]
                r_data_for_drivers[short_name][IDE] = stime[9]
            time.sleep(2)

            # Sector speeds
            r = requests.get(race_link + 'sector_speeds')
            html_speed = BeautifulSoup(r.text, 'html.parser')
            table = html_speed.find('tbody')
            rows = table.findAll('tr')
            speeds = []
            for row in rows:
                cols = row.findAll('td')
                cols = [e.text.strip() for e in cols]
                speeds.append([e for e in cols if e])
            for speed in speeds:
                short_name = speed[1][:3]
                r_data_for_drivers[short_name][S1S] = speed[6]
                r_data_for_drivers[short_name][S2S] = speed[7]
                r_data_for_drivers[short_name][S3S] = speed[8]
                r_data_for_drivers[short_name][ST] = speed[9]
            print(r_data_for_drivers)
            print(json.dumps(r_data_for_drivers, indent=4))
            time.sleep(2)

            # Grid
            r = requests.get(race_link + GRID)
            html_grid = BeautifulSoup(r.text, 'html.parser')
            
            # Lap chart data
            lap_data = getDataJson(year, race_id, 'lapcharts')
            print(json.dumps(lap_data, indent=4))

            time.sleep(2)

            # Get gp and grid
            # grand_prix = html_grid.find('a', {'class': 'active'})
            # grand_prix = grand_prix.find('span').get_text()
            # grid_table[grand_prix] = []
            # grid = html_grid.findAll('div', {'class': GRID_CLASS})
            # # Loop through grid positions
            # for pos in grid:
            #     spans = pos.findAll('span')
            #     position = pos.find('div').get_text()
            #     driver = spans[4].get_text()
            #     short = spans[1].get_text()
            #     team = spans[6].get_text()
            #     quali_time = spans[8].get_text()
            #     driver_id = pos.find('span').get('data-id')
            #     driver_id_table[driver_id] = driver
            #     driver_id_table[driver] = driver_id
            #     driver_details[short] = {'name': driver, I: driver_id, T: team}



            #     grid_table[grand_prix].append({P: position, D: driver, T: team, Q: quali_time})

            # lap_num = 0
            # lap_table = {}
            # for l in lap_data:
            #     lap_table[str(lap_num)] = {}
            #     for d in driver_table
            #         lap_table[str(lap_num)][d['id']]
            #     lap_num += 1
            # table[grand_prix] = 

            # Lap charts
            time.sleep(3)
            r = requests.get(race_link + 'lapcharts')



            # Don't spam requests
            time.sleep(3)




            # scripts = soup.findAll('script')
            # script_tag = re.compile(SCRIPT_TAG + '(.*?);')
            # for script in scripts:



if __name__ == "__main__":
    main()
