import numpy as np

from sim_math import SimMath
from particle import Particle

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
