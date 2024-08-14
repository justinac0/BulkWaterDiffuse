import yaml 
from yaml.loader import SafeLoader

import simulation.io.yaml_keys as keys

def write_simulations_files(NT: int, D0: float, dt: float, simulations: list,repeats: int, elapsed_time: str):
    particle_counts = []
    simulation_data = []

    for s in simulations:
        particle_counts.append(s.particle_count)

        simulation_toml = {}
        simulation_toml[f'sim_{s.index}_{s.particle_count}'] = s.as_dict()

        simulation_data.append(simulation_toml)

    particle_counts = [e for e in set(particle_counts)] 
    particle_counts.sort()

    simulation_info = {}
    simulation_info[keys.STEP_COUNT] = NT
    simulation_info[keys.DIFFUSION_COEF] = D0
    simulation_info[keys.TIME_STEP] = dt
    simulation_info[keys.PARTICLE_COUNT] = particle_counts
    simulation_info[keys.REPEATS] = repeats
    simulation_info['elapsed_time'] = elapsed_time

    # write header
    with open('results/data/info.yaml', 'w') as file:
        yaml.dump(simulation_info, file)

    # write individual simulation files
    for s in simulation_data:
        for k, _ in s.items():
            with open(f'results/data/{k}.yaml', 'w') as file:
                yaml.dump(s, file)

def read_yaml_to_object(file_path: str) -> object:
    data = None
    with open(file_path) as file:
        data = yaml.load(file, Loader=SafeLoader)

    return data

def get_simulation_by_info(run: int, NP: int, directory: str) -> object:
    file_name = f'sim_{run}_{NP}'
    data = read_yaml_to_object(f'{directory}/{file_name}.yaml')[f'sim_{run}_{NP}']
    if data == None:
        return data

    return data