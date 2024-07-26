from sim_math import SimMath

class Particle:
    def __init__(self, position: tuple):
        self.position = position

    # random walk in unbiased direction
    def walk(self, D, dt):
        rw_direction = SimMath.projected_surface_spherical_point()
        x, y, z = SimMath.calculate_displacement(D, dt, rw_direction)

        px, py, pz = self.position
        self.position = (px + x, py + y, pz + z)

    # x, y, z
    def get_cartesian_position(self):
        return self.position

    # r, theta, phi
    def get_spherical_position(self):
        return SimMath.cartesian_to_spherical(self.position)