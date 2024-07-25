from particle import Particle

class SimulationData:
    def __init__(self, particles: list<Particle>, diffusion_tensor: list<list<float>>, eigen_diffusion_tensor: list<float>):
        self.particles              = particles
        self.diffusion_tensor       = diffusion_tensor
        self.eigen_diffusion_tensor = eigen_diffusion_tensor
    
    def get(self):
        return (self.particles, self.diffusion_tensor, self.eigen_diffusion_tensor)

class Simulation:
    def __init__(self, Nt, Np, D0, dt):
        self.Nt = Nt
        self.Np = Np
        self.D0 = D0
        self.dt = dt
        self.simulation_data = None

    def run():
        pass