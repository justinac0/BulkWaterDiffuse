# Bulk Water Diffuse (Research Project QUT PVB304)
WIP...
# Description
WIP...

# Results
## Initial Conditions
- D0 (Diffusion Coefficient): 2.3*10^(-3) mm^2/s
- NT (Simulation Step Count): 300
- dt (Time Step): 5*10^(-9) seconds
- Simulation Repeats: 3
- Point Counts: 100 -> 30000 (250 equidistant points along 1/sqrt(NP) space, where NP is the number of particles for a given simulation)

## Showcase
The following are a few examples of the graphs that were produced during the simulation.

Simulations were run in triplicate; the following graphs showcase 5 different ways of analysing the simulation data. 

Just a brief note on what the graphs display:
1. The final state of the random walk of bulk water diffusion.

### Verfication of random sampling
The following graphs are important in quantifying the nature of the randomness for the random walk. If the random number
generation for the random walk is bias all simulation data would be considered void.
> If you havent read the description above the verfication step may not be intuitive.

2. Diffusion particles projected to the surface of a unit sphere to determine any bias in the random sampling method.
3. Phi observed compared against theoretical phi. The observed data should follow the theoretical trend if the random sampling for the random walk is unbiased.
4. Theta observed compared against theoretical theta. The observed data should follow the theoretical trend if the random sampling for the random walk is unbiased.
5. R observed compared against theoretical r. The observed data should follow the theoretical trend if the random sampling for the random walk is unbiased.

- Eigen values graph: The eigen values of the diffusion tensor compared over all simulation data.
- Fractional anisotropy graph: This describes the percent error over the eigen values.

> Graph Title Format: 
{run_index}_{particle_count},
`run_index` refers to the simulation run the graph was
generated from. `particle_count` is the count of particles
simulated in this simulation instance.

### 0_147
1. ![](showcase/0_147_diffuse.png)
2. ![](showcase/0_147_uniform_sampling.png)
3. ![](showcase/0_147_phi.png)
4. ![](showcase/0_147_theta.png)
5. ![](showcase/0_147_r.png)

### 0_1590
1. ![](showcase/0_1590_diffuse.png)
2. ![](showcase/0_1590_uniform_sampling.png)
3. ![](showcase/0_1590_phi.png)
4. ![](showcase/0_1590_theta.png)
5. ![](showcase/0_1590_r.png)

### 0_5950
1. ![](showcase/0_5950_diffuse.png)
2. ![](showcase/0_5950_uniform_sampling.png)
3. ![](showcase/0_5950_phi.png)
4. ![](showcase/0_5950_theta.png)
5. ![](showcase/0_5950_r.png)

### 0_10128
1. ![](showcase/0_10128_diffuse.png)
2. ![](showcase/0_10128_uniform_sampling.png)
3. ![](showcase/0_10128_phi.png)
4. ![](showcase/0_10128_theta.png)
5. ![](showcase/0_10128_r.png)

### 0_29999
1. ![](showcase/0_29999_diffuse.png)
2. ![](showcase/0_29999_uniform_sampling.png)
3. ![](showcase/0_29999_phi.png)
4. ![](showcase/0_29999_theta.png)
5. ![](showcase/0_29999_r.png)

### Eigen Values (All Simulation Data)
![](showcase/eigens.png)

### Fractional Anisotropy (All Simulation Data)
![](showcase/fa_combined.png)

# References
- Momot, K.I. Diffusion tensor of water in model articular cartilage. Eur Biophys J 40, 81–91 (2011). https://doi.org/10.1007/s00249-010-0629-4
