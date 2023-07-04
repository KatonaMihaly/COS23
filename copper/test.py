stacklenght = [
    69.45,
    69.14,
    68.35,
    68.07,
    68.31,
    68.80,
    71.47,
    70.80,
    71.42,
    72.44,
    70.61,
    69.20,
    68.52,
    68.62,
    68.86,
    69.54,
    71.52,
    69.70,
    68.59,
    68.37,
    67.70,
    67.63,
    68.61,
    69.11,
    69.75,
    69.65,
    68.97,
    67.98,
    68.00,
    69.03,
    69.89,
    70.37,
    70.92,
    70.77,
    69.95,
    69.50,
    68.28,
    68.04,
    68.59,
    68.96,
    69.37,
    68.80,
    68.50,
    68.32,
    68.19,
    67.87,
    68.25,
    68.62
]

# Python program to get average of a list
def Average(lst):
    return sum(lst) / len(lst)

    # Driver Code
    lst = [15, 9, 55, 41, 35, 20, 62, 49]
    average = Average(lst)

    # Printing average of the list
    print("Average of the list =", round(average, 2))

print(Average(stacklenght))

from numpy import linspace
a = 0
b = 30
c = 121
rot = linspace(a+61, b+61, c)
alp = linspace(a, -b*2, c)
print(list(zip(rot, alp)))
print(len(list(zip(rot, alp))))

# temp0 = list(linspace(0, 90, 361))
# angle = temp0 * 2
# temp1 = [25] * len(temp0)
# temp2 = [50] * len(temp0)
# current = temp1 + temp2
# print(list(zip(current, angle)))
#
# print(len(current))
