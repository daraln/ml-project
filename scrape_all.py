import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import json

# Grid position spans 5:name, 7:team , 9:quali time

# LINK = ('https://en.mclarenf-1.com/2022/gp/s8973/lap_times/')
LINK = 'https://en.mclarenf-1.com/'
YEARS = {'2022': 8978}
RACES = {'2022': 22}

CATEGORIES = ['lapcharts', 'sector_times', 'results', 'grid', 'sector_speeds']
GRID = 'grid'
GRID_CLASS = 'grid-pos'

# SCRIPT_TAG = '(.*)var chart = am4core.createFromConfig\('
# SCRIPT_TAG = '(.*)data":'
SCRIPT_TAG = '(.*)data":(.*?)}, "chartdiv'

# 821 ver
# 833 lec

N = 'name'
T = 'team'
G = 'grid_position'
Q = 'quali_time'
ID = 'id'
S = 'short_name'
P = 'position'
LP = 'lap_position'
U = 'number'
C = 'chassis'
E = 'engine'
L = 'laps'
LN = 'lap'
LT = 'lap_time'
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
R = 'race'

GTL = 'gap_to_leader'
PT = 'pit_time'
TY = 'tyre'

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

    # race, lap num, name, team, engine, grid, quali time, lap position, gap, pit time, tyre, final position, points, race time, sector info
    # df = pd.DataFrame(columns=[R, LN, S, ID, N, T, E, G, Q, LP, GTL, PT, TY, ST, P, CT, PO, FS1, FS2, FS3, IDE, S1S, S2S, S3S])
    df = pd.DataFrame(columns=[R, LN, S, ID, T, E, G, Q, LP, LT, GTL, P, PO, FS1, FS2, FS3, IDE, S1S, S2S, S3S, ST, TY, PT])

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
                print(result)
                short_name = result[2][:3]
                if len(result) < 10:
                    continue
                r_data_for_drivers[short_name] = {S: short_name, P: result[0].replace('=', ''), U: result[1], C: result[4], E: result[5], L: result[7], TI: result[8], PO: result[9]}
            print(r_data_for_drivers)
            time.sleep(2)

            # # Sector times
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
                if short_name not in r_data_for_drivers:
                    continue
                r_data_for_drivers[short_name][FS1] = stime[6]
                r_data_for_drivers[short_name][FS2] = stime[7]
                r_data_for_drivers[short_name][FS3] = stime[8]
                r_data_for_drivers[short_name][IDE] = stime[9]
            time.sleep(2)

            # # Sector speeds
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
                if short_name not in r_data_for_drivers:
                    continue
                r_data_for_drivers[short_name][S1S] = speed[6]
                r_data_for_drivers[short_name][S2S] = speed[7]
                r_data_for_drivers[short_name][S3S] = speed[8]
                r_data_for_drivers[short_name][ST] = speed[9]
            print(r_data_for_drivers)
            print(json.dumps(r_data_for_drivers, indent=4))
            time.sleep(2)
            
            # Lap chart data
            lap_data = getDataJson(year, race_id, 'lapcharts')
            print(json.dumps(lap_data, indent=4))

            # Tyre data
            tyre_data = getDataJson(year, race_id, 'pit_summary')
            print(json.dumps(tyre_data, indent=4))

            # Get gp and grid
            # Grid
            print("\n\n\n\n\n\n")
            r = requests.get(race_link + GRID)
            html_grid = BeautifulSoup(r.text, 'html.parser')
            grand_prix = html_grid.find('a', {'class': ['nav-link active']})
            print(grand_prix)
            grand_prix = grand_prix.find('span').get_text()
            grid_table[grand_prix] = []
            grid = html_grid.findAll('div', {'class': GRID_CLASS})
            # Loop through grid positions
            for pos in grid:
                spans = pos.findAll('span')
                position = pos.find('div').get_text()
                # driver = spans[4].get_text()
                short = spans[1].get_text()
                if short not in r_data_for_drivers:
                    r_data_for_drivers[short] = {}
                    r_data_for_drivers[short][S] = short
                team = spans[6].get_text()
                quali_time = spans[8].get_text()
                driver_id = pos.find('span').get('data-id')
                # driver_id_table[driver_id] = driver
                # driver_id_table[driver] = driver_id
                # driver_details[short] = {'name': driver, I: driver_id, T: team, G: position}
                r_data_for_drivers[short][ID] = driver_id
                r_data_for_drivers[short][G] = position
                r_data_for_drivers[short][Q] = quali_time
                r_data_for_drivers[short][R] = grand_prix
                r_data_for_drivers[short][T] = team
                driver_id_table[driver_id] = short
                driver_id_table[short] = driver_id

            for driver in r_data_for_drivers:
                print(driver)
                print(r_data_for_drivers[driver])
                if ID not in r_data_for_drivers[driver]:
                    continue
                d_id = r_data_for_drivers[driver][ID]
                laps = {}

                r = requests.get(race_link + 'lap_times/' + d_id + '-' + d_id + '/')
                html_speed = BeautifulSoup(r.text, 'html.parser')
                table = html_speed.find('tbody')
                if table is None:
                    continue
                rows = table.findAll('tr')
                speeds = []
                for row in rows:
                    cols = row.findAll('td')
                    for col in cols:
                        for child in col.findAll("small"):
                            child.decompose()
                    cols = [e.text.strip() for e in cols]
                    speeds.append([e for e in cols if e])
                for speed in speeds:
                    if len(speed) < 2:
                        continue
                    la = speed[0]
                    # print(la)
                    # print(speed)
                    # print(r_data_for_drivers[driver])
                    r_data_for_drivers[driver][la] = speed[1]

                tyre = {}
                tyre[d_id] = ""
                for lap in tyre_data:
                    ln = lap['lap']
                    laps[ln] = {}
                    if d_id in lap:
                        laps[ln][LP] = lap[d_id]
                    else:
                        laps[ln][LP] = ""
                    if ln == 'Start':
                        pit = lap['tooltip']
                        if d_id in pit:
                            # print(pit)
                            pit = pit[d_id].split(' ')
                            if len(pit) == 5:
                                tyre[d_id] = pit[3] + pit[4]
                                
                    # print(laps)
                    # print(tyre)

                for lap in lap_data:
                    ln = lap['lap']
                    laps[ln][LN] = ln
                    laps[ln][GTL] = ""
                    if ln != "Start" and ln in r_data_for_drivers[driver]:
                        laps[ln][LT] = r_data_for_drivers[driver][ln]
                    else:
                        laps[ln][LT] = ""
                    pitTime = ""
                    if not tyre[d_id]:
                        laps[ln][PT] = ""
                        laps[ln][TY] = ""
                        continue
                    if d_id in lap:
                        laps[ln][GTL] = lap[d_id]
                        pit = lap['tooltip']
                        if d_id in pit:
                            pit = pit[d_id].split('<br>')
                            if len(pit) > 1:
                                pit = pit[1]
                                print(pit)
                                pit = pit.split(' ')
                                if len(pit) == 4:
                                    pitTime = pit[1].replace('s', '')
                                    pitTyre = pit[2] + pit[3]
                                    tyre[d_id] = pitTyre
                    laps[ln][PT] = pitTime
                    laps[ln][TY] = tyre[d_id]
                print(laps)


                # [R, LN, S, ID, N, T, E, G, Q, LP, LT, GTL, P, PO, FS1, FS2, FS3, IDE, S1S, S2S, S3S, ST])
                for lap, ld in laps.items():
                    d = r_data_for_drivers[driver]
                    print(ld)
                    race = d[R]
                    lap = ld['lap']
                    lap_time = ld[LT]
                    pit_time = ld[PT]
                    tyre = ld[TY]
                    lap_position = ld[LP]
                    gap_to_leader = ld[GTL]

                    team = d[T]
                    engine = d[E]
                    grid = d[G]
                    quali_time = d[Q]
                    position = d[P]
                    points = d[PO]

                    fs1 = d[FS1]
                    fs2 = d[FS2]
                    fs3 = d[FS3]
                    ide = d[IDE]
                    s1s = d[S1S]
                    s2s = d[S2S]
                    s3s = d[S3S]
                    st = d[ST]


                    df.loc[len(df.index)] = [race, lap, driver, d_id, team, engine, grid, quali_time, lap_position, lap_time, gap_to_leader, position, points, fs1, fs2, fs3, ide, s1s, s2s, s3s, st, tyre, pit_time]
                    # print(lap[PT], lap[TY], lap[GTL], lap[LT], lap[LP])

                
            time.sleep(3)

            df.to_csv('./' + grand_prix + '.csv', index=False)
            df.to_csv('./output.csv', index=False)

            # Don't spam requests
            time.sleep(3)




if __name__ == "__main__":
    main()
