import numpy as np
import pandas as pd
from numpy import linspace
import json
import matplotlib.pyplot as plt

from digital_twin_distiller import ModelDir

ModelDir.set_base(__file__)

f = open(ModelDir.DATA / f'wp0i12a0_90r025.json')
temp = json.load(f)

df = pd.DataFrame(temp)
df['Angle'] = linspace(0, 90, 361)

ang_max = df.loc[df['Torque'] == df['Torque'].max()]
print(ang_max)

ang_min = df.loc[df['Torque'] == -(df['Torque'].abs()).min()]
print(ang_min)

# plt.plot(df['Angle'], df['Torque'])
# plt.show()

f = open(ModelDir.DATA / f'wp0i35a0_90r025.json')
temp = json.load(f)
plt.plot(df['Angle'], temp['Torque'])
plt.show()