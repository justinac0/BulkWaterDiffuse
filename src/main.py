# TODO(justin): rework how we gather info for repeated tests... all test data needs to be placed in toml on simulation completion
# TODO(justin): create individual graphs for runs then one graph with all data on it....
# TODO(justin): make everything that touches math be numpy please :D

import time
import concurrent.futures

from playsound3 import playsound

import matplotlib.pyplot as plt

from sim_math import SimMath
from plotter import Plotter
from simulation import Simulation, SimulationData

def simulation_worker(i: int, NT: int, NP: int, D0: float, dt: float) -> SimulationData:
    start = time.time()
    simulation = Simulation(NT, NP, D0, dt)
    data = simulation.run(i).get()
    end = time.time()

    elapsed = f'{(end - start):.2f}'
    print(f'simulation_worker> [completed]: {i}, {NT}, {NP}, elapsed = {elapsed} seconds')

    return data

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

def simulate_on_multiple_cores(NT: int, NP: list[int], D0: float, dt: float, repeats=3) -> list:
    start = time.time()
    data = run_parallel(NT, NP, D0, dt, repeats)
    end = time.time()

    file = open(f'results/data/time_elapsed.txt', 'w')
    file.write(f'time_elapsed: {end - start} seconds')
    file.close()

    return data

def simulation_as_plotting_format(simulations: list):
    plotting_format = {}

    for simulation in simulations:
        index, particles, diffusion_tensor, eigen_diffusion_tensor, fa = simulation

        key = len(particles)
        payload = (index, particles, diffusion_tensor, eigen_diffusion_tensor, fa)

        if not plotting_format.get(key):
            plotting_format.setdefault(key, [payload])
        else:
            plotting_format[key].append(payload)

    return plotting_format

if __name__ == '__main__':
    NT = 300          # steps
    D0 = 2.3*10**(-3) # diffusion coefficient
    dt = 5*10**(-9)   # time step

    NP = SimMath.equidistant_np_space(10, 10000, 5)

    # TODO(justin): simulation related functions should be in their own module...
    simulation = simulate_on_multiple_cores(NT, NP, D0, dt, repeats=3)
    # playsound('resources/audio/water_drop_reverb.mp3')

    # TODO(justin): If time permits; rework simulation plotting format...
    plotting_format = simulation_as_plotting_format(simulation)

    plt.style.use('seaborn-v0_8-muted')
    # Plotter.uniform_sampling(plotting_format)
    Plotter.verify_any_bias(plotting_format, D0, NT, dt)
    # Plotter.fa(plotting_format)
    # Plotter.eigens(plotting_format)
    # Plotter.diffusion(plotting_format)