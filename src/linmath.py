import numpy as np

class Math:
    @staticmethod
    def cartesian_to_polar(point: tuple) -> tuple:
        dx, dy, dz = point

        theta = np.atan2(dy, dx)
        phi = np.acos(dz) 
        r = np.sqrt(dx**2 + dy**2 + dz**2)

        return (theta, phi, r)

    @staticmethod
    def polar_to_cartesian(theta, phi, r) -> tuple:
        return (0, 0, 0)
