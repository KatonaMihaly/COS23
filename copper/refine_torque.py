import numpy as np
import pandas as pd
from numpy import linspace
import json
import matplotlib.pyplot as plt

from digital_twin_distiller import ModelDir

ModelDir.set_base(__file__)

f = open(ModelDir.DATA / f'wp0i25a24_24r1.json')
temp = json.load(f)

df = pd.DataFrame(temp)
df['Angle'] = linspace(-24, 24, 49)

ang_max = df.loc[df['Torque'] == df['Torque'].max()]
print(ang_max)

ang_min = df.loc[df['Torque'] == -(df['Torque'].abs()).min()]
print(ang_min)

# plt.plot(df['Angle'], df['Torque'])
# plt.show()

plt.plot(df['Angle'], temp['Torque'])
plt.show()