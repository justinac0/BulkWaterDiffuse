import matplotlib.pyplot as plt
import numpy as np

from spacial_random import SpacialRandom
from tests import Tests
from linmath import Math

def test_isotropic_points(Np: int) -> []:
    points = []

    # generate Np random points in sphere
    for i in range(0, Np):
        point = SpacialRandom.spherical_point()
        points.append(point)
        print(Math.cartesian_to_polar(point))
        #print('new point generated...')

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

    plt.hist(thetas, 100)
    plt.savefig('thetas.png')

    plt.hist(phis, 100)
    plt.savefig('phis.png')

if __name__ == '__main__':
    # Tests.translation_isotropic()
    Np = 10000
    points = test_isotropic_points(Np);
    verify_plot(points)

