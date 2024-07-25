# TODO(justin):
#   graphing...

import time
from playsound3 import playsound

from simulation import Simulation
from file_data import FileData

import concurrent.futures

def simulation_worker(i, NT, NP, D0, dt) -> tuple:
    file_path = f'resources/data/{i}_bulk_water_{NT}_{NP}.txt'
    contents = (f'{NP}> Simulation Index: {i+1}\n')

    start = time.time()
    simulation = Simulation(NT, NP, D0, dt)
    simulation_data = simulation.run().get()

    _, diffusion_tensor, eigen_diffusion_tensor, fa = simulation_data

    contents += (f'''Simulation Details:\nNT: {NT}\n
                    NP: {NP}\nD0: {D0}\n
                    dt: {dt}\n\n
                    Diffusion Tensor:\n{diffusion_tensor}\n\n
                    Diffusion Tensor Eigen Values:\n{eigen_diffusion_tensor}\n\n
                    Fractional Anisotropy:\n{fa}\n''')

    contents += (Simulation.static_run(NT, NP, D0, dt))
    end = time.time()

    elapsed = (f'time_elapsed: {end - start} seconds')
    print(f'FINISHED: {i}, {NT}, {NP}, {elapsed}')
    contents += elapsed

    return (simulation_data, FileData(file_path, contents))

def run_parallel(NT: int, NP: list[int], D0: float, dt: float, repeats=1):
    data = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = []

        for particle_count in NP:
            for i in range(0, repeats):
                future = executor.submit(simulation_worker, i, NT, particle_count, D0, dt)
                futures.append(future)

        for f in concurrent.futures.as_completed(futures):
            data.append(f.result())

        concurrent.futures.wait(futures)

    return data

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

    NP = [10, 30, 100, 300, 1000, 3000, 10000, 30000]

    _, files = simulate_on_multiple_cores(NT, NP, D0, dt)

    for file in files:
        with open(file.file_path, 'w') as stream:
            stream.write(file.contents)
