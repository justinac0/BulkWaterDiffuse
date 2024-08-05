import yaml 
from yaml.loader import SafeLoader

import simulation.io.yaml_keys as keys

def write_simulations_file(NT: int, D0: float, dt: float, simulations: list,repeats: int, elapsed_time: str, file_path: str):
    particle_counts = []
    simulation_toml = {}
    for s in simulations:
        particle_counts.append(s.particle_count)
        simulation_toml[f'sim_{s.index}_{s.particle_count}'] = s.as_dict()

    particle_counts = [e for e in set(particle_counts)] 
    particle_counts.sort()

    simulation_toml[keys.STEP_COUNT] = NT
    simulation_toml[keys.DIFFUSION_COEF] = D0
    simulation_toml[keys.TIME_STEP] = dt
    simulation_toml[keys.PARTICLE_COUNT] = particle_counts
    simulation_toml[keys.REPEATS] = repeats
    simulation_toml['elapsed_time'] = elapsed_time

    data = {
        'version': '1.0.0',
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
def get_simulation_by_info(simulation_object: object, run: int, NP: int) -> object:
    data = simulation_object[f'sim_{run}_{NP}']

    return data
