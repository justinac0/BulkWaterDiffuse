import numpy as np
from spacial_random import SpacialRandom

class Particle:
    def __init__(self, position):
        self.position = position

    def walk(self):
        sx, sy, sz = SpacialRandom.spherical_point()
        dx, dy, dz = self.position

        self.position = (dx + sx, dy + sy, dz + sz)

class Walk:
    @staticmethod
    def calculate_displacement(D, dt, point):
        # TODO(justin): vector functions
        dr = np.sqrt(6 * D * dt)
        dx, dy, dz = point

        return  (dr * dx, dr * dy, dr * dz)
