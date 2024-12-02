import os
import matplotlib.pyplot as plt
import subprocess

# Define constants
CITIES = [
    "Atlanta", "Berlin", "Boston", "Champaign", "Cincinnati", "Denver",
    "NYC", "Philadelphia", "Roanoke", "SanFrancisco", "Toronto",
    "UKansasState", "UMissouri"
]

# Cutoff times for each algorithm
BRUTE_FORCE_CUTOFFS = [0, 2, 5, 10, 20, 40, 50, 100, 150, 200, 500]
LOCAL_SEARCH_CUTOFFS = [
    0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
    0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1
]

ALGORITHMS = ["brute_force", "local_search"]
DATA_DIR = "../data"  # Directory containing .tsp files
PLOT_DIR = "../plots"  # Directory to save plots
OUTPUT_DIR = "./"  # Directory where the solution files are saved

def create_output_dirs():
    """Create output directories for storing plots."""
    for alg in ALGORITHMS:
        os.makedirs(os.path.join(PLOT_DIR, alg), exist_ok=True)

def run_algorithm(city, algorithm, cutoff):
    """
    Run the specified algorithm for the given city and cutoff time.
    Read the solution quality from the generated output file in /code/.
    """
    tsp_file = os.path.join(DATA_DIR, f"{city}.tsp")
    algo_suffix = "BF" if algorithm == "brute_force" else "LS"
    output_filename = f"{city.lower()}_{algo_suffix}_{cutoff}.sol"
    output_file = os.path.join(OUTPUT_DIR, output_filename)

    # Construct the command for the algorithm
    if algorithm == "brute_force":
        command = [
            "python", "../code/brute_force.py", "-inst", tsp_file, "-alg", "BF", "-time", str(cutoff)
        ]
    elif algorithm == "local_search":
        command = [
            "python", "../code/local_search.py", "-inst", tsp_file, "-cutoff", str(cutoff),
            "-seed", "42", "-output", output_file
        ]

    try:
        # Run the command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read the solution quality from the output file
        with open(output_file, "r") as f:
            lines = f.readlines()
            if algorithm == "brute_force":
                # First line contains the solution quality for brute force
                solution_quality = lines[0].strip()
                return float(solution_quality) if solution_quality != "inf" else float('inf')
            elif algorithm == "local_search":
                # Look for "Best Distance:" in the local search file
                for line in lines:
                    if line.startswith("Best Distance:"):
                        solution_quality = line.split(":")[1].strip()
                        return float(solution_quality) if solution_quality != "inf" else float('inf')
    except subprocess.CalledProcessError as e:
        print(f"Error running {algorithm} for {city} with cutoff {cutoff}: {e}")
        return float('inf')  # Return a high value to indicate failure
    except FileNotFoundError:
        print(f"Output file {output_file} not found.")
        return float('inf')
    except Exception as e:
        print(f"Error reading {output_file}: {e}")
        return float('inf')

def plot_results(city, algorithm, cutoff_times, solution_qualities):
    """
    Plot solution qualities against cutoff times for a given city and algorithm.
    Display 'inf' values as upward arrows.
    """
    plt.figure()

    # Handle 'inf' values for plotting
    finite_times = [cutoff for cutoff, quality in zip(cutoff_times, solution_qualities) if quality != float('inf')]
    finite_qualities = [quality for quality in solution_qualities if quality != float('inf')]
    
    inf_times = [cutoff for cutoff, quality in zip(cutoff_times, solution_qualities) if quality == float('inf')]
    
    # Plot finite values
    plt.plot(finite_times, finite_qualities, marker="o", linestyle="-", label="Solution Quality")
    
    # Add markers for 'inf' values
    if inf_times:
        # Place 'inf' markers above max finite quality
        inf_marker_y = max(finite_qualities) * 1.2 if finite_qualities else 1.0
        plt.scatter(inf_times, [inf_marker_y] * len(inf_times), color='red', label="inf (vertical)", marker='^')
        for inf_time in inf_times:
            plt.annotate("inf", (inf_time, inf_marker_y), textcoords="offset points", xytext=(-10, 10), ha='center')

    # Title and labels
    plt.title(f"{city} - {algorithm.replace('_', ' ').title()}")
    plt.xlabel("Cutoff Time (s)")
    plt.ylabel("Solution Quality")
    plt.yscale('linear')
    plt.legend()
    plt.grid(True)
    
    # Adjust filename based on algorithm
    algorithm_suffix = "BF" if algorithm == "brute_force" else "LS"
    output_filename = f"{city.lower()}_{algorithm_suffix}.png"
    output_path = os.path.join(PLOT_DIR, algorithm, output_filename)
    
    plt.savefig(output_path)
    plt.close()

def main():
    create_output_dirs()
    
    for city in CITIES:
        for algorithm in ALGORITHMS:
            # Select cutoff times based on the algorithm
            cutoff_times = BRUTE_FORCE_CUTOFFS if algorithm == "brute_force" else LOCAL_SEARCH_CUTOFFS
            solution_qualities = []
            for cutoff in cutoff_times:
                print(f"Running {algorithm} for {city} with cutoff {cutoff}")
                solution_quality = run_algorithm(city, algorithm, cutoff)
                solution_qualities.append(solution_quality)
            
            # Plot the results
            plot_results(city, algorithm, cutoff_times, solution_qualities)
            print(f"Plot saved for {city} using {algorithm}.")

if __name__ == "__main__":
    main()
