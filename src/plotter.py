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
        ax.set_xlabel('x')
        ax.set_xlabel('y')
        ax.set_xlabel('z')

        plt.savefig(f'results/graphs/uniform_sampling.png')
        # plt.show()

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

        fig, ax = plt.subplots(2, 2)
        fig.set_size_inches(10, 8)
        fig.set_dpi(100)

        # THETAS
        theta_theory = np.linspace(0, np.pi, len(random_samples))
        ax[0, 0].hist(thetas, bins=30, density=True, alpha=0.6, color='red')
        ax[0, 0].plot(theta_theory, 0.5 * np.sin(theta_theory), color='black')
        ax[0, 0].set_title('Observed Theta vs. Theoretical Theta')

        # PHIS
        phi_theory = np.linspace(0, 2 * np.pi, len(random_samples))
        ax[0, 1].hist(phis, bins=30, density=True, color='green')
        ax[0, 1].plot(phi_theory, [1 / (2 * np.pi)] * len(random_samples), color='black')
        ax[0, 1].set_title('Observed Phi vs. Theoretical Phi')

        # r
        # r_theory = np.linspace(0, len(random_samples))
        ax[1, 0].plot(rs, color='blue')
        # ax[1, 0].plot(r_theory, len(random_samples), color='black')
        ax[1, 0].set_title('Observed r vs. Theoretical r (INCORRECT)')

        plt.savefig(f'results/graphs/verify_any_bias.png')
        # plt.show()

    @staticmethod
    def fa(plotting_format):
        keys = plotting_format.keys()

        _ = plt.figure()
        plt.title('Fractional Anisotropy')
        plt.xlabel('Particle Count')
        plt.ylabel('Fractional Anisotropy')
        for key in keys:
            for data in plotting_format[key]:
                index, particles, diffusion_tensor, eigen_diffusion_tensor, fa = data
                plt.scatter(len(particles), fa, c='blue')

        plt.savefig(f'results/graphs/fa.png')
        # plt.show()

    @staticmethod
    def eigens(plotting_format):
        keys = plotting_format.keys()

        fig = plt.figure()
        plt.title('Eigens')
        plt.xlabel('a')
        plt.ylabel('b')
        for key in keys:
            for data in plotting_format[key]:
                _, _, _, eigen_diffusion_tensor, _ = data
                plt.scatter([key] * len(eigen_diffusion_tensor), eigen_diffusion_tensor, c='blue')

        plt.savefig(f'results/graphs/eigens.png')
        # plt.show()
    
    @staticmethod
    def diffusion(plotting_format):
        keys = plotting_format.keys()

        for key in keys:
            for data in plotting_format[key]:
                index, particles, _, _, _ = data

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.set_aspect('equal', 'box')
                ax.set_title(f'Bulk Water Diffusion (run={index}, NP={key})')
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')

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