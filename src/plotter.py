import numpy as np

import matplotlib.pyplot as plt

from sim_math import SimMath

class Plotter:
    @staticmethod
    def uniform_sampling(random_samples: list):
        if len(random_samples) > 1000:
            random_samples = random_samples[:1000]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal', 'box')

        xs = []
        ys = []
        zs = []

        for sample in random_samples:
            x, y, z = SimMath.project_to_sphere_surface(sample)
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
    def verify_any_bias(random_samples: list):
        thetas = []
        phis = []
        rs = []

        for sample in random_samples:
            x, y, z = SimMath.project_to_sphere_surface(sample)
            r, theta, phi = SimMath.cartesian_to_spherical((x, y, z))

            rs.append(r)
            thetas.append(theta)
            phis.append(phi)

        fig, axs = plt.subplots(2, 2)
        fig.set_size_inches(12, 10)
        fig.set_dpi(100)

        # THETAS
        ax = axs[0][0]
        theta_theory = np.linspace(0, np.pi, len(random_samples))
        ax.hist(thetas, bins=30, density=True, alpha=0.6, color='red')
        ax.plot(theta_theory, 0.5 * np.sin(theta_theory), color='black')
        ax.set_title('Observed θ vs. Theoretical θ')
        ax.set_xlabel('θ (Spherical Coord, [0, π])')
        ax.set_ylabel('Counts (bins=30)')

        # PHIS
        ax = axs[0][1]
        phi_theory = np.linspace(0, 2 * np.pi, len(random_samples))
        ax.hist(phis, bins=30, density=True, color='green')
        ax.plot(phi_theory, [1 / (2 * np.pi)] * len(random_samples), color='black')
        ax.set_title('Observed φ vs. Theoretical φ')
        ax.set_xlabel('φ (Spherical Coord, [0, 2π])')
        ax.set_ylabel('Counts (bins=30)')

        ax = axs[1][0]
        # r_theory = np.linspace(0, len(random_samples))
        ax.plot(rs, color='blue')
        # ax[1, 0].plot(r_theory, len(random_samples), color='black')
        ax.set_title('Observed r vs. Theoretical r (INCORRECT)')
        ax.set_xlabel('unknown')
        ax.set_ylabel('unknown')

        plt.savefig(f'results/graphs/verify_any_bias.png')
        plt.show()

    @staticmethod
    def fa(plotting_format):
        keys = plotting_format.keys()

        fig = plt.figure()
        fig.set_size_inches(8, 8)
        plt.title('Fractional Anisotropy (FA)')
        plt.xlabel('Particle Count')
        plt.ylabel('FA')
        for key in keys:
            for data in plotting_format[key]:
                index, particles, diffusion_tensor, eigen_diffusion_tensor, fa = data
                plt.scatter(len(particles), fa, c='blue')

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
                # plt.show()
