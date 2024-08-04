from enum import Enum

import yaml 
from yaml.loader import SafeLoader

# Keys to index simulation yaml...

class SimKeys(str, Enum):
    # Root Keys
    STEP_COUNT = 'NT',
    DIFFUSION_COEF = 'D0',
    TIME_STEP = 'dt',
    REPEATS = 'repeats',

    # Run specific keys
    RUN_INDEX = 'index',
    PARTICLE_COUNT = 'NP',
    DIFFUSION_TENSOR = 'DT'
    FRACTIONAL_ANISOTROPY = 'FA',
    PARTICLE_LIST = 'particle_list'

    def __str__(self) -> str:
        return str(self.value)

def write_simulations_file(NT: int, D0: float, dt: float, simulations: list, repeats: int, file_path: str):
    particle_counts = []
    simulation_toml = {}
    for s in simulations:
        particle_counts.append(s.particle_count)
        simulation_toml[f'sim_{s.index}_{s.particle_count}'] = s.as_dict()

    particle_counts = [e for e in set(particle_counts)] 
    particle_counts.sort()

    simulation_toml[SimKeys.STEP_COUNT] = NT
    simulation_toml[SimKeys.DIFFUSION_COEF] = D0
    simulation_toml[SimKeys.TIME_STEP] = dt
    simulation_toml[SimKeys.PARTICLE_COUNT] = particle_counts
    simulation_toml[SimKeys.REPEATS] = repeats

    data = {
        'production': simulation_toml
    }

    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def read_yaml_to_object(file_path: str) -> object:
    data = None
    with open(file_path) as file:
        data = yaml.load(file, Loader=SafeLoader)

    return data

# returns the object inside aggregate yaml object
def get_simulation_by_info(simulation_object: object, run: int, NP: int):
    data = simulation_object[f'sim_{run}_{NP}']

    return data