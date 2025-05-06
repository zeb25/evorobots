import os
import matplotlib.pyplot as plt

def read_fitness_files(output_dir):
    """
    Reads fitness values from files in the output directory.

    Args:
        output_dir (str): Path to the output directory.

    Returns:
        dict: A dictionary with fitness types as keys and lists of fitness values as values.
    """
    fitness_data = {"long_jump": [], "high_jump": []}

    for file_name in os.listdir(output_dir):
        if file_name.startswith("fitness") and file_name.endswith(".txt"):
            solution_id = file_name.replace("fitness", "").replace(".txt", "")
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "r") as f:
                fitness_value = float(f.read().strip())
            
            # Determine fitness type from solution ID or metadata (default to "long_jump")
            fitness_type = "long_jump" if "long_jump" in solution_id else "high_jump"
            fitness_data[fitness_type].append(fitness_value)

    return fitness_data

def plot_fitness(fitness_data, output_dir):
    """
    Plots fitness values for each fitness type.

    Args:
        fitness_data (dict): Fitness data grouped by fitness type.
        output_dir (str): Path to save the generated plots.
    """
    for fitness_type, values in fitness_data.items():
        plt.figure()
        plt.plot(values, marker='o', linestyle='-', label=fitness_type)
        plt.title(f"Fitness Over Solutions ({fitness_type})")
        plt.xlabel("Solution Index")
        plt.ylabel("Fitness Value")
        plt.legend()
        plt.grid(True)

        # Save the plot
        plot_path = os.path.join(output_dir, f"{fitness_type}_fitness_plot.png")
        plt.savefig(plot_path)
        print(f"Plot saved to {plot_path}")
        plt.close()

if __name__ == "__main__":
    output_dir = "/Users/zoebell/evorobots/output"
    fitness_data = read_fitness_files(output_dir)
    plot_fitness(fitness_data, output_dir)
