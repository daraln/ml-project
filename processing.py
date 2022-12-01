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


def processTimeField(df, field):
    times = df.loc[:, field]
    for i in range(len(times)):
        times[i] = toMs(times[i])
    df[field] = times


def toMs(item):
    print(item)
    if not isinstance(item, str) and math.isnan(item):
        return 0
    if not isinstance(item, str):
        return item
    a = datetime.strptime(item, '%M:%S.%f')
    return (a.minute * 60) + (a.second) + (a.microsecond / 1000000)


df = pd.read_csv(IN + "bahrain.csv")
processTimeField(df, LT)
processTimeField(df, Q)
processTimeField(df, GTL)
processTimeField(df, FS1)
processTimeField(df, FS2)
processTimeField(df, FS3)
processTimeField(df, IDE)
processTimeField(df, PT)
print(df)

df.to_csv(OUT + "bahrain.csv", index=False)
