import matplotlib.pyplot as plt
import simulation.io.yaml_helper as yamlhelper
import simulation.io.yaml_keys as keys
import plot.graphs as graph

if __name__ == "__main__":
    simulation_object = yamlhelper.read_yaml_to_object('results/data/simulation.yaml')['production']

    plt.style.use('seaborn-v0_8-muted')

    rand_np = simulation_object[keys.PARTICLE_COUNT]

    specific_run = yamlhelper.get_simulation_by_info(simulation_object, 0, max(rand_np))

    graph.uniform_sampling(specific_run)
    graph.verify_any_bias(specific_run)
    graph.fa(simulation_object)
    graph.eigens(simulation_object)
    graph.diffusion(specific_run)
