import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches

#  0 - 25An, 1 - 25Ap, 2 - 25Afull
#  3 - 35An, 4 - 35Ap, 5 - 35Afull
#  6 - 12An, 7 - 12Ap, 8 - 12Afull
switch = 8
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
    plt.plot(mes['Angle'], mes['Torque'], label='Simulation (25A)')

    handles, labels = plt.gca().get_legend_handles_labels()  # get existing handles and labels
    empty_patch = mpatches.Patch(color='none', label='Extra label')  # create a patch with no color
    handles.append(empty_patch)  # add new patches and labels to list
    labels.append("Measurement (25A)")
    plt.legend(handles, labels, fontsize=12)  # apply new handles and labels to plot
    # plt.legend(fontsize=12)

    plt.xticks(np.arange(-24, 25, 4), np.arange(-24, 25, 4), fontsize=12)
    plt.yticks(np.arange(-7, 8, 2), np.arange(-7, 8, 2), fontsize=12)
    plt.xlabel('Rotor position [deg]', fontsize=12)
    plt.ylabel('Static torque [Nm]', fontsize=12)
    plt.grid()

    plt.savefig('media/wp0i25a24_24r1l78.png', dpi=300)
    plt.show()

if switch == 3:

    file_path = 'measurement/35A_negative.dat'
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    data = data.replace(',', '.', regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    df = pd.DataFrame()
    df['Torque'] = data.transpose()
    df.drop(df.index[1288:], inplace=True)
    df['Torque'].plot()
    plt.show()

    subset1 = df.iloc[0:28, :].reset_index(drop=True)
    subset2 = df.iloc[29:79, :].reset_index(drop=True)
    subset3 = df.iloc[80:130, :].reset_index(drop=True)
    subset4 = df.iloc[131:180, :].reset_index(drop=True)
    subset5 = df.iloc[184:237, :].reset_index(drop=True)
    subset6 = df.iloc[240:290, :].reset_index(drop=True)
    subset7 = df.iloc[293:333, :].reset_index(drop=True)
    subset8 = df.iloc[339:379, :].reset_index(drop=True)
    subset9 = df.iloc[385:427, :].reset_index(drop=True)
    subset10 = df.iloc[431:480, :].reset_index(drop=True)
    subset11 = df.iloc[485:538, :].reset_index(drop=True)
    subset12 = df.iloc[540:590, :].reset_index(drop=True)
    subset13 = df.iloc[591:660, :].reset_index(drop=True)
    subset14 = df.iloc[665:740, :].reset_index(drop=True)
    subset15 = df.iloc[744:807, :].reset_index(drop=True)
    subset16 = df.iloc[812:832, :].reset_index(drop=True)

    df_sub = pd.concat([subset1, subset2, subset3, subset4, subset5, subset6, subset7, subset8, subset9, subset10,
                        subset11, subset12, subset13, subset14, subset15, subset16], axis=1, ignore_index=True)

    result35An = pd.DataFrame()

    for i in range(df_sub.shape[1]):
        average = df_sub.iloc[:, i].mean(skipna=True).round(3)
        minimum = df_sub.iloc[:, i].min(skipna=True).round(3)
        maximum = df_sub.iloc[:, i].max(skipna=True).round(3)

        result35An[str(i)] = pd.DataFrame([average, minimum, maximum], index=['Average', 'Minimum', 'Maximum'])

    print(result35An)
    result35An.to_json('measurement/results35An.json')
    df_sub.to_json('measurement/results35An_sub.json')
    result35An.boxplot()
    plt.show()

if switch == 4:

    file_path = 'measurement/35A_positive.dat'
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    data = data.replace(',', '.', regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    df = pd.DataFrame()
    df['Torque'] = data.transpose()
    # df.drop(df.index[1210:], inplace=True)
    df = df.iloc[788:1586, :].reset_index(drop=True)
    df = df.iloc[::-1].reset_index(drop=True)
    print(df)
    df['Torque'].plot()
    plt.show()

    subset1 = df.iloc[0:99, :].reset_index(drop=True)
    subset2 = df.iloc[104:162, :].reset_index(drop=True)
    subset3 = df.iloc[167:207, :].reset_index(drop=True)
    subset4 = df.iloc[215:257, :].reset_index(drop=True)
    subset5 = df.iloc[260:299, :].reset_index(drop=True)
    subset6 = df.iloc[302:349, :].reset_index(drop=True)
    subset7 = df.iloc[355:406, :].reset_index(drop=True)
    subset8 = df.iloc[412:458, :].reset_index(drop=True)
    subset9 = df.iloc[463:514, :].reset_index(drop=True)
    subset10 = df.iloc[518:574, :].reset_index(drop=True)
    subset11 = df.iloc[579:624, :].reset_index(drop=True)
    subset12 = df.iloc[630:687, :].reset_index(drop=True)
    subset13 = df.iloc[691:737, :].reset_index(drop=True)
    subset14 = df.iloc[743:798, :].reset_index(drop=True)

    df_sub = pd.concat(
        [subset1, subset2, subset3, subset4, subset5, subset6, subset7, subset8, subset9, subset10, subset11,
         subset12, subset13, subset14], axis=1, ignore_index=True)

    result35Ap = pd.DataFrame()

    for i in range(df_sub.shape[1]):
        average = df_sub.iloc[:, i].mean(skipna=True).round(3)
        minimum = df_sub.iloc[:, i].min(skipna=True).round(3)
        maximum = df_sub.iloc[:, i].max(skipna=True).round(3)

        result35Ap[str(i)] = pd.DataFrame([average, minimum, maximum], index=['Average', 'Minimum', 'Maximum'])

    print(result35Ap)
    result35Ap.to_json('measurement/results35Ap.json')
    df_sub.to_json('measurement/results35Ap_sub.json')

    result35Ap.boxplot()
    plt.show()

if switch == 5:
    df1 = pd.read_json('measurement/results35Ap_sub.json')
    df2 = pd.read_json('measurement/results35An_sub.json')
    df = pd.concat([df1, df2], axis=1)
    df = df.reset_index(drop=True)
    df.columns = [np.arange(0, 30, 1)]
    df = df.drop(df.columns[[13]], axis=1)
    df.columns = [np.arange(0, 29, 1)]
    print(df.to_string())

    mes = pd.read_json('data/wp0i35a24_24r025l78.json')
    mes['Angle'] = np.linspace(-24, 24, len(mes['Torque']))
    print(mes)

    df3 = pd.read_json('measurement/results35Ap.json')
    df4 = pd.read_json('measurement/results35An.json')
    df5 = pd.concat([df3, df4], axis=1)
    df5 = df5.reset_index(drop=True)


    x_values = [-19.5, -16, -15, -14, -12.5, -11.5, -9.5, -8, -6.5, -5, -3.5, -2, -1, 0, 1, 2.5, 4, 5.5, 7.5, 8.5, 11,
                12, 13, 14.5, 15, 16, 19, 20, 20.5]

    y_values = [df.iloc[:, 0].dropna(), df.iloc[:, 1].dropna(), df.iloc[:, 2].dropna(), df.iloc[:, 3].dropna(),
                df.iloc[:, 4].dropna(), df.iloc[:, 5].dropna(), df.iloc[:, 6].dropna(), df.iloc[:, 7].dropna(),
                df.iloc[:, 8].dropna(), df.iloc[:, 9].dropna(), df.iloc[:, 10].dropna(), df.iloc[:, 11].dropna(),
                df.iloc[:, 12].dropna(), df.iloc[:, 13].dropna(), df.iloc[:, 14].dropna(), df.iloc[:, 15].dropna(),
                df.iloc[:, 16].dropna(), df.iloc[:, 17].dropna(), df.iloc[:, 18].dropna(), df.iloc[:, 19].dropna(),
                df.iloc[:, 20].dropna(), df.iloc[:, 21].dropna(), df.iloc[:, 22].dropna(), df.iloc[:, 23].dropna(),
                df.iloc[:, 24].dropna(), df.iloc[:, 25].dropna(), df.iloc[:, 26].dropna(), df.iloc[:, 27].dropna(),
                df.iloc[:, 28].dropna()]

    plt.boxplot(y_values, positions=x_values, showfliers=False)
    plt.plot(mes['Angle'], -mes['Torque'], label='Simulation (35A)')

    handles, labels = plt.gca().get_legend_handles_labels()  # get existing handles and labels
    empty_patch = mpatches.Patch(color='none', label='Extra label')  # create a patch with no color
    handles.append(empty_patch)  # add new patches and labels to list
    labels.append("Measurement (35A)")
    plt.legend(handles, labels, fontsize=12)  # apply new handles and labels to plot

    plt.xticks(np.arange(-24, 25, 4), np.arange(-24, 25, 4), fontsize=12)
    plt.yticks(np.arange(-14, 16, 3), np.arange(-14, 16, 3), fontsize=12)
    plt.xlabel('Rotor position [deg]', fontsize=12)
    plt.ylabel('Static torque [Nm]', fontsize=12)
    plt.grid()

    plt.savefig('media/wp0i35a24_24r1l78.png', dpi=300)
    plt.show()

if switch == 6:

    file_path = 'measurement/12A_negative.dat'
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    data = data.replace(',', '.', regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    df = pd.DataFrame()
    df['Torque'] = data.transpose()
    df.drop(df.index[780:], inplace=True)
    df['Torque'].plot()
    plt.show()

    subset1 = df.iloc[40:86, :].reset_index(drop=True)
    subset2 = df.iloc[88:148, :].reset_index(drop=True)
    subset3 = df.iloc[167:209, :].reset_index(drop=True)
    subset4 = df.iloc[214:267, :].reset_index(drop=True)
    subset5 = df.iloc[276:341, :].reset_index(drop=True)
    subset6 = df.iloc[349:399, :].reset_index(drop=True)
    subset7 = df.iloc[405:478, :].reset_index(drop=True)
    subset8 = df.iloc[493:567, :].reset_index(drop=True)
    subset9 = df.iloc[573:632, :].reset_index(drop=True)
    subset10 = df.iloc[633:717, :].reset_index(drop=True)
    subset11 = df.iloc[730:780, :].reset_index(drop=True)

    df_sub = pd.concat([subset1, subset2, subset3, subset4, subset5, subset6, subset7, subset8, subset9, subset10,
                        subset11], axis=1, ignore_index=True)

    result12An = pd.DataFrame()

    for i in range(df_sub.shape[1]):
        average = df_sub.iloc[:, i].mean(skipna=True).round(3)
        minimum = df_sub.iloc[:, i].min(skipna=True).round(3)
        maximum = df_sub.iloc[:, i].max(skipna=True).round(3)

        result12An[str(i)] = pd.DataFrame([average, minimum, maximum], index=['Average', 'Minimum', 'Maximum'])

    print(result12An)
    result12An.to_json('measurement/results12An.json')
    df_sub.to_json('measurement/results12An_sub.json')
    result12An.boxplot()
    plt.show()

if switch == 7:

    file_path = 'measurement/12A_positive.dat'
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    data = data.replace(',', '.', regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    df = pd.DataFrame()
    df['Torque'] = data.transpose()
    # df.drop(df.index[1210:], inplace=True)
    df = df.iloc[0:788, :].reset_index(drop=True)
    df = df.iloc[::-1].reset_index(drop=True)
    print(df)
    df['Torque'].plot()
    plt.show()

    subset1 = df.iloc[0:99, :].reset_index(drop=True)
    subset2 = df.iloc[104:162, :].reset_index(drop=True)
    subset3 = df.iloc[167:207, :].reset_index(drop=True)
    subset4 = df.iloc[215:257, :].reset_index(drop=True)
    subset5 = df.iloc[260:299, :].reset_index(drop=True)
    subset6 = df.iloc[302:349, :].reset_index(drop=True)
    subset7 = df.iloc[355:406, :].reset_index(drop=True)
    subset8 = df.iloc[412:458, :].reset_index(drop=True)
    subset9 = df.iloc[463:514, :].reset_index(drop=True)
    subset10 = df.iloc[518:574, :].reset_index(drop=True)
    subset11 = df.iloc[579:624, :].reset_index(drop=True)
    subset12 = df.iloc[630:687, :].reset_index(drop=True)
    subset13 = df.iloc[691:737, :].reset_index(drop=True)
    subset14 = df.iloc[743:798, :].reset_index(drop=True)

    df_sub = pd.concat(
        [subset1, subset2, subset3, subset4, subset5, subset6, subset7, subset8, subset9, subset10, subset11,
         subset12, subset13, subset14], axis=1, ignore_index=True)

    result12Ap = pd.DataFrame()

    for i in range(df_sub.shape[1]):
        average = df_sub.iloc[:, i].mean(skipna=True).round(3)
        minimum = df_sub.iloc[:, i].min(skipna=True).round(3)
        maximum = df_sub.iloc[:, i].max(skipna=True).round(3)

        result12Ap[str(i)] = pd.DataFrame([average, minimum, maximum], index=['Average', 'Minimum', 'Maximum'])

    print(result12Ap)
    result12Ap.to_json('measurement/results12Ap.json')
    df_sub.to_json('measurement/results12Ap_sub.json')

    result12Ap.boxplot()
    plt.show()

if switch == 8:
    df = pd.read_json('measurement/results12An_sub.json')
    print(df.to_string())

    mes = pd.read_json('data/wp0i12a0_24r025l78.json')
    mes['Angle'] = np.linspace(0, 24, len(mes['Torque']))
    print(mes)

    x_values = [0, 1, 2, 3.5, 5.5, 8, 9, 12, 16.5, 18.5, 20.5]

    y_values = [df.iloc[:, 0].dropna(), df.iloc[:, 1].dropna(), df.iloc[:, 2].dropna(), df.iloc[:, 3].dropna(),
                df.iloc[:, 4].dropna(), df.iloc[:, 5].dropna(), df.iloc[:, 6].dropna(), df.iloc[:, 7].dropna(),
                df.iloc[:, 8].dropna(), df.iloc[:, 9].dropna(), df.iloc[:, 10].dropna()]

    plt.boxplot(y_values, positions=x_values, showfliers=False)
    plt.plot(mes['Angle'], -mes['Torque'], label='Simulation (12A)')

    handles, labels = plt.gca().get_legend_handles_labels()  # get existing handles and labels
    empty_patch = mpatches.Patch(color='none', label='Extra label')  # create a patch with no color
    handles.append(empty_patch)  # add new patches and labels to list
    labels.append("Measurement (12A)")
    plt.legend(handles, labels, fontsize=12)  # apply new handles and labels to plot

    plt.xticks(np.arange(0, 25, 4), np.arange(0, 25, 4), fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Rotor position [deg]', fontsize=12)
    plt.ylabel('Static torque [Nm]', fontsize=12)
    plt.grid()

    plt.savefig('media/wp0i12a0_24r1l78.png', dpi=300)
    plt.show()