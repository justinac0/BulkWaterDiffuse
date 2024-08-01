# TODO(justin): create individual graphs for runs then one graph with all data on it....
# TODO(justin): make everything that touches math be numpy please :D

import time
import concurrent.futures
import yaml 
from yaml.loader import SafeLoader

from playsound3 import playsound

import numpy as np
import matplotlib.pyplot as plt

from sim_math import SimMath
from plotter import Plotter
from simulation import Simulation, SimulationData

def simulation_worker(i: int, NT: int, NP: int, D0: float, dt: float) -> SimulationData:
    start = time.time()
    simulation = Simulation(i, NT, NP, D0, dt)
    simulation_data = simulation.run(i)
    end = time.time()

    elapsed = f'{(end - start):.2f}'
    print(f'simulation_worker> [completed]: {i}, {NT}, {NP}, elapsed = {elapsed} seconds')

    return simulation_data

def run_parallel(NT: int, NP: list[int], D0: float, dt: float, repeats: int) -> list:
    data = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        futures = []

        for particle_count in NP:
            for i in range(0, repeats):
                future = executor.submit(simulation_worker, i, NT, particle_count, D0, dt)
                futures.append(future)

        for f in concurrent.futures.as_completed(futures):
            data.append(f.result())

        concurrent.futures.wait(futures)

    return data

def simulate_on_multiple_cores(NT: int, NP: list[int], D0: float, dt: float, repeats) -> tuple:
    start = time.time()
    data = run_parallel(NT, NP, D0, dt, repeats)
    end = time.time()

    return (f'time_elapsed: {end - start} seconds', data)

def write_simulations_to_yaml(NT: int, D0: float, dt: float, simulations: list):
    particle_counts = []
    simulation_toml = {}
    for s in simulations:
        particle_counts.append(s.particle_count)
        simulation_toml[f'sim_{s.index}_{s.particle_count}'] = s.as_dict()

    particle_counts = [e for e in set(particle_counts)] 
    particle_counts.sort()

    simulation_toml['particle_counts'] = particle_counts
    simulation_toml['NT'] = NT
    simulation_toml['D0'] = D0
    simulation_toml['dt'] = dt

    data = {
        'version': '0.0.1',
        'production': simulation_toml
    }

    with open('results/data/simulation.yaml', 'w') as file:
        yaml.dump(data, file)

def read_yaml_to_object(file_path: str) -> object:
    data = None
    with open(file_path) as file:
        data = yaml.load(file, Loader=SafeLoader)

    return data['production']

# returns the object inside aggregate yaml object
def get_simulation_info(simulation_object: object, run: int, NP: int):
    data = simulation_object[f'sim_{run}_{NP}']

    return data

if __name__ == '__main__':
    NT = 300          # steps
    D0 = 2.3*10**(-3) # diffusion coefficient
    dt = 5*10**(-9)   # time step

    NP = SimMath.equidistant_np_space(10, 1000, 100)

    # TODO(justin): simulation related functions should be in their own module...
    elapsed_time, simulations = simulate_on_multiple_cores(NT, NP, D0, dt, repeats=3)
    playsound('resources/audio/water_drop_reverb.mp3')

    print(elapsed_time)

    write_simulations_to_yaml(NT, D0, dt, simulations)

    simulation_object = read_yaml_to_object('results/data/simulation.yaml')

    plt.style.use('seaborn-v0_8-muted')

    specific_run = get_simulation_info(simulation_object, 0, 1000)

    Plotter.uniform_sampling(specific_run)
    Plotter.verify_any_bias(specific_run)
    Plotter.fa(simulation_object)
    Plotter.eigens(simulation_object)
    Plotter.diffusion(specific_run)