import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import math
import DataGlobals as g

df = pd.read_csv( "./processed_data/race_data_no_dnfs.csv" )
print( df . head ( ) )
race = df.iloc[:,3]


lap	= df.loc[:,g.LAP_N]
short_name = df.loc[:,g.SHORT_NAME]
driver_id = df.loc[:,g.ID]
team = df.loc[:,g.TEAM]
engine = df.loc[:,g.ENGINE]
grid_position = df.loc[:,g.GRID]
quali_time = df.loc[:,g.QUALI_TIME]
lap_position = df.loc[:,g.LAP_POS]
lap_time = df.loc[:,g.LAP_TIME]
gap_to_leader = df.loc[:,g.GTL]
position = df.loc[:,g.POS]
points = df.loc[:,g.POINTS]
fastest_s1 = df.iloc[:,16]
fastest_s2 = df.iloc[:,17]
fastest_s3 = df.iloc[:,18]
ideal_time = df.iloc[:,19]
s1_speed = df.iloc[:,20]
s2_speed = df.iloc[:,21]
s3_speed = df.iloc[:,22]
speed_trap = df.iloc[:,23]
tyre = df.loc[:, g.TYRE_STRING]
pit_time = df.iloc[:,25]
tyre_num = df.iloc[:, 26]
used = df.iloc[:, 27]
tyre_age = df.iloc[:, 28]
pit_this_lap = df.iloc[:, 29]
next_pit = df.iloc[:, 30]
total_laps = df.iloc[:, 31]
lap_pcts = df.iloc[:, 32]
# tyre_age_pct = df.iloc[:, 33]
# next_pit_pcts = df.iloc[:, 34]
# distances = df.iloc[:, 35]
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
minimum = []

for i in range(len(race)):
    j = -1
    if i==0:
        minimum.append(999)
        j+1
    if i>0:
        if race[i] != race[i - 1]:
            minimum.append(999)
            j+1
    if minimum[j]>lap_time[i]:
        minimum[j] = lap_time[i]
# print(minimum)
lap_time_norm = []
for i in range(len(lap_time)):
    j = -1
    if i==0:
        j+1
    if i>0:
        if race[i] != race[i - 1]:
            j+1
    lap_time_norm.append(lap_time[i]/minimum[j])

# X=np.column_stack( ( quali_time, gap_to_leader, speed_trap, soft,medium,hard, lap_pcts, lap,pit_time, tyre_age,total_laps,distances,next_pit ) )

# This is easier than using indices
tyre_age_pct = df.loc[:, g.TYRE_AGE_PCT]
tyre_num = df.loc[:, g.TYRE_NUM]
lap_pcts = df.loc[:, g.LAP_PCT]
quali_time = df.loc[:, g.QUALI_TIME]
pit_time = df.loc[:, g.PIT_TIME]
lap_time = df.loc[:, g.LAP_TIME]
distance = df.loc[:, g.DISTANCE]
used = df.loc[:, g.USED]

X=np.column_stack( ( soft, medium, hard, tyre_age_pct, lap_pcts,quali_time, pit_time) )#features
y = lap_time
# print(y)
# y = lap_time_norm
from sklearn.model_selection import train_test_split    #holding back 20% of data for testing
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)

from sklearn.linear_model import Lasso, Ridge
from sklearn.preprocessing import PolynomialFeatures
n = 2
C_range = [1,5,10,50,100,500,1000]  #values of C iterated over
for C in C_range:
    alpha = 1/(2*C) #models use alpha as a hyperparameter
    #introducing higher order features
    Xtrain_poly = PolynomialFeatures(n).fit_transform(Xtrain)
    Xtest_poly = PolynomialFeatures(n).fit_transform(Xtest)
    X_poly = PolynomialFeatures(n).fit_transform(X)
    #enter = [[90,5,300,1,0,0,0.2,5,20,10,60,5000,15]]
    # enter = [[1,0,0,10,0.1,90.5,20,0]]       #predict particular scenarios
    enter = [[1, 0, 0, 0.5, 0.5, 95.3, 0]]
    enter = PolynomialFeatures(n).fit_transform(enter)
    model = Lasso(alpha)
    #model = Ridge(alpha)
    model.fit(Xtrain_poly, ytrain)
    predict = model.predict(Xtest_poly)
    #print(predict)
    from sklearn.metrics import mean_squared_error
    print("Prediction: " + str(model.predict(enter)))

    #print("C: "+str(C))
    #print("coef: "+str(model.coef_))
    #print("intercept: "+str(model.intercept_))
    print("mean squared error: "+str(mean_squared_error(ytest, predict)))

    font1 = {'family':'serif','color':'black','size':15}
    font2 = {'family':'serif','color':'black','size':10}
    fig = plt.figure()

    #ax = plt.subplot(1,1,1)
    ax = plt.axes(projection='3d')
    #plotting all data
    p01 = ax.scatter3D(speed_trap, gap_to_leader,y,alpha = 0.5,color ="blue",label = "Training Data")
    X1test = []
    X2test = []
    for i in range(len(Xtest)):#plotting test data
        X1test.append(Xtest[i][0])
        X2test.append(Xtest[i][1])
    #p02 = ax.scatter3D(X1test,X2test,predict,color = "orange",label = "Test Data")
    fake = ax.scatter3D(X1test, X2test, predict, alpha=0,color="r", label="Predictions")

    mesh = []
    a = b = np.arange(-2.0, 2.0, 0.05)
    A, B = np.meshgrid(a, b)
    for i in range(len(a)):     #preparing mesh grid to plot predictions
        for j in range(len(b)):
            mesh.append([])
            mesh[-1].append(a[i])
            mesh[-1].append(b[j])

    mesh_poly = PolynomialFeatures(n).fit_transform(mesh)
    #zs = model.predict(mesh_poly)
    #Z = zs.reshape(A.shape)
    #Surface = ax.plot_surface(B,A,Z,color="r",alpha = 0.6)#plotting prediction surface

    #plt.xlim(-1.1,1.1)
    #plt.ylim(-1.1,1.1)

    l3 = ax.legend(bbox_to_anchor=(1.02, 0.5), loc="center left", borderaxespad=0)
    ax.xaxis.set_rotate_label(False)
    ax.yaxis.set_rotate_label(False)
    ax.zaxis.set_rotate_label(False)
    plt.xlabel(r'$X_1$', fontdict=font2)
    plt.ylabel(r'$X_2$', fontdict=font2)
    ax.set_zlabel(r'$\hat{y}$', fontdict=font2)
    plt.title("Ridge Regression with C = "+str(C),fontdict = font1)
    ax.view_init(elev = 20,azim = 45)

    #plt.show()