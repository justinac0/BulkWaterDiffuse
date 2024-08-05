import numpy as np

import math

import matplotlib.pyplot as plt

import simulation.math as smath
import simulation.io.yaml_keys as keys

def uniform_sampling(simulation_object: object):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal', 'box')

    ax.ticklabel_format(style='sci', axis='x', scilimits=(-3, 3), useMathText=True)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(-3, 3), useMathText=True)
    ax.ticklabel_format(style='sci', axis='z', scilimits=(-3, 3), useMathText=True)

    xs = []
    ys = []
    zs = []

    for p in simulation_object[keys.PARTICLE_LIST]:
        x = p['x']
        y = p['y']
        z = p['z']

        x, y, z = smath.project_to_sphere_surface((x, y, z))
        xs.append(x)
        ys.append(y)
        zs.append(z)

    ax.set_title('Uniform Sampling Projected On Surface Of Sphere')
    ax.scatter(xs, ys, zs, color='blue', s=1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig(f'results/graphs/uniform_sampling.png')
    plt.show()

def verify_any_bias(simulation_object: object):
    thetas = []
    phis = []
    rs = np.array([])

    for p in simulation_object[keys.PARTICLE_LIST]: # particles in particle lists
        x = p['x']
        y = p['y']
        z = p['z']

        px, py, pz = smath.project_to_sphere_surface((x, y, z))
        _, theta, phi = smath.cartesian_to_spherical((px, py, pz))

        r_length = math.sqrt(x**2 + y**2 + z**2) # from origin (a.k.a simulation start point)
        rs = np.append(rs, r_length)
        thetas.append(theta)
        phis.append(phi)

    fig, axs = plt.subplots(2, 2)
    fig.set_size_inches(12, 10)
    fig.set_dpi(100)

    # THETAS
    ax = axs[0][0]
    theta_theory = np.linspace(0, np.pi, len(thetas))
    ax.hist(thetas, bins=100, color='red', density=True, alpha=0.7)
    ax.plot(theta_theory, 0.5 * np.sin(theta_theory), color='black')
    ax.set_title('Observed θ vs. Theoretical θ')
    ax.set_xlabel('θ (Spherical Coord, [0, π]) (bins=100)')
    ax.set_ylabel('Counts')

    # PHIS
    ax = axs[0][1]
    phi_theory = np.linspace(0, 2 * np.pi, len(phis))
    ax.hist(phis, bins=100, color='green', density=True, alpha=0.7)
    ax.plot(phi_theory, [1 / (2 * np.pi)] * len(phis), color='black')
    ax.set_title('Observed φ vs. Theoretical φ')
    ax.set_xlabel('φ (Spherical Coord, [0, 2π]) (bins=100)')
    ax.set_ylabel('Counts')

    # R
    ax = axs[1][0]
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    ax.hist(rs, bins=100, density=True, color='blue', alpha=0.7)

    ax.set_title('Observed r vs. Theoretical r (bins=100)')
    ax.set_xlabel('r')
    ax.set_ylabel('Counts')

    ax = axs[1][1]
    ax.axis('off')

    plt.savefig(f'results/graphs/verify_any_bias.png')
    plt.show()

def fa(simulation_object: object):
    fig = plt.figure()
    fig.set_size_inches(8, 8)
    plt.title('Fractional Anisotropy (FA)')
    plt.xlabel('1/√NP')
    plt.ylabel('FA')

    xs = np.array([])
    ys = np.array([])

    for counts in simulation_object[keys.PARTICLE_COUNT]:
        sim = simulation_object[f'sim_0_{counts}']
        FA = sim[keys.FRACTIONAL_ANISOTROPY]
        NP = sim[keys.PARTICLE_COUNT]

        x = 1/math.sqrt(NP)
        y = FA

        xs = np.append(xs, x)
        ys = np.append(ys, y)

    plt.scatter(xs, ys, s=3, c='blue')

    a, b = np.polyfit(xs, ys, 1)
    plt.plot(xs, a * xs + b, c='black')

    plt.savefig(f'results/graphs/fa.png')
    plt.show()

def eigens(simulation_object: object):
    fig = plt.figure()
    fig.set_size_inches(8, 8)
    plt.title('Diffusion Tensor Eigen Values')
    plt.xlabel('Particle Count')
    plt.ylabel('Eigen Values')

    for count in simulation_object[keys.PARTICLE_COUNT]:
        D11 = simulation_object[f'sim_0_{count}'][keys.DIFFUSION_TENSOR]['D11']
        D22 = simulation_object[f'sim_0_{count}'][keys.DIFFUSION_TENSOR]['D22']
        D33 = simulation_object[f'sim_0_{count}'][keys.DIFFUSION_TENSOR]['D33']

        plt.scatter([count] * 3, [D11, D22, D33], c='blue')

    plt.savefig(f'results/graphs/eigens.png')
    plt.show()

def diffusion(simulation_object: object):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal', 'box')

    ax.ticklabel_format(style='sci', axis='x', scilimits=(-3, 3), useMathText=True)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(-3, 3), useMathText=True)
    ax.ticklabel_format(style='sci', axis='z', scilimits=(-3, 3), useMathText=True)

    xs = []
    ys = []
    zs = []

    for p in simulation_object[keys.PARTICLE_LIST]:
        x = p['x']
        y = p['y']
        z = p['z']

        xs.append(x)
        ys.append(y)
        zs.append(z)

    ax.set_title('Diffusion of Bulk Water')
    ax.scatter(xs, ys, zs, color='blue', s=1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig(f'results/graphs/diffuse.png')
    plt.show()
