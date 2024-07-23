import math

class Math:
    @staticmethod
    def cartesian_to_spherical(point: tuple) -> tuple:
        dx, dy, dz = point

        r = math.sqrt(dx**2 + dy**2 + dz**2)
        theta = math.acos(dz / r)
        phi = math.atan2(dy, dx) 
        if phi < 0:
            phi += 2 * math.pi

        return (theta, phi, r)

    @staticmethod
    def spherical_to_cartesian(spherical: tuple) -> tuple:
        theta, phi, r = spherical
        dx = r * math.sin(theta) * math.cos(phi)
        dy = r * math.sin(theta) * math.sin(phi)
        dz = r * math.cos(theta)

        return (dx, dy, dz)
