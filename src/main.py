# TODO(justin):
#   units on graphs
#   test suite
#   Simulation class for running bulk water diffuse in triplicate

from sim_math import SimMath
from particle import Particle
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
