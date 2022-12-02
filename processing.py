import pandas as pd
from datetime import datetime
import math


IN = './scraped_data/'
OUT = './processed_data/'

TIME_LAYOUT = ''

R = 'race'
LN = 'lap'
S = 'short_name'
ID = 'id'
T = 'team'
E = 'engine'
G = 'grid_position'
Q = 'quali_time'
LP = 'lap_position'
LT = 'lap_time'
GTL = 'gap_to_leader'
P = 'position'
PO = 'points'
FS1 = 'fastest_s1'
FS2 = 'fastest_s2'
FS3 = 'fastest_s3'
IDE = 'ideal_time'
S1S = 's1_speed'
S2S = 's2_speed'
S3S = 's3_speed'
ST = 'speed_trap'
PT = 'pit_time'
TY = 'tyre'
PTL = 'pit_this_lap'
TYN = 'tyre_num'
TA = 'tyre_age'
U = 'used'
NP = 'next_pit'
TOT = 'total_laps'
SOFT = 'soft'
MED = 'medium'
HARD = 'hard'
# APT = 'avg_pit_time'


def processPitData(df, tyref, pitf, lapsf):
    tyres = df.loc[:, tyref]
    laps = df.loc[:, lapsf]
    pitt = df.loc[:, pitf]
    pit_this_lap = [0] * len(laps)
    used = [0] * len(laps)
    tyre_num = [1] * len(laps)
    next_pit = [0] * len(laps)
    tyre_ages = [0] * len(laps)
    use_soft = [0] * len(laps)
    use_medium = [0] * len(laps)
    use_hard = [0] * len(laps)
    pit_times = [0] * len(laps)
    # current_tyre = None
    tyre_age = 0
    last_pit_index = 0

    for i in range(len(tyres)):
        lap = laps[i]
        tyre = tyres[i]
        pit = pitt[i]

        if "Soft" in tyre:
            tyre_num[i] = 1
            use_soft[i] = 1
        elif "Medium" in tyre:
            tyre_num[i] = 2
            use_medium[i] = 1
        elif "Hard" in tyre:
            tyre_num[i] = 3
            use_hard[i] = 1
        else:
            tyre_num[i] = 4

        if "used" in tyre:
            used[i] = 1

        if lap == 0:
            # current_tyre = tyre
            tyre_age = 0
            last_pit_index = i
        elif pit != 0:
            pit_this_lap[i] = 1
            pit_times[i+1] = pit
            # current_tyre = tyre
            tyre_age = 0

            for j in range(last_pit_index, i):
                next_pit[j] = lap
            last_pit_index = i
        else:
            tyre_age += 1
        tyre_ages[i] = tyre_age
    df[TYN] = tyre_num
    df[U] = used
    df[TA] = tyre_ages
    df[PTL] = pit_this_lap
    df[NP] = next_pit
    df[SOFT] = use_soft
    df[MED] = use_medium
    df[HARD] = use_hard
    df[PT] = pit_times


def processTimeField(df, field):
    times = df.loc[:, field]
    for i in range(len(times)):
        times[i] = toMs(times[i])
    df[field] = times


def processLaps(df, field):
    laps = df.loc[:, field]
    for i in range(len(laps)):
        if isinstance(laps[i], str) and laps[i] == 'Start':
            laps[i] = 0


def processLapPct(df, lap_field, tyre_age, next_pit):
    start_index = 0
    laps = df.loc[:, lap_field]
    tyre_ages = df.loc[:, tyre_age]
    next_pits = df.loc[:, next_pit]
    lap_pcts = [0] * len(laps)
    tyre_age_pcts = [0] * len(laps)
    next_pit_pcts = [0] * len(laps)
    total_laps = [0] * len(laps)
    for i in range(len(laps)):
        lap = laps[i]
        if lap == 0 and i > 0:
            max_laps = float(laps[i - 1])
            for j in range(start_index, i):
                lap_pcts[j] = float(laps[j]) / max_laps
                tyre_age_pcts[j] = float(tyre_ages[j]) / max_laps
                next_pit_pcts[j] = float(next_pits[j]) / max_laps
                total_laps[j] = max_laps
            start_index = i
    df[TOT] = total_laps
    df['lap_pcts'] = lap_pcts
    df['tyre_age_pct'] = tyre_age_pcts
    df['next_pit_pcts'] = next_pit_pcts

    for i in range(len(laps)):
        if isinstance(laps[i], str) and laps[i] == 'Start':
            laps[i] = 0


def processDist(df, race):
    distances = {
        'Bahrain': 5412,
        'Abu Dhabi': 5281,
        'Australian': 5278,
        'Austrian': 4318,
        'Belgian': 7004,
        'French': 5842,
        'Hungarian': 4381,
        'Mexican': 4304,
        'Miami': 5412,
        'Saudi Arabian': 6174
    }
    races = df.loc[:, race]
    lap_distances = [0] * len(races)
    for i in range(len(races)):
        lap_distances[i] = distances[races[i]]
    df['distances'] = lap_distances


def processPosition(df, pos):
    positions = df.loc[:, pos]
    to_drop = []
    for i in range(len(positions)):
        if positions[i] == "NC":
            to_drop.append(i)
            continue
        positions[i] = int(str(positions[i]).split(' ')[0])
    for i in to_drop:
        df.drop(i, axis=0, inplace=True)


def removeStartLaps(df, lap_field):
    laps = df.loc[:, lap_field]
    to_drop = []
    for i in range(len(laps)):
        if laps[i] == 0 or laps[i] == 1:
            to_drop.append(i)
    for i in to_drop:
        df.drop(i, axis=0, inplace=True)


def removeZeros(df, fields):
    for f in fields:
        field = df.loc[:, f]
        to_drop = []
        for i in range(len(field)):
            if field[i] == 0:
                to_drop.append(i)
        for i in to_drop:
            df.drop(i, axis=0, inplace=True)


def removeSCLaps(df, race, lap_field):
    race_names = {
        'Bahrain': [44, 45, 46, 47, 48, 49, 50, 51],
        'Abu Dhabi': [],
        'Australian': [3, 4, 5, 6, 23, 24, 25, 26, 39, 40],
        'Austrian': [57, 58, 59],
        'Belgian': [1, 2, 3, 4],
        'French': [18, 19, 20, 49, 50],
        'Hungarian': [2, 3, 66, 67, 68, 69],
        'Mexican': [],
        'Miami': [40, 41, 42, 43, 44, 45, 46],
        'Saudi Arabian': [16, 17, 18, 19, 20, 37, 38, 39, 40]
    }
    races = df.loc[:, race]
    laps = df.loc[:, lap_field]
    to_drop = []
    for i in range(len(races)):
        r = races[i]
        if laps[i] in race_names[r]:
            to_drop.append(i)
    for i in to_drop:
        df.drop(i, axis=0, inplace=True)


def toMs(item):
    if not isinstance(item, str) and math.isnan(item):
        return 0
    if not isinstance(item, str):
        return item
    a = datetime.strptime(item, '%M:%S.%f')
    return (a.minute * 60) + (a.second) + (a.microsecond / 1000000)


def removePitLaps(df):
    laps = df.loc[:, PTL]
    to_drop = []
    for i in range(len(laps)):
        if laps[i] == 1:
            to_drop.append(i)
            to_drop.append(i + 1)
    for i in to_drop:
        a, b = df.axes
        if i in a:
            print(i)
            df.drop(i, axis=0, inplace=True)


def main():

    # # Process individual races
    # df = pd.read_csv(IN + "austrian.csv")
    # processTimeField(df, LT)
    # processTimeField(df, Q)
    # processTimeField(df, GTL)
    # processTimeField(df, FS1)
    # processTimeField(df, FS2)
    # processTimeField(df, FS3)
    # processTimeField(df, IDE)
    # processTimeField(df, PT)
    # processLaps(df, LN)
    # processPitData(df, TY, PT, LN)
    # processLapPct(df, LN, TA, NP)
    # processDist(df, R)
    # print(df)
    # df.to_csv(OUT + "austrian.csv", index=False)

    # # Join all and remove bad rows
    df = pd.read_csv(OUT + "bahrain.csv")
    abu = pd.read_csv(OUT + "abu dhabi.csv")
    aus = pd.read_csv(OUT + "australian.csv")
    bel = pd.read_csv(OUT + "belgian.csv")
    fre = pd.read_csv(OUT + "french.csv")
    hun = pd.read_csv(OUT + "hungarian.csv")
    mex = pd.read_csv(OUT + "mexican.csv")
    mia = pd.read_csv(OUT + "miami.csv")
    sau = pd.read_csv(OUT + "saudi arabian.csv")
    aut = pd.read_csv(OUT + "austrian.csv")
    df = pd.concat([df, abu, aus, bel, fre, hun, mex, mia, sau, aut], ignore_index=True)
    df.to_csv(OUT + 'concat.csv')
    processPosition(df, P)
    df.reset_index(inplace=True, drop=True)
    df.to_csv(OUT + "temp.csv", index=False)
    df = pd.read_csv(OUT + "temp.csv")
    # removePitLaps(df)
    df.reset_index(inplace=True, drop=True)
    removeSCLaps(df, R, LN)
    df.reset_index(inplace=True, drop=True)
    removeStartLaps(df, LN)
    df.reset_index(inplace=True, drop=True)
    removeZeros(df, [LT])
    df.reset_index(inplace=True, drop=True)
    # df.to_csv(OUT + "race_data_no_sc.csv", index=False)

    # # df = pd.read_csv(OUT + "race_data_no_SC.csv")
    # df.reset_index(inplace=True, drop=True)
    # processPosition(df, P)
    # df.reset_index(inplace=True, drop=True)
    
    
    
    

    df.to_csv(OUT + "race_data_model_2.csv", index=False)



if __name__ == "__main__":
    main()
