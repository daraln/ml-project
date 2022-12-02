import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import math
import statistics

df = pd.read_csv( "fixedpits.csv" )
print( df . head ( ) )

compound = [[1,1,1,0,0],
[0,0,1,1,1],
[0,1,1,0,1],
[0,1,1,1,0],
[0,1,1,1,0],
[0,1,1,1,0],
[0,1,1,1,0],
[0,1,1,1,0],
[0,1,1,1,0]]





'''
race = df.loc[:,race]
lap	= df.loc[:,lap]
short_name = df.loc[:,short_name]
id = df.loc[:,id]
team = df.loc[:,team]
engine = df.loc[:,engine]
grid_position = df.loc[:,grid_position]
quali_time = df.loc[:,quali_time]
lap_position = df.loc[:,lap_position]
lap_time = df.loc[:,lap_time]
gap_to_leader = df.loc[:,gap_to_leader]
position = df.loc[:,position]
points = df.loc[:,points]
fastest_s1 = df.loc[:,fastest_s1]
fastest_s2 = df.loc[:,fastest_s2]
fastest_s3 = df.loc[:,fastest_s3]
ideal_time = df.loc[:,ideal_time]
s1_speed = df.loc[:,s1_speed]
s2_speed = df.loc[:,s2_speed]
s3_speed = df.loc[:,s3_speed]
speed_trap = df.loc[:,speed_trap]
#tyre = df.loc[:,tyre]
soft = df.loc[:,soft]
medium = df.loc[:,medium]
hard= df.loc[:,hard]
pit_time = df.loc[:,pit_time]
tyre_num = df.loc[:, tyre_num]
used = df.loc[:, used]
tyre_age = df.loc[:, tyre_age]
pit_this_lap = df.loc[:, pit_this_lap]
next_pit = df.loc[:, next_pit]
total_laps = df.loc[:, total_laps]
lap_pcts = df.loc[:, lap_pcts]
tyre_age_pct = df.loc[:, tyre_age_pct]
next_pit_pcts = df.loc[:, next_pit_pcts]
distances = df.loc[:, distances]
'''
race = df.iloc[:,0]
lap	= df.iloc[:,1]
short_name = df.iloc[:,2]
id = df.iloc[:,3]
team = df.iloc[:,4]
engine = df.iloc[:,5]
grid_position = df.iloc[:,6]
quali_time = df.iloc[:,7]
lap_position = df.iloc[:,8]
lap_time = df.iloc[:,9]
gap_to_leader = df.iloc[:,10]
position = df.iloc[:,11]
points = df.iloc[:,12]
fastest_s1 = df.iloc[:,13]
fastest_s2 = df.iloc[:,14]
fastest_s3 = df.iloc[:,15]
ideal_time = df.iloc[:,16]
s1_speed = df.iloc[:,17]
s2_speed = df.iloc[:,18]
s3_speed = df.iloc[:,19]
speed_trap = df.iloc[:,20]
tyre = df.iloc[:,21]
pit_time = df.iloc[:,22]
tyre_num = df.iloc[:, 23]
used = df.iloc[:, 24]
tyre_age = df.iloc[:, 25]
pit_this_lap = df.iloc[:, 26]
next_pit = df.iloc[:, 27]
total_laps = df.iloc[:, 28]
lap_pcts = df.iloc[:, 29]
tyre_age_pct = df.iloc[:, 30]
next_pit_pcts = df.iloc[:, 31]
distances = df.iloc[:, 32]
soft=df.iloc[:, 33]
medium=df.iloc[:, 34]
hard=df.iloc[:, 35]
c1=df.iloc[:, 36]
c2=df.iloc[:, 37]
c3=df.iloc[:, 38]
c4=df.iloc[:, 39]
c5=df.iloc[:, 40]

for i in range(len(soft)):
    if hard[i] == 1:
        if c5[i] == 1:
            c1[i] = 0
            c2[i] = 0
            c3[i] = 0
            c4[i] = 0
        if c5[i] == 0 and c4[i]==1:
            c1[i] = 0
            c2[i] = 0
            c3[i] = 0
            c5[i] = 0
        if c5[i] == 0 and c4[i]==0 and c3[i] == 1:
            c1[i] = 0
            c2[i] = 0
            c3[i] = 0
            c5[i] = 0
    if soft[i] == 1:
        if c1[i] == 1:
            c5[i] = 0
            c2[i] = 0
            c3[i] = 0
            c4[i] = 0
        if c1[i] == 0 and c2[i]==1:
            c1[i] = 0
            c4[i] = 0
            c3[i] = 0
            c5[i] = 0
        if c1[i] == 0 and c2[i]==0 and c3[i] == 1:
            c1[i] = 0
            c2[i] = 0
            c4[i] = 0
            c5[i] = 0
    if medium[i] == 1:
        if c5[i] == 1 and c4[i] == 1:
            c1[i] = 0
            c2[i] = 0
            c3[i] = 0
            c5[i] = 0
        if c5[i] == 0 and c4[i]==1 and c3[i] == 1:
            c1[i] = 0
            c2[i] = 0
            c4[i] = 0
            c5[i] = 0
        if c5[i] == 0 and c4[i]==0 and c3[i] == 1 and c2[i] == 1:
            c1[i] = 0
            c4[i] = 0
            c3[i] = 0
            c5[i] = 0


'''
soft=[]
medium=[]
hard=[]
for i in range(len(tyre)):
    if tyre[i][0:4]=="Soft":
        soft.append(1)
        medium.append(0)
        hard.append(0)
    if tyre[i][0:6]=="Medium":
        soft.append(0)
        medium.append(1)
        hard.append(0)
    if tyre[i][0:4]=="Hard":
        soft.append(0)
        medium.append(0)
        hard.append(1)
'''
min = []

for i in range(len(race)):
    j = -1
    if i==0:
        min.append(999)
        j+1
    if i>0:
        if race[i] != race[i - 1]:
            min.append(999)
            j+1
    if min[j]>lap_time[i]:
        min[j] = lap_time[i]
lap_time_norm = []
for i in range(len(lap_time)):
    j = -1
    if i==0:
        j+1
    if i>0:
        if race[i] != race[i - 1]:
            j+1
    lap_time_norm.append(lap_time[i]/min[j])

#X=np.column_stack( ( quali_time, gap_to_leader, speed_trap, soft,medium,hard, lap_pcts, lap,pit_time, tyre_age,total_laps,distances,next_pit ) )
#X=np.column_stack( ( soft,medium,hard,tyre_age_pct ,lap_pcts,quali_time, pit_time) )#features
X=np.column_stack( ( c1,c2,c3,c4,c5,tyre_age_pct ,lap_pcts,quali_time, pit_time) )
y = lap_time
#y = lap_time_norm

from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import PolynomialFeatures
'''
n_range = [1]
C_range = [25]#[0.05, 0.1, 1,2,3,4,5,10,25,50,75,100]
num_splits = 5
for C in C_range:
    mean = []
    standard = []
    for n in n_range:
        #cross validation by splitting the data into 5 groups
        #each iteration uses a new fifth as the test data
        from sklearn.model_selection import KFold
        kf = KFold(n_splits=num_splits)
        error = []
        for train, test in kf.split(X):
            alpha = 1/(2*C)
            Xtrain_poly = PolynomialFeatures(n).fit_transform(X[train])
            Xtest_poly = PolynomialFeatures(n).fit_transform(X[test])
            X_poly = PolynomialFeatures(n).fit_transform(X)

            model = Lasso(alpha)
            #model = Ridge(alpha)
            model.fit(Xtrain_poly, y[train])

            predict = model.predict(Xtest_poly)
            # print("C: "+str(C))
            # print("coef: "+str(model.coef_))
            # print("intercept: "+str(model.intercept_))
            enter = [[0, 0, 0, 1, 0, 0.6, 0.8, 90.5, 0]]  # predict particular scenarios
            enter = PolynomialFeatures(n).fit_transform(enter)

            from sklearn.metrics import mean_squared_error
            print("prediction: "+str(model.predict(enter)))
            print("mean squared error: " + str(mean_squared_error(y[test], predict)))
            error.append(mean_squared_error(y[test],predict))

            font1 = {'family':'serif','color':'black','size':15}
            font2 = {'family':'serif','color':'black','size':10}
            #fig = plt.figure()
            #ax = plt.subplot(1,1,1)

        mean.append(sum(error)/len(error))    #these will be our y values
        standard.append(statistics.stdev(error))#these are our y error values
        
#ax.plot(C_range,mean)                                  #accuracy vs C
#plt.errorbar(C_range, mean, xerr=0, yerr=standard)
plt.plot(n_range,mean)                                  #accuracy vs poly order
plt.errorbar(n_range, mean, xerr=0, yerr=standard)
#plt.show()
'''
print("KNN")

from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import PolynomialFeatures

k_range =[10]# np.arange(1,101,5)
num_splits = 5
mean = []
standard = []
for k in k_range:
    #cross validation by splitting the data into 5 groups
    #each iteration uses a new fifth as the test data
    from sklearn.model_selection import KFold
    kf = KFold(n_splits=num_splits)
    Accuracy = []
    for train, test in kf.split(X):
        model = KNeighborsRegressor(n_neighbors=k, weights='uniform').fit(X[train], y[train])
        model.fit(X[train], y[train])
        # enter = [[90,5,300,1,0,0,0.2,5,20,10,60,5000,15]]
        enter = [[0, 1, 0, 0, 0, 0.1, 0.1, 90.5, 0]]  # predict particular scenarios

        model.fit(X[train], y[train])
        predict = model.predict(X[test])
        # print(predict)
        from sklearn.metrics import mean_squared_error

        print("Prediction: " + str(model.predict(enter)))

        # print("C: "+str(C))
        # print("coef: "+str(model.coef_))
        # print("intercept: "+str(model.intercept_))
        print("mean squared error: " + str(mean_squared_error(y[test], predict)))