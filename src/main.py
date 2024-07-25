# TODO(justin):
#   graphing...

import time
from playsound3 import playsound

from simulation import Simulation

def simulate_on_single_core(NT: int, NP: list[int], D0: float, dt: float):
    start = time.time()
    Simulation.run_sequential(NT, NP, D0, dt)
    end = time.time()

    file = open(f'resources/data/time_elapsed.txt', 'w')
    file.write(f'time_elapsed: {end - start} seconds')
    file.close()

    playsound('resources/audio/water_drop_reverb.wav')

def simulate_on_multiple_cores(NT: int, NP: list[int], D0: float, dt: float):
    start = time.time()
    Simulation.run_parallel(NT, NP, D0, dt)
    end = time.time()

    file = open(f'resources/data/time_elapsed.txt', 'w')
    file.write(f'time_elapsed: {end - start} seconds')
    file.close()

    playsound('resources/audio/water_drop_reverb.wav')

if __name__ == '__main__':
    NT = 300            # steps
    D0 = 2.3 * 10**(-3) # diffusion coefficient
    dt = 5 * 10**(-9)   # time step

    NP = [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000]

    # simulate_on_single_core(NT, NP, D0, dt) # multiple cores almost always faster
    simulate_on_multiple_cores(NT, NP, D0, dt)
