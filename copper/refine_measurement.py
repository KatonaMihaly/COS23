import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches

#  0 - 25An, 1 - 25Ap
switch = 2
if switch == 0:

    file_path = 'measurement/25A_negative.dat'
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    data = data.replace(',', '.', regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    df = pd.DataFrame()
    df['Torque'] = data.transpose()
    df.drop(df.index[1288:], inplace=True)
    # df['Torque'].plot()
    # plt.show()

    subset1 = df.iloc[0:75, :].reset_index(drop=True)
    subset2 = df.iloc[76:143, :].reset_index(drop=True)
    subset3 = df.iloc[143:196, :].reset_index(drop=True)
    subset4 = df.iloc[198:271, :].reset_index(drop=True)
    subset5 = df.iloc[274:331, :].reset_index(drop=True)
    subset6 = df.iloc[333:390, :].reset_index(drop=True)
    subset7 = df.iloc[392:443, :].reset_index(drop=True)
    subset8 = df.iloc[445:501, :].reset_index(drop=True)
    subset9 = df.iloc[504:558, :].reset_index(drop=True)
    subset10 = df.iloc[563:623, :].reset_index(drop=True)
    subset11 = df.iloc[625:706, :].reset_index(drop=True)
    subset12 = df.iloc[709:780, :].reset_index(drop=True)
    subset13 = df.iloc[783:834, :].reset_index(drop=True)
    subset14 = df.iloc[838:924, :].reset_index(drop=True)
    subset15 = df.iloc[926:991, :].reset_index(drop=True)
    subset16 = df.iloc[995:1071, :].reset_index(drop=True)
    subset17 = df.iloc[1075:1173, :].reset_index(drop=True)
    subset18 = df.iloc[1175:1288, :].reset_index(drop=True)

    df_sub = pd.concat([subset1, subset2, subset3, subset4, subset5, subset6, subset7, subset8, subset9, subset10, subset11,
                        subset12, subset13, subset14, subset15, subset16, subset17, subset18], axis=1, ignore_index=True)

    result25An = pd.DataFrame()

    for i in range(df_sub.shape[1]):
        average = df_sub.iloc[:, i].mean(skipna=True).round(3)
        minimum = df_sub.iloc[:, i].min(skipna=True).round(3)
        maximum = df_sub.iloc[:, i].max(skipna=True).round(3)

        result25An[str(i)] = pd.DataFrame([average, minimum, maximum], index=['Average', 'Minimum', 'Maximum'])

    print(result25An)
    result25An.to_json('measurement/results25An.json')
    df_sub.to_json('measurement/results25An_sub.json')
    result25An.boxplot()
    plt.show()

if switch == 1:

    file_path = 'measurement/25A_positive.dat'
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    data = data.replace(',', '.', regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    df = pd.DataFrame()
    df['Torque'] = data.transpose()
    df.drop(df.index[1210:], inplace=True)
    df = df.iloc[::-1].reset_index(drop=True)
    print(df)
    df['Torque'].plot()
    plt.show()

    subset1 = df.iloc[0:75, :].reset_index(drop=True)
    subset2 = df.iloc[76:156, :].reset_index(drop=True)
    subset3 = df.iloc[160:217, :].reset_index(drop=True)
    subset4 = df.iloc[220:270, :].reset_index(drop=True)
    subset5 = df.iloc[273:324, :].reset_index(drop=True)
    subset6 = df.iloc[327:375, :].reset_index(drop=True)
    subset7 = df.iloc[378:458, :].reset_index(drop=True)
    subset8 = df.iloc[460:530, :].reset_index(drop=True)
    subset9 = df.iloc[535:588, :].reset_index(drop=True)
    subset10 = df.iloc[591:660, :].reset_index(drop=True)
    subset11 = df.iloc[664:739, :].reset_index(drop=True)
    subset12 = df.iloc[742:800, :].reset_index(drop=True)
    subset13 = df.iloc[805:867, :].reset_index(drop=True)
    subset14 = df.iloc[870:934, :].reset_index(drop=True)
    subset15 = df.iloc[940:992, :].reset_index(drop=True)
    subset16 = df.iloc[996:1065, :].reset_index(drop=True)
    subset17 = df.iloc[1070:1135, :].reset_index(drop=True)
    subset18 = df.iloc[1139:1194, :].reset_index(drop=True)

    df_sub = pd.concat(
        [subset1, subset2, subset3, subset4, subset5, subset6, subset7, subset8, subset9, subset10, subset11,
         subset12, subset13, subset14, subset15, subset16, subset17, subset18], axis=1, ignore_index=True)

    result25Ap = pd.DataFrame()

    for i in range(df_sub.shape[1]):
        average = df_sub.iloc[:, i].mean(skipna=True).round(3)
        minimum = df_sub.iloc[:, i].min(skipna=True).round(3)
        maximum = df_sub.iloc[:, i].max(skipna=True).round(3)

        result25Ap[str(i)] = pd.DataFrame([average, minimum, maximum], index=['Average', 'Minimum', 'Maximum'])

    print(result25Ap)
    result25Ap.to_json('measurement/results25Ap.json')
    df_sub.to_json('measurement/results25Ap_sub.json')

    result25Ap.boxplot()
    plt.show()

if switch == 2:
    df1 = pd.read_json('measurement/results25Ap_sub.json')
    df2 = pd.read_json('measurement/results25An_sub.json')
    df = pd.concat([df1, df2], axis=1)
    df = df.reset_index(drop=True)

    mes = pd.read_json('data/wp0i25a24_24r025l78.json')
    mes['Angle'] = np.linspace(-24, 24, len(mes['Torque']))
    print(mes)

    df3 = pd.read_json('measurement/results25Ap.json')
    df4 = pd.read_json('measurement/results25An.json')
    df5 = pd.concat([df3, df4], axis=1)
    df5 = df5.reset_index(drop=True)
    print(df5)


    x_values = [-20.5, -19.75, -17, -16, -15.5, -14.75, -13, -12.5, -11, -10, -9, -8, -6, -5.5, -4, -3, -2, -1, 0, 1,
                2, 3, 4, 5, 6, 7.5, 8.5, 9.5, 11, 11.5, 12, 13.5, 14, 15, 16, 20]

    y_values = [df.iloc[:, 0].dropna(), df.iloc[:, 1].dropna(), df.iloc[:, 2].dropna(), df.iloc[:, 3].dropna(),
                df.iloc[:, 4].dropna(), df.iloc[:, 5].dropna(), df.iloc[:, 6].dropna(), df.iloc[:, 7].dropna(),
                df.iloc[:, 8].dropna(), df.iloc[:, 9].dropna(), df.iloc[:, 10].dropna(), df.iloc[:, 11].dropna(),
                df.iloc[:, 12].dropna(), df.iloc[:, 13].dropna(), df.iloc[:, 14].dropna(), df.iloc[:, 15].dropna(),
                df.iloc[:, 16].dropna(), df.iloc[:, 17].dropna(), df.iloc[:, 18].dropna(), df.iloc[:, 19].dropna(),
                df.iloc[:, 20].dropna(), df.iloc[:, 21].dropna(), df.iloc[:, 22].dropna(), df.iloc[:, 23].dropna(),
                df.iloc[:, 24].dropna(), df.iloc[:, 25].dropna(), df.iloc[:, 26].dropna(), df.iloc[:, 27].dropna(),
                df.iloc[:, 28].dropna(), df.iloc[:, 29].dropna(), df.iloc[:, 30].dropna(), df.iloc[:, 31].dropna(),
                df.iloc[:, 32].dropna(), df.iloc[:, 33].dropna(), df.iloc[:, 34].dropna(), df.iloc[:, 35].dropna()]

    plt.boxplot(y_values, positions=x_values, showfliers=False)
    plt.plot(mes['Angle'], mes['Torque'], label='Simulation')

    handles, labels = plt.gca().get_legend_handles_labels()  # get existing handles and labels
    empty_patch = mpatches.Patch(color='none', label='Extra label')  # create a patch with no color
    handles.append(empty_patch)  # add new patches and labels to list
    labels.append("Measurement")
    plt.legend(handles, labels, fontsize=12)  # apply new handles and labels to plot

    plt.xticks(np.arange(-24, 25, 3), np.arange(-24, 25, 3), fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Rotor position [deg]', fontsize=12)
    plt.ylabel('Static torque [Nm]', fontsize=12)
    plt.grid()

    plt.savefig('media/wp0i25a24_24r1l78.png', dpi=300)
    plt.show()