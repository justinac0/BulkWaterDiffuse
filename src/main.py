# TODO(justin):
#   graphing...

import time
import concurrent.futures

from playsound3 import playsound

import matplotlib as mpl
import matplotlib.pyplot as plt

from simulation import Simulation
from file_data import FileData


def simulation_worker(i: int, NT: int, NP: int, D0: float, dt: float) -> tuple:
    file_path = f'resources/data/{i}_bulk_water_{NT}_{NP}.txt'
    contents = (f'{NP}> Simulation Index: {i+1}\n')

    start = time.time()

    simulation = Simulation(NT, NP, D0, dt)
    simulation_data = simulation.run(i, NP).get()
    _, _, _, diffusion_tensor, eigen_diffusion_tensor, fa = simulation_data

    contents += (f'Simulation Details:\nNT: {NT}\nNP: {NP}\nD0: {D0}\ndt: {dt}\n\nDiffusion Tensor:\n{diffusion_tensor}\n\nDiffusion Tensor Eigen Values:\n{eigen_diffusion_tensor}\n\nFractional Anisotropy:\n{fa}\n')

    end = time.time()

    elapsed = f'{(end - start):.2f}'
    print(f'simulation_worker> [completed]: {i}, {NT}, {NP}, elapsed = {elapsed} seconds')
    contents += f'\n\nelapsed_time: {elapsed} seconds'

    return (simulation_data, FileData(file_path, contents))

def run_parallel(NT: int, NP: list[int], D0: float, dt: float, repeats=3) -> list:
    data = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []

        for particle_count in NP:
            for i in range(0, repeats):
                future = executor.submit(simulation_worker, i, NT, particle_count, D0, dt)
                futures.append(future)

        for f in concurrent.futures.as_completed(futures):
            data.append(f.result())

        concurrent.futures.wait(futures)

    return data

def plot_results():
    pass

def simulate_on_multiple_cores(NT, NP, D0, dt) -> list:
    start = time.time()
    data = run_parallel(NT, NP, D0, dt)
    end = time.time()

    file = open(f'resources/data/time_elapsed.txt', 'w')
    file.write(f'time_elapsed: {end - start} seconds')
    file.close()

    return data

if __name__ == '__main__':
    NT = 300            # steps
    D0 = 2.3 * 10**(-3) # diffusion coefficient
    dt = 5 * 10**(-9)   # time step

    NP = [10, 30, 100, 300, 1000, 3000]#, 10000, 30000, 81910]

    simulation = simulate_on_multiple_cores(NT, NP, D0, dt)
    playsound('resources/audio/water_drop_reverb.mp3')

    xfas = []
    fas = []
    for data, file in simulation:
        index, particle_count, _, diffusion_tensor, eigen_diffusion_tensor, fa = data
        fas.append(fa)
        xfas.append(particle_count)

        with open(file.file_path, 'w') as stream:
            stream.write(file.contents)

    fig, ax = plt.subplots()
    ax.plot(xfas, fas)
    plt.show()
