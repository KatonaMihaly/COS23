import numpy as np
import pandas as pd
from numpy import linspace
import json
import matplotlib.pyplot as plt

from digital_twin_distiller import ModelDir

ModelDir.set_base(__file__)

f1 = open(ModelDir.DATA / f'H_wp0i35a24_24r025l70_22,5.json')

temp1 = json.load(f1)

df1 = pd.DataFrame(f1)
df1['Angle'] = linspace(1, 48, 25)

plt.plot(df1['Angle'], temp1['Torque'])


plt.yticks(fontsize=12)
plt.xlabel('Rotor position [deg]', fontsize=12)
plt.ylabel('Torque [Nm]', fontsize=12)
plt.grid()
plt.legend()
plt.savefig('media/half.png', dpi=300)
plt.show()