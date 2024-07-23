import numpy as np
from spacial_random import SpacialRandom

class Particle:
    def __init__(self, position):
        self.position = position

    def walk(self, D, dt):
        x, y, z = Walk.calculate_displacement(D, dt, SpacialRandom.sphere_surface_point())

        px, py, pz = self.position
        self.position = (px + x, py + y, pz + z)

class Walk:
    @staticmethod
    def calculate_displacement(D, dt, point) -> tuple:
        # TODO(justin): vector functions
        dr = np.sqrt(6 * D * dt)
        dx, dy, dz = point

        return (dr * dx, dr * dy, dr * dz)
