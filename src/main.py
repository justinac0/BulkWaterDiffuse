# TODO(justin):
#   units on graphs
#   test suite

import time
import threading
import logging

from playsound3 import playsound

from sim_math import SimMath
from particle import Particle
from simulation import Simulation
import file_io

import concurrent.futures

def run_data_collection(NT: int, NP: list[int], D0: float, dt: float):
    for particle_count in NP:
        for i in range(0, 3): # running in triplicate
            # output information about current simulation to files...
            file = open(f'resources/data/{i}_bulk_water_{NT}_{particle_count}.txt', 'w')
            file.write(f'{particle_count}> Simulation Index: {i+1}\n')

            start = time.time()
            file.write(Simulation.static_run(NT, particle_count, D0, dt))
            end = time.time()

            file.write(f'time_elapsed: {end - start} seconds')
            file.close()

            print(f'1{i}: file written...')

if __name__ == '__main__':
    NT = 300            # steps
    D0 = 2.3 * 10**(-3) # diffusion coefficient
    dt = 5 * 10**(-9)   # time step

    NP = [10, 30, 100, 300, 1000, 3000]
 
    start = time.time()
    run_data_collection(NT, NP, D0, dt)
    end = time.time()

    file = open(f'resources/data/time_elapsed.txt', 'w')
    file.write(f'time_elapsed: {end - start} seconds')
    file.close()

    playsound('resources/audio/water_drop_reverb.wav')
