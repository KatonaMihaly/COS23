import json
from multiprocessing import Pool
from itertools import product
from numpy import linspace

from digital_twin_distiller.encapsulator import Encapsulator
from digital_twin_distiller.modelpaths import ModelDir
from digital_twin_distiller.simulationproject import sim
from model_copper_wound import SzEReluctanceMotor

def execute_model(model: SzEReluctanceMotor):
    return model(timeout=2000, cleanup=True).get("Torque", 0.0)

@sim.register('sim')
def avg(model, modelparams, simparams, miscparams):

    models = [model(I0=250)]
    with Pool() as pool:
        res = pool.map(execute_model, models)

    result = {'Torque': list(res)}

    with open(ModelDir.DATA / f'test.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=True)

    return result

if __name__ == "__main__":
    ModelDir.set_base(__file__)

    # set the model for the simulation
    sim.set_model(SzEReluctanceMotor)

    model = Encapsulator(sim)
    model.port = 8080
    model.run()
