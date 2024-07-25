import numpy as np

class SimMath:
    @staticmethod
    def cartesian_to_spherical(point: tuple) -> tuple:
        dx, dy, dz = point

        r = np.sqrt(dx**2 + dy**2 + dz**2)
        theta = np.acos(dz / r)
        phi = np.atan2(dy, dx) 
        if phi < 0:
            phi += 2 * np.pi

        return (r, theta, phi)

    @staticmethod
    def spherical_to_cartesian(spherical: tuple) -> tuple:
        theta, phi, r = spherical
        dx = r * np.sin(theta) * np.cos(phi)
        dy = r * np.sin(theta) * np.sin(phi)
        dz = r * np.cos(theta)

        return (dx, dy, dz)
    
    @staticmethod
    def cube_point(xmin: float, xmax: float, ymin: float, ymax: float, zmin: float, zmax: float) -> tuple:
        # generate points in bounds
        dx = np.random.uniform(xmin, xmax)
        dy = np.random.uniform(ymin, ymax)
        dz = np.random.uniform(zmin, zmax)

        return (dx, dy, dz)

    # bounded by a cube of (dx: -1..1, dy: -1..1, dz: -1..1)
    # therefore, radius of 1 sphere is inside said cube.
    # NOTE(justin): should each point be projected to the surface???
    @staticmethod
    def sphere_surface_point() -> tuple:
        point = SimMath.cube_point(-1, 1, -1, 1, -1, 1)
        while not SimMath.is_point_in_sphere(point):
            point = SimMath.cube_point(-1, 1, -1, 1, -1, 1)

        # NOTE(justin): project point to surface of sphere
        # 1. normalize point
        dx, dy, dz = point
        mag = np.sqrt(dx**2 + dy**2 + dz**2)
        surface_projected_point = (dx / mag, dy / mag, dz / mag)

        return surface_projected_point

    def spherical_point(point) -> tuple:
        return SimMath.cartesian_to_spherical(point)

    @staticmethod
    def is_point_in_sphere(point: tuple) -> bool:
        dx, dy, dz = point
        return dx**2 + dy** 2 + dz**2 <= 1

    @staticmethod
    def calculate_fractional_anisotropy(D1, D2, D3):
        Dav = (D1 + D2 + D3) / 3
        numerator = (D1 - Dav)**2 + (D2 - Dav)**2 + (D3 - Dav)**2 
        denumerator = D1**2 + D2**2 + D3**2

        FA = np.sqrt(3/2) * np.sqrt(numerator / denumerator)

        return FA
    
    @staticmethod
    def calculate_displacement(D, dt, point) -> tuple:
        # TODO(justin): vector functions
        dr = np.sqrt(6 * D * dt)
        dx, dy, dz = point

        return (dr * dx, dr * dy, dr * dz)

