import time
import concurrent.futures
import numpy as np

from sim_math import SimMath
from particle import Particle
from file_data import FileData

class SimulationData:
    def __init__(self, particles: list[Particle], diffusion_tensor: list[list[float]], eigen_diffusion_tensor: list[float], fractional_anisotropy: float):
        self.particles              = particles
        self.diffusion_tensor       = diffusion_tensor
        self.eigen_diffusion_tensor = eigen_diffusion_tensor
        self.fractional_anisotropy  = fractional_anisotropy

    # particles, DT, eigen, FA
    def get(self):
        return (self.particles, self.diffusion_tensor, self.eigen_diffusion_tensor, self.fractional_anisotropy)

class Simulation:
    def __init__(self, Nt, Np, D0, dt):
        self.Nt = Nt
        self.Np = Np
        self.D0 = D0
        self.dt = dt
        self.simulation_data = None

    def run(self) -> SimulationData:
        # initialize particles at origin
        particles = []
        for i in range(0, self.Np):
            particles.append(Particle((0, 0, 0)))

        # run random walk
        for step in range(0, self.Nt):
            for p in particles:
                p.walk(self.D0, self.dt)

        # Calculate Diffusion Tensors
        Dxx = 0
        Dxy = 0
        Dxz = 0
        Dyy = 0
        Dyz = 0
        Dzz = 0

        for p in particles:
            xi, yi, zi = p.position
            Dxx += xi * xi
            Dxy += xi * yi
            Dxz += xi * zi
            Dyy += yi * yi
            Dyz += yi * zi
            Dzz += zi * zi

        coefactor = (1 / (2 * self.Nt * self.dt * self.Np))
        DT = np.array([
            [Dxx, Dxy, Dxz],
            [Dxy, Dyy, Dyz],
            [Dxz, Dyz, Dzz]
        ]) * coefactor

        # retrieve eigen values of diffusion tensor
        eigens = np.diag(DT)

        # calculate fractional anisotropy of eigen values
        FA = SimMath.calculate_fractional_anisotropy(Dxx, Dyy, Dzz)

        return SimulationData(particles, DT, eigens, FA)

    @staticmethod
    def static_run(NT, NP, D0, dt) -> str:
        simulation = Simulation(NT, NP, D0, dt)
        _, diffusion_tensor, eigen_diffusion_tensor, fa = simulation.run().get()
        return (f'Simulation Details:\nNT: {NT}\nNP: {NP}\nD0: {D0}\ndt: {dt}\n\nDiffusion Tensor:\n{diffusion_tensor}\n\nDiffusion Tensor Eigen Values:\n{eigen_diffusion_tensor}\n\nFractional Anisotropy:\n{fa}\n')

    # @staticmethod
    # def run_sequential(NT: int, NP: list[int], D0: float, dt: float):
    #     for particle_count in NP:
    #         for i in range(0, 3): # running in triplicate
    #             # output information about current simulation to files...
    #             file = open(f'resources/data/{i}_bulk_water_{NT}_{particle_count}.txt', 'w')
    #             file.write(f'{particle_count}> Simulation Index: {i+1}\n')

    #             start = time.time()
    #             file.write(Simulation.static_run(NT, particle_count, D0, dt))
    #             end = time.time()

    #             file.write(f'time_elapsed: {end - start} seconds')
    #             file.close()

    # @staticmethod
    # def run_parallel(NT: int, NP: list[int], D0: float, dt: float):
    #     def worker(i: int, NT: int, NP: int, D0: float, dt: float, files: list):
    #         file_path = f'resources/data/threaded/{i}_bulk_water_{NT}_{NP}.txt'
    #         contents = (f'{NP}> Simulation Index: {i+1}\n')

    #         start = time.time()
    #         contents += (Simulation.static_run(NT, NP, D0, dt))
    #         end = time.time()

    #         contents += (f'time_elapsed: {end - start} seconds')

    #         file = FileData(file_path, contents)
    #         files.append(file)

    #     files = []
    #     with concurrent.futures.ProcessPoolExecutor() as executor:
    #         futures = []

    #         for particle_count in NP:
    #             for i in range(0, 3): # running in triplicate
    #                 future = executor.submit(worker, i, NT, particle_count, D0, dt, files)
    #                 futures.append(future)

    #         concurrent.futures.wait(futures)

    #     for file in files:
    #         with open(file.file_path, 'w') as stream:
    #             stream.write(file.file_path + '\n')
    #             stream.write(file.contents)