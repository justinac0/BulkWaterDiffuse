# TODO(justin):
#   units on graphs
#   test suite
#   Simulation class for running bulk water diffuse in triplicate

from sim_math import SimMath
from particle import Particle
from simulation import Simulation
import file_io

if __name__ == '__main__':
    NT = 300            # steps
    D0 = 2.3 * 10**(-3) # diffusion coefficient
    dt = 5 * 10**(-9)   # time step

    NP = [10, 30, 100, 300] # 1000, 3000, 10000, 30000
    for particle_count in NP:
        for i in range(0, 3): # running in triplicate
            print(f'{particle_count}> Simulation Index: {i+1}')
            Simulation.static_run(particle_count, particle_count, D0, dt)

    # file_io.write_csv('test.csv', [])