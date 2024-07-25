# TODO(justin):
#   graphing...

import time
from playsound3 import playsound

from simulation import Simulation
from file_data import FileData

import concurrent.futures

def simulation_worker(i, NT, NP, D0, dt) -> FileData:
    file_path = f'resources/data/{i}_bulk_water_{NT}_{NP}.txt'
    contents = (f'{NP}> Simulation Index: {i+1}\n')

    start = time.time()
    contents += (Simulation.static_run(NT, NP, D0, dt))
    end = time.time()

    contents += (f'time_elapsed: {end - start} seconds')

    return FileData(file_path, contents)

def run_parallel(NT: int, NP: list[int], D0: float, dt: float):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files = []
        futures = []

        for particle_count in NP:
            for i in range(0, 3): # running in triplicate
                future = executor.submit(simulation_worker, i, NT, particle_count, D0, dt)
                futures.append(future)

        for f in concurrent.futures.as_completed(futures):
            files.append(f.result())

        concurrent.futures.wait(futures)

        for file in files:
            with open(file.file_path, 'w') as stream:
                stream.write(file.contents)

def simulate_on_multiple_cores(NT, NP, D0, dt):
    start = time.time()
    run_parallel(NT, NP, D0, dt)
    end = time.time()

    file = open(f'resources/data/time_elapsed.txt', 'w')
    file.write(f'time_elapsed: {end - start} seconds')
    file.close()

    playsound('resources/audio/water_drop_reverb.wav')

if __name__ == '__main__':
    NT = 300            # steps
    D0 = 2.3 * 10**(-3) # diffusion coefficient
    dt = 5 * 10**(-9)   # time step

    NP = [10, 30, 100]

    simulate_on_multiple_cores(NT, NP, D0, dt)