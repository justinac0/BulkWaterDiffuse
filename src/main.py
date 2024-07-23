from matplotlib import plot as plt
from spacial_random import SpacialRandom

if __name__ == '__main__':
    dx, dy, dz = SpacialRandom.cube_point(-1, 1, -1, 1, -1, 1)
    
    Np = 100


    print(f'{dx}, {dy}, {dz}')

