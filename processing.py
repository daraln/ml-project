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
    # current_tyre = None
    tyre_age = 0
    last_pit_index = 0

    for i in range(len(tyres)):
        lap = laps[i]
        tyre = tyres[i]
        pit = pitt[i]

        if "Soft" in tyre:
            tyre_num[i] = 1
        elif "Medium" in tyre:
            tyre_num[i] = 2
        elif "Hard" in tyre:
            tyre_num[i] = 3
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


def toMs(item):
    if not isinstance(item, str) and math.isnan(item):
        return 0
    if not isinstance(item, str):
        return item
    a = datetime.strptime(item, '%M:%S.%f')
    return (a.minute * 60) + (a.second) + (a.microsecond / 1000000)


def main():
    df = pd.read_csv(IN + "bahrain.csv")
    processTimeField(df, LT)
    processTimeField(df, Q)
    processTimeField(df, GTL)
    processTimeField(df, FS1)
    processTimeField(df, FS2)
    processTimeField(df, FS3)
    processTimeField(df, IDE)
    processTimeField(df, PT)
    processLaps(df, LN)
    processPitData(df, TY, PT, LN)
    print(df)

    df.to_csv(OUT + "bahrain.csv", index=False)


if __name__ == "__main__":
    main()
