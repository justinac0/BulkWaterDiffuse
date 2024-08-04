from playsound3 import playsound

import simulation.io.yaml as yamlhelper
import simulation.math as smath
import simulation.parallel.functions as parallel
from simulation.io.yaml import SimKeys

if __name__ == '__main__':
    NT = 300          # steps
    D0 = 2.3*10**(-3) # diffusion coefficient
    dt = 5*10**(-9)   # time step
    repeats = 3       # how many times each NP simulation will be run

    NP = smath.equidistant_np_space(10, 10, 1)

    elapsed_time, simulations = parallel.simulate_on_multiple_cores(NT, NP, D0, dt, repeats)
    # playsound('resources/audio/water_drop_reverb.mp3')

    print(elapsed_time)

    yamlhelper.write_simulations_file(NT, D0, dt, simulations, repeats, 'results/data/simulation.yaml')