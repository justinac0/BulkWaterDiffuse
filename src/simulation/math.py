import numpy as np
from simulation.particle import Particle
from simulation.collagen import CollagenNetwork

def cartesian_to_spherical(point: tuple) -> tuple:
    dx, dy, dz = point

    r = np.sqrt(dx**2 + dy**2 + dz**2)
    theta = np.acos(dz)
    phi = np.atan2(dy, dx) 
    if phi < 0:
        phi += 2 * np.pi

    return (r, theta, phi)

def spherical_to_cartesian(spherical: tuple) -> tuple:
    r, theta, phi = spherical
    dx = r * np.sin(theta) * np.cos(phi)
    dy = r * np.sin(theta) * np.sin(phi)
    dz = r * np.cos(theta)

    return (dx, dy, dz)

def is_point_in_sphere(point: tuple) -> bool:
    x, y, z = point
    return x**2 + y** 2 + z**2 <= 1

def cube_point(xmin: float, xmax: float, ymin: float, ymax: float, zmin: float, zmax: float) -> tuple:
    # generate points in bounds
    dx = np.random.uniform(xmin, xmax)
    dy = np.random.uniform(ymin, ymax)
    dz = np.random.uniform(zmin, zmax)

    return (dx, dy, dz)

def project_to_sphere_surface(point) -> tuple:
    x, y, z = point
    mag = np.sqrt(x**2 + y**2 + z**2)
    surface_projected_point = (x / mag, y / mag, z / mag)

    return surface_projected_point

def spherical_point() -> tuple:
    point = cube_point(-1, 1, -1, 1, -1, 1)
    while not is_point_in_sphere(point):
        point = cube_point(-1, 1, -1, 1, -1, 1)

    return point

def projected_surface_spherical_point() -> tuple:
    return project_to_sphere_surface(spherical_point())

def calculate_fractional_anisotropy(D1, D2, D3):
    Dav = (D1 + D2 + D3) / 3
    numerator = (D1 - Dav)**2 + (D2 - Dav)**2 + (D3 - Dav)**2 
    denumerator = D1**2 + D2**2 + D3**2

    FA = np.sqrt(3/2) * np.sqrt(numerator / denumerator)

    return FA

def calculate_displacement(D, dt, point) -> tuple:
    # TODO(justin): vector functions
    dr = np.sqrt(6 * D * dt)
    dx, dy, dz = point

    return (dr * dx, dr * dy, dr * dz)

def generate_uniform_points(N: int) -> list:
    points = []

    for _ in range(N):
        cartesian = spherical_point()
        points.append(cartesian)

    return points

def is_in_collagen_network() -> bool:
    return False

def equidistant_np_space(min, max, N):
    # transform max and min into 1/sqrt(N) space
    linMin = np.power(min, -0.5)
    linMax = np.power(max, -0.5)

    # get equidistant points
    space = np.linspace(linMin, linMax, N)

    # transform back to N space
    return np.power(space, -2).astype(int)

def is_point_in_collagen_network(x, y, network: CollagenNetwork) -> bool:
    # Relative x-y positions of collagen fiber centers (offset from center)
    Rx = x / network.L - 0.5
    Ry = y / network.L - 0.5

    # Integer fiber positions (Cx, Cy) -> (col, row)
    Cx = np.floor(Rx)
    dx = Rx - Cx
    if dx > 0.5:
        Cx = np.ceil(Rx)

    Cy = np.floor(Ry)
    dy = Ry - Cy
    if dy > 0.5:
        Cy = np.ceil(Ry)

    # Distance to center of collagen fiber
    dist = np.sqrt((Rx - Cx)**2 + (Ry - Cy)**2)

    # Relative collagen fiber radius
    tr = (network.r) / network.L

    return dist < tr

