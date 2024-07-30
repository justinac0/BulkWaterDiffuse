import numpy as np

import math

from scipy.stats import rayleigh
import matplotlib.pyplot as plt

from particle import Particle
from sim_math import SimMath

class Plotter:
    @staticmethod
    def uniform_sampling(plotting_format):
        keys = plotting_format.keys()
        particlekv = []
        for key in keys:
            for data in plotting_format[key]:
                index, ps, _, _, _ = data
                particlekv.append((index, ps))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal', 'box')

        xs = []
        ys = []
        zs = []

        for index, particles in particlekv:
            for p in particles:
                x, y, z = SimMath.project_to_sphere_surface(p.position)
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

    @staticmethod
    def verify_any_bias(plotting_format, D0, NT, dt):
        keys = plotting_format.keys()
        particlekv = []
        eigen_diffusion_tensors = []
        for key in keys:
            for data in plotting_format[key]:
                index, ps, _, eigen_diffusion_tensor, _ = data
                particlekv.append((index, ps))

                eigen_diffusion_tensors.append(eigen_diffusion_tensor)

        thetas = []
        phis = []
        rs = np.array([])

        for _, v in particlekv: # NOTE(justin): do we need multiple graphs?
            for p in v: # particles in particle lists
                position = p.position
                x, y, z = SimMath.project_to_sphere_surface(position)
                _, theta, phi = SimMath.cartesian_to_spherical((x, y, z))

                x, y, z = position
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

    @staticmethod
    def fa(plotting_format):
        keys = plotting_format.keys()

        fig = plt.figure()
        fig.set_size_inches(8, 8)
        plt.title('Fractional Anisotropy (FA)')
        plt.xlabel('1/√NP')
        plt.ylabel('FA')

        xs = np.array([])
        ys = np.array([])
        for key in keys:
            for data in plotting_format[key]:
                index, particles, diffusion_tensor, eigen_diffusion_tensor, fa = data
                x = 1/math.sqrt(len(particles))
                y = fa

                xs = np.append(xs, x)
                ys = np.append(ys, y)

        plt.scatter(xs, ys, s=3, c='blue')

        a, b = np.polyfit(xs, ys, 1)
        plt.plot(xs, a * xs + b, c='black')

        plt.savefig(f'results/graphs/fa.png')
        plt.show()

    @staticmethod
    def eigens(plotting_format):
        keys = plotting_format.keys()

        fig = plt.figure()
        fig.set_size_inches(8, 8)
        plt.title('Diffusion Tensor Eigen Values')
        plt.xlabel('Particle Count')
        plt.ylabel('Eigen Values')
        for key in keys:
            for data in plotting_format[key]:
                _, _, _, eigen_diffusion_tensor, _ = data
                plt.scatter([key] * len(eigen_diffusion_tensor), eigen_diffusion_tensor, c='blue')

        plt.savefig(f'results/graphs/eigens.png')
        plt.show()
    
    @staticmethod
    def diffusion(plotting_format):
        keys = plotting_format.keys()

        for key in keys:
            for data in plotting_format[key]:
                index, particles, _, _, _ = data

                fig = plt.figure()
                fig.set_size_inches(8, 8)
                ax = fig.add_subplot(111, projection='3d')
                ax.set_aspect('equal', 'box')
                ax.set_title(f'Bulk Water Diffusion (run={index}, NP={key})')
                ax.set_xlabel('X (mm)')
                ax.set_ylabel('Y (mm)')
                ax.set_zlabel('Z (mm)')

                xs = []
                ys = []
                zs = []
                for p in particles:
                    x, y, z = p.get_cartesian_position()
                    xs.append(x)
                    ys.append(y)
                    zs.append(z)

                ax.scatter(xs, ys, zs, s=1, c='blue')
                plt.savefig(f'results/graphs/diffusion_{index}_{key}.png')
                plt.show()