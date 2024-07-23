import numpy as np

class SpacialRandom:
    def __init__(self):
        pass

    @staticmethod
    def cube_point(xmin: float, xmax: float, ymin: float, ymax: float, zmin: float, zmax: float) -> tuple:
        # generate points in bounds
        dx = np.random.uniform(xmin, xmax)
        dy = np.random.uniform(ymin, ymax)
        dz = np.random.uniform(zmin, zmax)

        return (dx, dy, dz)

    @staticmethod
    def is_point_in_sphere(point: tuple, radius: float) -> bool:
        # deconstruct point into components
        dx, dy, dz = point
        return dx**2 + dy ** 2 + dz **2 <= 1

