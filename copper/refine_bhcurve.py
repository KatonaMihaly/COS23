from functools import reduce

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import curve_fit
import json
from scipy.optimize import curve_fit

def read_lvm_file(file_path):
    try:
        # Load the data from the .lvm file into a NumPy array
        data = np.loadtxt(file_path, skiprows=0)  # Skip header rows, adjust if needed

        # Assuming the data in the file has two columns, you can split them into x and y
        x = data[:, 0]  # First column
        # If you want to store the second column (y values) as well:
        y = data[:, 1]  # Second column

        return x, y
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

switch = 0
if switch == 1:

    df_bhc = pd.DataFrame()
    df_bhv = pd.DataFrame()
    df_bhv['H'] = [0]
    df_bhv['B'] = [0]

    for i in range(1, 10):
        f = read_lvm_file("measurement/bhcurve/S235_0" + str(i) + "A.lvm")

        df = pd.DataFrame()
        df['H'] = f[0]
        df['B'] = f[1]

        df_bhc['H0' + str(i)] = f[0]
        df_bhc['B0' + str(i)] = f[1]
        new_row = pd.DataFrame()
        new_row['H'] = [max(f[0])]
        new_row['B'] = [max(f[1])]

        df_bhv = pd.concat([df_bhv, new_row], axis=0, ignore_index=True)

    for i in range(10, 27):
        f = read_lvm_file("measurement/bhcurve/S235_" + str(i) + "A.lvm")

        df = pd.DataFrame()
        df['H'] = f[0]
        df['B'] = f[1]

        df_bhc['H' + str(i)] = f[0]
        df_bhc['B' + str(i)] = f[1]
        new_row = pd.DataFrame()
        new_row['H'] = [max(f[0])]
        new_row['B'] = [max(f[1])]

        df_bhv = pd.concat([df_bhv, new_row], axis=0, ignore_index=True)

    for i in range(30, 31):
        f = read_lvm_file("measurement/bhcurve/S235_" + str(i) + "A.lvm")

        df = pd.DataFrame()
        df['H'] = f[0]
        df['B'] = f[1]

        df_bhc['H' + str(i)] = f[0]
        df_bhc['B' + str(i)] = f[1]
        new_row = pd.DataFrame()
        new_row['H'] = [max(f[0])]
        new_row['B'] = [max(f[1])]

        df_bhv = pd.concat([df_bhv, new_row], axis=0, ignore_index=True)

    for i in range(1, 10):
        f = read_lvm_file("measurement/bhcurve/B0" + str(i) + "0.lvm")

        df = pd.DataFrame()
        df['H'] = f[0]
        df['B'] = f[1]

        df_bhc['H' + str(i)] = f[0]
        df_bhc['B' + str(i)] = f[1]
        new_row = pd.DataFrame()
        new_row['H'] = [max(f[0])]
        new_row['B'] = [max(f[1])]

        df_bhv = pd.concat([df_bhv, new_row], axis=0, ignore_index=True)

    for i in range(0, 10):
        f = read_lvm_file("measurement/bhcurve/B10" + str(i) + ".lvm")

        df = pd.DataFrame()
        df['H'] = f[0]
        df['B'] = f[1]

        df_bhc['H' + str(i)] = f[0]
        df_bhc['B' + str(i)] = f[1]
        new_row = pd.DataFrame()
        new_row['H'] = [max(f[0])]
        new_row['B'] = [max(f[1])]

        df_bhv = pd.concat([df_bhv, new_row], axis=0, ignore_index=True)

    for i in range(10, 41):
        f = read_lvm_file("measurement/bhcurve/B1" + str(i) + ".lvm")

        df = pd.DataFrame()
        df['H'] = f[0]
        df['B'] = f[1]

        df_bhc['H' + str(i)] = f[0]
        df_bhc['B' + str(i)] = f[1]
        new_row = pd.DataFrame()
        new_row['H'] = [max(f[0])]
        new_row['B'] = [max(f[1])]

        df_bhv = pd.concat([df_bhv, new_row], axis=0, ignore_index=True)

    df_bhv.to_pickle('measurement/df_bhv')

df_bhv = pd.read_pickle('measurement/bhcurve/df_bhv')
# f = json.load('measurement/df_bhv.json')
# print(f)
# # df_bhv = pd.read_json(f)
#
# print(df_bhv)
# print(df_bhv)
# rev = -df_bhv.iloc[::-1]
# rev = rev.reset_index(drop=True)
# df_bhv = pd.concat([rev, df_bhv], axis=0, ignore_index=True)
df_bhv = df_bhv.sort_values(['H', 'B'], ignore_index = True)
df_bhv = df_bhv.drop(index=[1, 7, 11, 14, 16, 17, 18, 20, 21, 22, 24, 26, 27, 28, 30, 31, 32, 34, 35, 36, 38, 40, 42, 44,
                            46, 48, 50, 52, 54, 59, 60, 65, 72, 73, 74])
# print(df_bhv.to_string())
a = 12
b = -1
xdata1 = list(df_bhv['H'].iloc[a:b])
ydata1 = list(df_bhv['B'].iloc[a:b])
xdata2 = list(df_bhv['H'].iloc[0:a+4])
ydata2 = list(df_bhv['B'].iloc[0:a+4])
xmes = list(df_bhv['H'])
ymes = list(df_bhv['B'])
# print(ydata)
# spline = scipy.interpolate.InterpolatedUnivariateSpline(xdata, ydata)
# xi = list(np.linspace(0, 15000, 10))
# yi = spline(xi)
# plt.scatter(xdata, ydata, color='r')
# plt.plot(xi, yi, color='b')
# plt.show()

def func(x, a, b, c): # x-shifted log
    return a*np.log(x + b)+c

# these are the same as the scipy defaults
initialParameters = np.array([1, 1, 1])

# curve fit the test data
fittedParameters1, pcov = curve_fit(func, xdata1, ydata1, initialParameters)
fittedParameters2, pcov = curve_fit(func, xdata2, ydata2, initialParameters)

j = 20000
x1 = np.linspace(195, j, 190)
x2 = np.linspace(0, 195, 10)
modelPredictions1 = func(x1, *fittedParameters1)
modelPredictions2 = func(x2, *fittedParameters2)

x_ref = list(x2) + list(x1)
y_ref = list(modelPredictions2) + list(modelPredictions1)
x_ref[0] = 0
y_ref[0] = 0

print([round(i, 4) for i in y_ref])
res = {'H': x_ref, 'B': y_ref}
res = pd.DataFrame(res)

plt.plot(x_ref, y_ref, color='r')
# plt.plot(x1, modelPredictions1)
# plt.plot(x2, modelPredictions2)
plt.scatter(xmes, ymes)
# plt.scatter(xdata1, ydata1)
# plt.scatter(xdata2, ydata2)
plt.xlabel("H [A/m]")
plt.ylabel("B [T]")
plt.grid()
plt.show()

file_path = 'measurement/bhcurve/S235_BH_H' + str(j) + '.xlsx'
res.to_excel(file_path, index=False)


# for i in range(1, 10):
#     plt.plot(df_bhc['H0' + str(i)], df_bhc['B0' + str(i)],)
#
# # for i in range(10, 11):
# #     plt.plot(df_bhc['H' + str(i)], df_bhc['B' + str(i)], )
#
# plt.show()