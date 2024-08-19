from playsound3 import playsound

import simulation.math as smath
import simulation.io.yaml_helper as yamlhelper
import simulation.parallel.functions as parallel
import initial_conditions as ic

if __name__ == '__main__':
    NP = smath.equidistant_np_space(ic.min_particles, ic.max_particles, ic.iterations)
    elapsed_time, simulations = parallel.simulate_on_multiple_cores(ic.NT, NP, ic.D0, ic.dt, ic.repeats)
    yamlhelper.write_simulations_files(ic.NT, ic.D0, ic.dt, simulations, ic.repeats, elapsed_time)
    playsound('resources/audio/water_drop_reverb.mp3')

