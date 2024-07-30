import numpy as np

import math

import matplotlib.pyplot as plt

from particle import Particle
from sim_math import SimMath

import click

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
        ax.scatter(xs, ys, zs, color='blue', s=1, alpha=0.5)
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
        rs = []

        for _, v in particlekv: # NOTE(justin): do we need multiple graphs?
            for p in v: # particles in particle lists
                position = p.position
                x, y, z = SimMath.project_to_sphere_surface(position)
                _, theta, phi = SimMath.cartesian_to_spherical((x, y, z))

                x, y, z = position
                r_length = math.sqrt(x**2 + y**2 + z**2) # from origin (a.k.a simulation start point)
                rs.append(r_length)
                thetas.append(theta)
                phis.append(phi)

        fig, axs = plt.subplots(2, 2)
        fig.set_size_inches(12, 10)
        fig.set_dpi(100)

        # THETAS
        ax = axs[0][0]
        theta_theory = np.linspace(0, np.pi, len(thetas))
        ax.hist(thetas, bins=30, density=True, alpha=0.6, color='red')
        ax.plot(theta_theory, 0.5 * np.sin(theta_theory), color='black')
        ax.set_title('Observed θ vs. Theoretical θ')
        ax.set_xlabel('θ (Spherical Coord, [0, π]) (bins=30)')
        ax.set_ylabel('Counts')

        # PHIS
        ax = axs[0][1]
        phi_theory = np.linspace(0, 2 * np.pi, len(phis))
        ax.hist(phis, bins=30, density=True, color='green')
        ax.plot(phi_theory, [1 / (2 * np.pi)] * len(phis), color='black')
        ax.set_title('Observed φ vs. Theoretical φ')
        ax.set_xlabel('φ (Spherical Coord, [0, 2π]) (bins=30)')
        ax.set_ylabel('Counts')

        # fig = plt.figure()
        #fig.set_size_inches(8, 8)
        #plt.title('Diffusion Tensor Eigen Values')
        #plt.xlabel('Particle Count')
        #plt.ylabel('Eigen Values')
        #for tensor in eigen_diffusion_tensors:
        #    plt.scatter([] * len(eigen_diffusion_tensor), eigen_diffusion_tensor, c='blue')

        # plt.savefig(f'results/graphs/eigens.png')
        # plt.show()

        # R
        ax = axs[1][0]
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.hist(rs, bins=30, density=True, color='yellow')
        # ax.plot(math.exp(-1/(4*D0*NT*dt)), color='black')
        ax.set_title('Observed r vs. Theoretical r (bins=30)')
        ax.set_xlabel('r')
        ax.set_ylabel('Counts')


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
        for key in keys:
            for data in plotting_format[key]:
                index, particles, diffusion_tensor, eigen_diffusion_tensor, fa = data
                plt.scatter(1/math.sqrt(len(particles)), fa, s=3, c='blue')

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

                ax.scatter(xs, ys, zs, s=1, alpha=0.5, c='blue')
                plt.savefig(f'results/graphs/diffusion_{index}_{key}.png')
                plt.show()
