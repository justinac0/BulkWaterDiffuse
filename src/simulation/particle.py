import simulation.math as smath
from simulation.collagen import CollagenNetwork

network = CollagenNetwork(0.3, 1)

class Particle:
    def __init__(self, position: tuple):
        self.position = position

    # random walk in unbiased direction
    def walk(self, D0: float, dt: float):
        rw_direction = smath.projected_surface_spherical_point()
        x, y, z = smath.calculate_displacement(D0, dt, rw_direction)

        px, py, pz = self.position
        nx = px + x
        ny = py + y
        nz = pz + z

        # simulate the collagen network
        if smath.is_point_in_collagen_network(nx, ny, network):
           return 

        self.position = (nx, ny, nz)

    # x, y, z
    def get_cartesian_position(self):
        return self.position

    # r, theta, phi
    def get_spherical_position(self):
        return smath.cartesian_to_spherical(self.position)
