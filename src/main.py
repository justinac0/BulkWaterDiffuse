import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import statistics

from spacial_random import SpacialRandom
from tests import Tests
from linmath import Math
from plots import Plot

def test_isotropic_points(Np: int) -> list:
    points = []

    # generate Np random points in sphere
    for _ in range(0, Np):
        point = SpacialRandom.sphere_surface_point()
        points.append(SpacialRandom.spherical_point(point))

    return points

def verify_plot(points):
    thetas = []
    phis = []
    rs = []
    cpoints = []

    for p in points:
        theta, phi, r = p
        print(p)
        thetas.append(theta)
        phis.append(phi)
        rs.append(r)
        cpoints.append(Math.spherical_to_cartesian(p))

    # NOTE(justin): points plot
    # NOTE(justin): very slow to generate... only generate for report
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = []
    ys = []
    zs = []
    for x, y, z in cpoints:
        xs.append(x)
        ys.append(y)
        zs.append(z)

    ax.scatter(xs, ys, zs, color='blue', s=1, alpha=0.6)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

    # # NOTE(justin): verification plots
    plt.hist(thetas, bins=30, density=True, alpha=0.6, color='red')
    theta_theory = np.linspace(0, np.pi, len(points))
    plt.plot(theta_theory, 0.5 * np.sin(theta_theory))
    plt.show()

    plt.hist(phis, bins=30, density=True, color='green')
    phi_theory = np.linspace(0, 2 * np.pi, len(points))
    plt.plot(phi_theory, [1 / (2 * np.pi)] * len(points))
    plt.show()

    plt.plot(rs, color='blue')
    plt.show()

if __name__ == '__main__':
    Np = 10000
    points = test_isotropic_points(Np)
    verify_plot(points)
