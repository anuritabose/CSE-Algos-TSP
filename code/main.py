import argparse
import os
import time
from approximate import approximation_tsp
from brute_force import TSPSolver
from local_search import tsp_local_search
import sys



def parse_tsp_file(file_path):
    """
    Parses a .tsp file and extracts the node coordinates.
    Args:
        file_path (str): Path to the .tsp file.
    Returns:
        list: List of tuples representing coordinates of the locations [(x1, y1), (x2, y2), ...].
    """
    coordinates = []
    if getattr(sys, 'frozen', False):  # Running as an executable
        project_root = os.path.dirname(os.path.dirname(sys.executable))
    else:  # Running as a script
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(project_root,file_path)
    print()
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Locate the "NODE_COORD_SECTION" and read coordinates
    coordinates_start = lines.index("NODE_COORD_SECTION\n") + 1
    for line in lines[coordinates_start:]:
        if line.strip() == "EOF":
            break
        _, x, y = line.strip().split()
        coordinates.append((float(x), float(y)))

    return coordinates


def write_output(output_dir, file_name, best_distance, best_route, total_time, full_tour):
    """
    Writes the output of the algorithm to a .sol file.
    Args:
        output_dir (str): Directory where the output file will be stored.
        file_name (str): Name of the output file.
        best_distance (float): The shortest distance found.
        best_route (list): The best route found.
        total_time (float): The time taken by the algorithm.
        full_tour (bool): Whether a full tour was computed.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, file_name)

    with open(output_file, 'w') as f:
        f.write(f"Best Distance: {best_distance:.2f}\n")
        f.write(f"Route: {','.join(map(str, best_route))}\n")
        f.write(f"Time Taken: {total_time:.6f} seconds\n")
        f.write(f"Full Tour: {'Yes' if full_tour else 'No'}\n")

    print(f"Output written to {output_file}")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="TSP Solver")
    parser.add_argument("-inst", required=True, help="Path to the TSP file")
    parser.add_argument("-alg", required=True, choices=["BF", "Approx", "LS"], help="Algorithm to use: BF, Approx, or LS")
    parser.add_argument("-time", required=True, type=int, help="Cutoff time in seconds")
    parser.add_argument("-seed", type=int, help="Random seed (only for LS and Approx)")
    args = parser.parse_args()

    # Parse the arguments
    tsp_file = args.inst
    cutoff_time = args.time
    random_seed = args.seed
    algorithm = args.alg

    # Prepare the output directory
    if getattr(sys, 'frozen', False):  # Running as an executable
        project_root = os.path.dirname(os.path.dirname(sys.executable))
    else:  # Running as a script
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    output_dir = f"output_exec/{algorithm}"
    instance_name = os.path.splitext(os.path.basename(tsp_file))[0].lower()
    output_dir = os.path.join(project_root, output_dir)
    if algorithm == "BF":
        # Brute Force Algorithm
        if getattr(sys, 'frozen', False):  # Running as an executable
            project_root = os.path.dirname(os.path.dirname(sys.executable))
        else:  # Running as a script
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tsp_file = os.path.join(project_root,tsp_file)
        solver = TSPSolver(tsp_file, cutoff_time)
        solver.solve()

        # Extract results from the solver
        best_distance = solver.best_tour_length
        best_route = [solver.cities[i].id for i in solver.best_tour]
        total_time = time.time() - solver.start_time  # Calculate the actual time taken
        full_tour = not solver.time_exceeded  # Check if the full tour was computed

        # Prepare the output file name
        output_file_name = f"{instance_name}_BF_{cutoff_time}.sol"

        # Write results to the output file
        write_output(output_dir, output_file_name, best_distance, best_route, total_time, full_tour)

    elif algorithm == "Approx":
        # Approximation Algorithm
        # Parse the TSP file
        coordinates = parse_tsp_file(tsp_file)

        # Start measuring time
        start_time = time.time()

        # Run the approximation algorithm
        best_distance, best_route = approximation_tsp(coordinates)

        # End time
        total_time = time.time() - start_time

        # Check if a full tour is computed
        full_tour = len(best_route) == len(coordinates)

        # Prepare the output file name
        output_file_name = f"{instance_name}_Approx_{cutoff_time}.sol"

        # Write results to the output file
        write_output(output_dir, output_file_name, best_distance, [node + 1 for node in best_route], total_time, full_tour)

    elif algorithm == "LS":
        # Local Search Algorithm
        if random_seed is None:
            print("Error: -seed is required for LS algorithm.")
            return

        # Run the local search algorithm
        best_distance, best_route, total_time, full_tour = tsp_local_search(tsp_file, cutoff_time, random_seed)

        # Prepare the output file name
        output_file_name = f"{instance_name}_LS_{cutoff_time}_{random_seed}.sol"

        # Write results to the output file
        write_output(output_dir, output_file_name, best_distance, [node + 1 for node in best_route], total_time, full_tour)

    else:
        print("Error: Unsupported algorithm selected.")
        return


if __name__ == "__main__":
    main()
