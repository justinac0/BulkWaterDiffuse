import time
import concurrent.futures
from simulation.core import Simulation, SimulationData

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