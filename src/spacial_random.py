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

    # bounded by a cube of (dx: -1..1, dy: -1..1, dz: -1..1)
    # therefore, radius of 1 sphere is inside said cube.
    # NOTE(justin): should each point be projected to the surface???
    @staticmethod
    def spherical_point() -> tuple:
        origin = (0, 0, 0)
        point = SpacialRandom.cube_point(-1, 1, -1, 1, -1, 1)
        while not SpacialRandom.is_point_in_sphere(point, 1):
            print('point is outside sphere... re-generating point...')
            point = SpacialRandom.cube_point(-1, 1, -1, 1, -1, 1)

        # NOTE(justin): project point to surface of sphere
        # 1. normalize point
        # 2. presto
        
        # TODO(justin): write vector math functions in linmath...
        #dx, dy, dz = point
        #mag = np.sqrt(dx**2 + dy**2 + dz**2)
        #surface_projected_point = (dx / mag, dy / mag, dz / mag)

        #print(f'point in sphere was generated: {dx / mag}, {dy / mag}, {dz / mag}')

        return point
        #return surface_projected_point

    @staticmethod
    def is_point_in_sphere(point: tuple, radius: float) -> bool:
        # deconstruct point into components
        dx, dy, dz = point
        return dx**2 + dy ** 2 + dz **2 <= 1

