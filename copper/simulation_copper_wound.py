import json
from multiprocessing import Pool
from numpy import linspace

from digital_twin_distiller.encapsulator import Encapsulator
from digital_twin_distiller.modelpaths import ModelDir
from digital_twin_distiller.simulationproject import sim
from model_copper_wound import SzEReluctanceMotor

def execute_model(model: SzEReluctanceMotor):
    return model(timeout=10000, cleanup=True).get("Torque", 0.0)

@sim.register('static')
def avg(model, modelparams, simparams, miscparams):
    list = linspace(0, 90, 361)
    models = [model(I0=45, rotor_angle=i) for i in list]
    with Pool() as pool:
        res = pool.map(execute_model, models)

    result = {'Torque': res}

    with open(ModelDir.DATA / f'wp0i45a0_90r025.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=True)

    return result

@sim.register('rotating')
def avg(model, modelparams, simparams, miscparams):
    a = 0
    b = 30
    c = 121
    x = 61.25
    rot = linspace(a + x, b + x, c)
    alp = linspace(a, -b*2, c)
    models = [model(I0=12, rotor_angle=i, alpha=j) for i, j in zip(rot, alp)]
    with Pool() as pool:
        res = pool.map(execute_model, models)

    result = {'Torque': res}

    with open(ModelDir.DATA / f'i12a0_30t61r025.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=True)

    return result

if __name__ == "__main__":
    ModelDir.set_base(__file__)

    # set the model for the simulation
    sim.set_model(SzEReluctanceMotor)

    model = Encapsulator(sim)
    model.port = 8080
    model.run()
