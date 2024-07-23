import matplotlib.pyplot as plt
import numpy as np

from spacial_random import SpacialRandom
from tests import Tests
from linmath import Math
from plots import Plot

def test_isotropic_points(Np: int) -> list:
    points = []

    # generate Np random points in sphere
    for _ in range(0, Np):
        point = SpacialRandom.spherical_point()
        points.append(point)
        print(Math.cartesian_to_polar(point))

    print(f'{len(points)}')
    return points

def verify_plot(points):
    thetas = []
    phis = []
    rs = []

    for p in points:
        theta, phi, r = p
        thetas.append(theta)
        phis.append(phi)
        rs.append(r)
    
    # NOTE(justin): points plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))
    plt.figure(figsize=(5,5))

    for p in points:
        dx, dy, dz = p
        ax.scatter(dx, dy, dz, c='blue', marker='.')

    fig.savefig('points.png')

    # NOTE(justin): verification plots
    fig, axs = plt.subplots(1, 3, tight_layout=True)
    axs[0].hist(thetas, bins=100, color='red')
    axs[1].hist(phis, bins=100, color='green')
    axs[2].hist([], bins=100, color='blue')
    fig.savefig('graph.png')

if __name__ == '__main__':
    # Tests.translation_isotropic()
    Np = 1000
    points = test_isotropic_points(Np);
    verify_plot(points)


