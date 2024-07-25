from sim_math import SimMath

class Particle:
    def __init__(self, position: tuple):
        self.position = position
    
    def walk(self, D, dt):
        rw_direction = SimMath.sphere_surface_point()
        x, y, z = SimMath.calculate_displacement(D, dt, rw_direction)

        px, py, pz = self.position
        self.position = (px + x, py + y, pz + z)