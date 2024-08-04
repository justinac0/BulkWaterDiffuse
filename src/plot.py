import matplotlib.pyplot as plt
import simulation.io.yaml as yamlhelper
import plot.graphs as graph

if __name__ == "__main__":
    simulation_object = yamlhelper.read_yaml_to_object('results/data/simulation.yaml')

    plt.style.use('seaborn-v0_8-muted')

    rand_np = simulation_object['counts']

    specific_run = yamlhelper.get_simulation_by_info(simulation_object, 0, max(rand_np))

    graph.uniform_sampling(specific_run)
    graph.verify_any_bias(specific_run)
    graph.fa(simulation_object)
    graph.eigens(simulation_object)
    graph.diffusion(specific_run)