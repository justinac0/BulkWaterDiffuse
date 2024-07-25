# TODO(justin):
#   units on graphs
#   clean up code (restructure/refactor bad function names and plotting code)
#   test suite
#   generate diffusion tensor from final data
#   Simulation class for running bulk water diffuse in triplicate

# import matplotlib.pyplot as plt
# import numpy as np
# import math

from sim_math import SimMath
from walk import Particle
from simulation import Simulation

if __name__ == '__main__':
    NT = 200
    NP = 100

    D0 = 2.3 * 10**(-3)
    dt = 5 * 10**(-9)

    sim1 = Simulation(NT, NP, D0, dt)
    data = sim1.run()
    _, diffusion_tensor, eigen_diffusion_tensor, fa = data.get()
    print(f'{eigen_diffusion_tensor}\n{fa}')
