from playsound3 import playsound

import simulation.io.yaml_helper as yamlhelper
import simulation.math as smath
import simulation.parallel.functions as parallel

if __name__ == '__main__':
    NT = 300          # steps
    D0 = 2.3*10**(-3) # diffusion coefficient
    dt = 5*10**(-9)   # time step
    repeats = 3       # how many times each NP simulation will be run

    NP = smath.equidistant_np_space(100, 30000, 250)
    elapsed_time, simulations = parallel.simulate_on_multiple_cores(NT, NP, D0, dt, repeats)
    yamlhelper.write_simulations_files(NT, D0, dt, simulations, repeats, elapsed_time)
    playsound('resources/audio/water_drop_reverb.mp3')
