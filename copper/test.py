# stacklenght = [
#     69.45,
#     69.14,
#     68.35,
#     68.07,
#     68.31,
#     68.80,
#     71.47,
#     70.80,
#     71.42,
#     72.44,
#     70.61,
#     69.20,
#     68.52,
#     68.62,
#     68.86,
#     69.54,
#     71.52,
#     69.70,
#     68.59,
#     68.37,
#     67.70,
#     67.63,
#     68.61,
#     69.11,
#     69.75,
#     69.65,
#     68.97,
#     67.98,
#     68.00,
#     69.03,
#     69.89,
#     70.37,
#     70.92,
#     70.77,
#     69.95,
#     69.50,
#     68.28,
#     68.04,
#     68.59,
#     68.96,
#     69.37,
#     68.80,
#     68.50,
#     68.32,
#     68.19,
#     67.87,
#     68.25,
#     68.62
# ]
#
# # Python program to get average of a list
# def Average(lst):
#     return sum(lst) / len(lst)
#
#     # Driver Code
#     lst = [15, 9, 55, 41, 35, 20, 62, 49]
#     average = Average(lst)
#
#     # Printing average of the list
#     print("Average of the list =", round(average, 2))
#
# print(Average(stacklenght))
#
from math import pi

import matplotlib.pyplot as plt
from numpy import linspace
# a = 0
# b = 30
# c = 121
# rot = linspace(a+61, b+61, c)
# alp = linspace(a, -b*2, c)
# print(list(zip(rot, alp)))
# print(len(list(zip(rot, alp))))
#
# # temp0 = list(linspace(0, 90, 361))
# # angle = temp0 * 2
# # temp1 = [25] * len(temp0)
# # temp2 = [50] * len(temp0)
# # current = temp1 + temp2
# # print(list(zip(current, angle)))
# #
# # print(len(current))

print(linspace(0, 24, 97))
#
# y = [0.0000, 0.0974, 0.1949, 0.3004, 0.3343, 0.3609, 0.3900, 0.4110, 0.4354, 0.4609, 0.4895, 0.5102,
#                    0.5362, 0.5611, 0.5893, 0.6102, 0.6362, 0.6608, 0.6854, 0.7066, 0.7355, 0.7613, 0.7893, 0.8092,
#                    0.8344, 0.8596, 0.8826, 0.9015, 0.9230, 0.9433, 0.9640, 0.9857, 1.0048, 1.0309, 1.0556, 1.0780,
#                    1.0998, 1.1200, 1.1397, 1.1597, 1.1796, 1.1998, 1.2180, 1.2366, 1.2552, 1.2736, 1.2936, 1.3086,
#                    1.3265, 1.3433, 1.3597, 1.3764, 1.3946, 1.4072, 1.4219, 1.4357, 1.4495, 1.4633, 1.4771, 1.4920,
#                    1.5018, 1.5114, 1.5198, 1.5284, 1.5375, 1.5459, 1.5545, 1.5634, 1.5719, 1.5805, 1.5895, 1.5981,
#                    1.6048, 1.6119, 1.6188, 1.6256, 1.6325, 1.6393, 1.6462, 1.6529, 1.6591, 1.6630, 1.6733]
#
# x = [0.0000, 119.4373, 177.5188, 221.0054, 241.0910, 251.9625, 265.3464, 277.0617, 287.0970, 299.6462,
#                    313.8689, 326.4229, 338.1333, 351.5214, 365.7444, 379.9749, 393.3619, 407.5887, 420.9770, 436.0455,
#                    453.6212, 470.3617, 487.9383, 504.6847, 521.4258, 539.8434, 555.7485, 571.6575, 590.0790, 608.5016,
#                    626.9239, 645.3451, 663.7690, 682.1858, 700.6040, 717.3479, 734.0924, 752.5152, 770.9384, 789.3614,
#                    807.7844, 826.2072, 844.6320, 863.0563, 881.4807, 899.9052, 918.3281, 936.7561, 955.1812, 973.6074,
#                    992.0339, 1010.4602, 1028.8849, 1047.3153, 1065.7436, 1084.1728, 1102.6020, 1121.0312, 1139.4604,
#                    1157.8884, 1176.3217, 1194.7550, 1213.1896, 1231.6240, 1250.0580, 1268.4925, 1286.9270, 1305.3610,
#                    1323.7956, 1342.2299, 1360.6640, 1379.0984, 1397.5347, 1415.9706, 1434.4067, 1452.8430, 1471.2791,
#                    1489.7153, 1508.1514, 1526.5877, 1545.0245, 1557.5954, 1582.7347]
#
# fig = plt.figure(figsize=(6, 4))
# plt.scatter(x, y, label="A36")
# plt.grid()
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.xlabel("Magnetic field strength [A/m]", fontsize=12)
# plt.ylabel("Magnetic field density [T]", fontsize=12)
# plt.legend(fontsize=12)
#
# plt.savefig("media/a36bh", dpi=300)

# i0 = 25
# Nturns = 8  # turns of the coil in one slot [u.]
# nturns = 34  # paralell copper conductors in one turn [u.]
# d_cond = 0.67  # diameter of a copper conductor based on IEC 60217-0-1:2013+AMD1:2019 [m]
# A_cond = (pow(d_cond / 2, 2)) * pi
# coil_area = Nturns * nturns * A_cond
# turn_area = nturns * A_cond
# print(turn_area)
# J20 = i0 / turn_area
# J1 = i0 / coil_area
# print(J1, J20)
# slot_area = 142.793  # area of the slot [m^2]
# fill = coil_area / slot_area
# print(fill)
# print(coil_area)
#
# full = A_cond*272
# fillfull = full / slot_area
# print(fillfull)

