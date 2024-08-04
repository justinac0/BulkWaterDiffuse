import yaml 
from yaml.loader import SafeLoader

def write_simulations_file(NT: int, D0: float, dt: float, simulations: list, repeats: int, file_path: str):
    particle_counts = []
    simulation_toml = {}
    for s in simulations:
        particle_counts.append(s.particle_count)
        simulation_toml[f'sim_{s.index}_{s.particle_count}'] = s.as_dict()

    particle_counts = [e for e in set(particle_counts)] 
    particle_counts.sort()

    simulation_toml['NT'] = NT
    simulation_toml['D0'] = D0
    simulation_toml['dt'] = dt
    simulation_toml['counts'] = particle_counts
    simulation_toml['repeats'] = repeats

    data = {
        'version': '0.0.1',
        'production': simulation_toml
    }

    with open(file_path, 'w') as file:
        yaml.dump(data, file)

def read_entry_to_object(file_path: str) -> object:
    data = None
    with open(file_path) as file:
        data = yaml.load(file, Loader=SafeLoader)

    return data['production']


# returns the object inside aggregate yaml object
def get_simulation_info(simulation_object: object, run: int, NP: int):
    data = simulation_object[f'sim_{run}_{NP}']

    return data