import numpy as np

from sim_math import SimMath
from particle import Particle

class SimulationData:
    def __init__(self, index: int, particles: list[Particle], diffusion_tensor: list[list[float]], fractional_anisotropy: float):
        self.index                  = index
        self.particle_count         = len(particles)
        self.particles              = particles
        self.diffusion_tensor       = diffusion_tensor
        self.fractional_anisotropy  = fractional_anisotropy

    def as_dict(self) -> dict:
        # convert particle positions to yaml
        particles_yaml = []
        for p in self.particles:
            x, y, z = p.position

            # convert numpy types to normal python types :)
            inner_yaml = {'x': float(x), 'y': float(y), 'z': float(z)}
            particles_yaml.append(inner_yaml)

        # convert diffusion tensor values into yaml
        diffusion_tensor_yaml = {} 
        row_idx = 0
        for row in self.diffusion_tensor:
            col_idx = 0
            for col in row:
                diffusion_tensor_yaml[f'D{row_idx}{col_idx}'] = float(col)
                col_idx += 1

            row_idx += 1

        particle_count = len(self.particles)
        simulation_yaml = {
                'run_index': self.index,
                'particle_count': particle_count,
                'particles': particles_yaml,
                'diffusion_tensor': diffusion_tensor_yaml,
                'fractional_anisotropy': float(self.fractional_anisotropy)
        }

        return simulation_yaml

class Simulation:
    def __init__(self, index, Nt, Np, D0, dt):
        self.index = index
        self.Nt = Nt
        self.Np = Np
        self.D0 = D0
        self.dt = dt
        self.simulation_data = None

    # negative index or particle count just means that this data isn't tracked
    def run(self, index) -> SimulationData:
        # initialize particles at origin
        particles = []
        for i in range(0, self.Np):
            particles.append(Particle((0, 0, 0)))

        # run random walk
        for _ in range(0, self.Nt):
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
        diffusion_tensor = np.array([
            [Dxx, Dxy, Dxz],
            [Dxy, Dyy, Dyz],
            [Dxz, Dyz, Dzz]
        ]) * coefactor


        # calculate fractional anisotropy of eigen values
        FA = SimMath.calculate_fractional_anisotropy(Dxx, Dyy, Dzz)

        return SimulationData(index, particles, diffusion_tensor, FA)
