import random
import os
from local_search import tsp_local_search
import time


def run_experiments(city_file, cutoff, num_runs=15, output_dir="output/local_search"):
    """
    Runs the TSP Local Search algorithm multiple times for a given city and calculates
    the average runtime, average solution quality, best solution quality, and relative error.

    Args:
        city_file (str): Path to the .tsp file for the city.
        cutoff (int): Time cutoff (in seconds) for each run.
        num_runs (int): Number of runs to average the results.
        output_dir (str): Directory to save intermediate outputs.

    Returns:
        tuple: Average runtime (seconds), average solution quality, best solution quality, relative error, and full tour status.
    """
    total_time = 0.0
    total_solution_quality = 0.0
    best_solution_quality = float('inf')  # Initialize to a very high value
    best_solution_file = None
    best_route = None
    city_name = os.path.basename(city_file).replace(".tsp", "").lower()
    os.makedirs(output_dir, exist_ok=True)
    full_tour_status = False  # Track whether the best solution is a full tour

    for run in range(num_runs):
        # Generate a random seed for each iteration
        seed = random.randint(1, 100000)

        # Run TSP Local Search
        best_distance, route, time_taken, full_tour = tsp_local_search(city_file, cutoff, seed)

        # Track overall results
        total_time += time_taken
        total_solution_quality += best_distance

        # Update the best solution if necessary
        if best_distance < best_solution_quality:
            best_solution_quality = best_distance
            best_route = route
            full_tour_status = full_tour  # Update full tour status for the best solution
            best_solution_file = os.path.join(output_dir, f"{city_name}_LS_{cutoff}_{seed}.sol")

    # Write the best solution to file
    if best_solution_file:
        with open(best_solution_file, 'w') as f:
            f.write(f"Best Distance: {best_solution_quality}\n")
            f.write(f"Route: {','.join(map(str, best_route))}\n")
            f.write(f"Full Tour: {'Yes' if full_tour_status else 'No'}\n")

    # Calculate averages
    avg_time = total_time / num_runs
    avg_solution_quality = total_solution_quality / num_runs

    # Calculate relative error
    rel_error = ((avg_solution_quality - best_solution_quality) / best_solution_quality) * 100

    print(f"Best solution file for {city_name}: {best_solution_file}")

    return avg_time, avg_solution_quality, best_solution_quality, rel_error, full_tour_status


def main():
    """
    Main driver function to run experiments for all city files.
    """
    # Directory containing .tsp files
    city_dir = "DATA"
    cutoff = 30  # Set a 30-second cutoff for each run
    num_runs = 15  # Number of runs per city

    # List all .tsp files in the directory
    city_files = [os.path.join(city_dir, file) for file in os.listdir(city_dir) if file.endswith(".tsp")]

    # Results storage
    results = []

    for city_file in city_files:
        city_name = os.path.basename(city_file).replace(".tsp", "").lower()
        print(f"Running experiments for {city_name}...")

        # Run experiments and store the results
        avg_time, avg_solution_quality, best_solution_quality, rel_error, full_tour_status = run_experiments(
            city_file, cutoff, num_runs
        )
        results.append((city_name, avg_time, avg_solution_quality, best_solution_quality, rel_error, full_tour_status))
        print(f"Completed {city_name}: Avg Time = {avg_time:.2f}s, "
              f"Avg Solution Quality = {avg_solution_quality:.2f}, "
              f"Best Solution Quality = {best_solution_quality:.2f}, "
              f"RelError = {rel_error:.2f}%, "
              f"Full Tour = {'Yes' if full_tour_status else 'No'}")

    # Save results to a CSV file
    results_file = "results.csv"
    with open(results_file, "w") as f:
        f.write("City,Average Time (s),Average Solution Quality,Best Solution Quality,RelError (%),Full Tour\n")
        for city_name, avg_time, avg_solution_quality, best_solution_quality, rel_error, full_tour_status in results:
            f.write(f"{city_name},{avg_time:.2f},{avg_solution_quality:.2f},{best_solution_quality:.2f},{rel_error:.2f},{'Yes' if full_tour_status else 'No'}\n")

    print(f"Results saved to {results_file}")


if __name__ == "__main__":
    main()

