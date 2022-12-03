import DataGlobals as g
import sklearn as sk
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor 
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
# from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import KFold
# from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

IN = './processed_data/withcompounds.csv'


def crossval_p(X, y, model, err, cvals, maxpoly, minpoly):
    if len(cvals) > 0:
        # model.C = cvals[0]
        model.alpha = (1 / (2 * cvals[0]))
    kf = KFold(n_splits=5)
    pvals, mean_err, std_err, mean_err_tr, std_err_tr = [], [], [], [], []
    for q in range(minpoly, maxpoly + 1):
        pvals.append(q)
        Xp = PolynomialFeatures(q, include_bias=False).fit_transform(X)
        sc = StandardScaler()
        Xp = sc.fit_transform(Xp)
        k_errors, k_errors_tr = [], []
        for train, test in kf.split(Xp):
            model.fit(Xp[train], y[train])
            y_pred = model.predict(Xp[test])
            k_errors.append(err(y[test], y_pred))
            y_pred = model.predict(Xp[train])
            k_errors_tr.append(err(y[train], y_pred))
        mean_err.append(np.array(k_errors).mean())
        std_err.append(np.array(k_errors).std())
        mean_err_tr.append(np.array(k_errors_tr).mean())
        std_err_tr.append(np.array(k_errors_tr).std())
    return pvals, mean_err, std_err, mean_err_tr, std_err_tr


def crossval_c(X, y, model, err, cvals):
    sc = StandardScaler()
    X = sc.fit_transform(X)
    mean_err, std_err = [], []
    kf = KFold(n_splits=5)
    for c in cvals:
        k_errors = []
        for train, test in kf.split(X):
            # model.C = c
            model.alpha = (1 / (2 * c))
            model.fit(X[train], y[train])
            y_pred = model.predict(X[test])
            k_errors.append(err(y[test], y_pred))
        mean_err.append(np.array(k_errors).mean())
        std_err.append(np.array(k_errors).std())
    return mean_err, std_err


def crossval_k(X, y, err, kvals):
    mean_err, std_err, mean_err_tr, std_err_tr = [], [], [], []
    kf = KFold(n_splits=5, shuffle=True)
    for k in kvals:
        k_errors, k_errors_tr = [], []
        for train, test in kf.split(X):
            model = KNeighborsRegressor(k, weights='uniform')
            model.fit(X[train], y[train])
            y_pred = model.predict(X[test])
            k_errors.append(err(y[test], y_pred))
            y_pred = model.predict(X[train])
            k_errors_tr.append(err(y[train], y_pred))
        mean_err.append(np.array(k_errors).mean())
        std_err.append(np.array(k_errors).std())
        mean_err_tr.append(np.array(k_errors_tr).mean())
        std_err_tr.append(np.array(k_errors_tr).std())
    plt.figure()
    plt.errorbar(kvals, mean_err, yerr=std_err, label=f'Test data')
    plt.errorbar(kvals, mean_err_tr, yerr=std_err_tr, label=f'Training data')
    plt.xlabel('K value')
    plt.ylabel('Mean Sq Err')
    plt.legend(loc='upper left')
    plt.title('Cross-validation for k selection')
    return mean_err, std_err


def crossval_hp(X, y, model, err, cvals, maxpoly=1, minpoly=1):
    # For one value of c focus on tuning
    if len(cvals) <= 1:
        pvals, mean, std, m_t, s_t = crossval_p(X, y, model, err, cvals, maxpoly, minpoly)
        plt.errorbar(pvals, mean, yerr=std, label=f'Test data')
        plt.errorbar(pvals, m_t, yerr=s_t, label=f'Training data')
        plt.xlabel('q value (max polynomial orders)')
        plt.title('For different max polynomial order values')
        ax = plt.gca()
        ax.set_xticks(list(range(1, maxpoly + 1)))
    else:
        for q in range(minpoly, maxpoly + 1):
            Xp = PolynomialFeatures(q, include_bias=False).fit_transform(X)

            mean, std = crossval_c(Xp, y, model, err, cvals)
            # Plot
            plt.errorbar(cvals, mean, yerr=std, label=f'q: {q}')
        plt.xlabel('C value')
        plt.title('For max polynomial orders q and penalty weight C')
    plt.ylabel('Mean Sq Err')
    plt.legend(loc='center right')
    plt.suptitle('Cross-validation for hyperparameter selection')
    return



# 2D Plot
def scPlot(p, xa, ya, cl, c_pos, c_neg, m_pos, m_neg, a, l_pos, l_neg):
    y1x, y1y = xa.copy(), ya.copy()
    y2x, y2y = [], []
    for i in range(len(cl)):
        if cl[i] > 0:
            y2x.append(y1x.pop(i))
            y2y.append(y1y.pop(i))
    p.scatter(y1x, y1y, color=c_neg, marker=m_neg, alpha=a, label=l_neg)
    p.scatter(y2x, y2y, color=c_pos, marker=m_pos, alpha=a, label=l_pos)


def main():

    df = pd.read_csv(IN)

    lap_pct = df.loc[:, g.LAP_PCT]
    tyre_age_pct = df.loc[:, g.TYRE_AGE_PCT]
    soft = df.loc[:, g.SOFT]
    medium = df.loc[:, g.MEDIUM]
    hard = df.loc[:, g.HARD]
    ptl = df.loc[:, g.PIT_THIS_LAP]
    pt = df.loc[:, g.PIT_TIME]
    quali = df.loc[:, g.QUALI_TIME]
    ideal = df.loc[:, g.IDEAL]
    c1 = df.loc[:, 'c1']
    c2 = df.loc[:, 'c2']
    c3 = df.loc[:, 'c3']
    c4 = df.loc[:, 'c4']
    c5 = df.loc[:, 'c5']

    X = np.column_stack((c1, c2, c3, c4, c5, lap_pct, tyre_age_pct, pt, ptl, ideal))
    y = df.loc[:, g.LAP_TIME]

    sc = StandardScaler()
    model = Lasso()

    # Baseline predictors
    dummy_f = DummyRegressor(strategy='mean')
    dummy_f.fit(X, y)
    fy_pred = dummy_f.predict(X)

    model = Ridge()

    cvals = [0.000005, 0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01]
    crossval_hp(X, y, model, mean_squared_error, cvals, 4, 1)
    plt.axhline(mean_squared_error(y, fy_pred), color='pink', label="Mean baseline predictor")
    plt.legend()
    plt.suptitle("[Ridge regression] Cross validation for hyperparameters")

    # # Plot values of q
    plt.figure()
    crossval_hp(X, y, model, mean_squared_error, [0.0004], 5)
    plt.legend(loc='lower left')
    plt.suptitle("[Ridge regression] Cross validation for hyperparameters")

    # # Plot c values for one q
    plt.figure()
    cvals = [0.00001, 0.00005, 0.0001, 0.0002, 0.0004, 0.0008, 0.0012, 0.0016, 0.0032, 0.0064, 0.0128]
    cvals = [1, 2, 5, 10, 15, 20, 30, 40]
    plt.axhline(mean_squared_error(y, fy_pred), color='pink', label="Mean baseline predictor")
    crossval_hp(X, y, model, mean_squared_error, cvals, 1, 1)
    plt.suptitle("[Ridge regression] Cross validation for hyperparameters")

    model = Lasso()

    cvals = [0.000005, 0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 0.01]
    cvals = [0.01, 0.1, 1, 10, 20, 40, 80, 160]
    crossval_hp(X, y, model, mean_squared_error, cvals, 4, 1)
    plt.axhline(mean_squared_error(y, fy_pred), color='pink', label="Mean baseline predictor")
    plt.legend()
    plt.suptitle("[Lasso regression] Cross validation for hyperparameters")

    # # Plot values of q
    plt.figure()
    crossval_hp(X, y, model, mean_squared_error, [10], 5)
    plt.legend(loc='lower left')
    plt.suptitle("[Lasso regression] Cross validation for hyperparameters")

    # # Plot c values for one q
    plt.figure()
    cvals = [0.00001, 0.00005, 0.0001, 0.0002, 0.0004, 0.0008, 0.0012, 0.0016, 0.0032, 0.0064, 0.0128]
    cvals = [1, 2, 5, 10, 15, 20, 30, 40]
    # plt.axhline(mean_squared_error(y, fy_pred), color='pink', label="Mean baseline predictor")
    crossval_hp(X, y, model, mean_squared_error, cvals, 1, 1)
    plt.suptitle("[Lasso regression] Cross validation for hyperparameters")

    crossval_k(X, y, mean_squared_error, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
    # Baseline too large to plot!
    # plt.axhline(mean_squared_error(y, fy_pred), color='pink', label="Mean baseline predictor")
    plt.legend(loc='upper right')


    plt.show()

    print(f"Ridge Regression with q=2 & c=0.0004. Model parameters:")
    q = 2
    c = 0.0004
    Xp = PolynomialFeatures(q).fit_transform(X)
    Xp = sc.fit_transform(Xp)
    model = Ridge(alpha=(1 / (2*c)))
    model.fit(Xp, y)
    y_pred = model.predict(Xp)

    s = [[0, 0, 1, 0, 0, .1, .1, 0, 0, 95]]
    s = PolynomialFeatures(q).fit_transform(s)
    sc.transform(s)
    print(model.predict(s))

    print(f"intercept: {model.intercept_}\ncoef:\n{model.coef_}")
    print(f"[Ridge Regression] Mean Squared Error: {mean_squared_error(y, y_pred)}")

    print(f"Lasso Regression with q=1 & c=10. Model parameters:")
    q = 1
    c = 10
    Xp = PolynomialFeatures(q).fit_transform(X)
    Xp = sc.fit_transform(Xp)
    model = Lasso(alpha=(1 / (2*c)))
    model.fit(Xp, y)
    y_pred = model.predict(Xp)
    print(f"intercept: {model.intercept_}\ncoef:\n{model.coef_}")
    print(f"[Lasso Regression] Mean Squared Error: {mean_squared_error(y, y_pred)}")

    kf = KFold(n_splits=5, shuffle=True)
    
    model = None
    for train, test in kf.split(X):
        model = KNeighborsRegressor(n_neighbors=10, weights='uniform')
        model.fit(X[train], y[train])
        predict = model.predict(X[test])
        print("mean squared error: " + str(mean_squared_error(y[test], predict)))
        # err.append(mean_squared_error(y[test], predict, squared=True))

    ys, xs = [], []
    for i in range(21):
        pct = i/20
        xs.append(pct)
        yp = model.predict([[1, 0, 0, 0, 0, 0.5, pct, 0, 0, 95]])
        ys.append(yp)
    plt.suptitle("Lap times with C1 tyre compound as tyre age increases")
    plt.title(f"At 50% race distance with an ideal time of 95 seconds")
    plt.scatter(xs, ys)
    plt.xlabel('Tyre age in percentage of total race laps')
    plt.ylabel('Lap time')
    plt.show()


if __name__ == '__main__':
    main()
