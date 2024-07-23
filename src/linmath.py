import math

class Math:
    @staticmethod
    def cartesian_to_polar(point: tuple) -> tuple:
        dx, dy, dz = point

        r = math.sqrt(dx**2 + dy**2 + dz**2)
        theta = math.atan2(dy, dx)
        phi = math.acos(dz / r) 

        return (theta, phi, r)

    @staticmethod
    def polar_to_cartesian(polar: tuple) -> tuple:
        theta, phi, r = polar
        dx = r * math.sin(phi) * math.sin(theta)
        dy = r * math.sin(phi) * math.sin(theta)
        dz = r * math.cos(phi)

        return (dx, dy, dz)
