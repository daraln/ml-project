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

            # Grid
            race_link = link + 's' + str(race_id) + '/'
            r = requests.get(race_link + GRID)
            html_grid = BeautifulSoup(r.text, 'html.parser')
            
            # Lap chart data
            lap_data = getDataJson(year, race_id, 'lapcharts')
            print(json.dumps(lap_data, indent=4))
            
            time.sleep(2)

            # Get gp and grid
            grand_prix = html_grid.find('a', {'class': 'active'})
            grand_prix = grand_prix.find('span').get_text()
            grid_table[grand_prix] = []
            grid = html_grid.findAll('div', {'class': GRID_CLASS})
            # Loop through grid positions
            for pos in grid:
                spans = pos.findAll('span')
                position = pos.find('div').get_text()
                driver = spans[4].get_text()
                short = spans[1].get_text()
                team = spans[6].get_text()
                quali_time = spans[8].get_text()
                driver_id = pos.find('span').get('data-id')
                driver_id_table[driver_id] = driver
                driver_id_table[driver] = driver_id
                driver_details[short] = {'name': driver, I: driver_id, T: team}



                grid_table[grand_prix].append({P: position, D: driver, T: team, Q: quali_time})

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
