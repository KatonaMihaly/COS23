import numpy as np
import pandas as pd
from numpy import linspace
import json
import matplotlib.pyplot as plt

from digital_twin_distiller import ModelDir

ModelDir.set_base(__file__)

locked_12A = []
f = open(ModelDir.DATA / f'i12a0_10r025.json')
temp1 = json.load(f)

f = open(ModelDir.DATA / f'i12a10_30r025.json')
temp2 = json.load(f)

f = open(ModelDir.DATA / f'i12a30_45r025.json')
temp3 = json.load(f)

f = open(ModelDir.DATA / f'i12a45_60r025.json')
temp4 = json.load(f)

f = open(ModelDir.DATA / f'i12a60_90r025.json')
temp5 = json.load(f)

f = open(ModelDir.DATA / f'i12a90_180r025.json')
temp6 = json.load(f)

locked_12A_torque = temp1['Torque'] + temp2['Torque'] + temp3['Torque'] + temp4['Torque'] + temp5['Torque'] + temp6['Torque']
locked_12A_rotor_angle = linspace(0, 180, len(locked_12A_torque))

plt.plot(locked_12A_torque)
# plt.show()

f = open(ModelDir.DATA / f'i25a0_90r025.json')
temp = json.load(f)

plt.plot(temp["Torque"] + temp["Torque"])
plt.show()
