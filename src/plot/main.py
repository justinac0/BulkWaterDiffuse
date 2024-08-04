if __name__ == "__main__":
    simulation_object = read_yaml_to_object('results/data/simulation.yaml')

    plt.style.use('seaborn-v0_8-muted')

    rand_np = simulation_object['particle_counts']

    specific_run = get_simulation_info(simulation_object, 0, max(rand_np))

    Plotter.uniform_sampling(specific_run)
    Plotter.verify_any_bias(specific_run)
    Plotter.fa(simulation_object)
    Plotter.eigens(simulation_object)
    Plotter.diffusion(specific_run)