import argparse
import math
import random
import time
import os
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
    print(file_path)
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


def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def calculate_total_distance(route, distances):
    """Calculates the total distance of a route."""
    total_distance = sum(distances[route[i]][route[i + 1]] for i in range(len(route) - 1))
    total_distance += distances[route[-1]][route[0]]  # Return to start
    return total_distance


def get_neighbor(route):
    """
    Generates a neighboring solution by swapping two cities.
    Args:
        route (list): Current route.
    Returns:
        list: A new route with two cities swapped.
    """
    new_route = route[:]
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


def acceptance_probability(old_cost, new_cost, temperature):
    """
    Calculates the probability of accepting a worse solution.
    Args:
        old_cost (float): Current solution cost.
        new_cost (float): New solution cost.
        temperature (float): Current temperature.
    Returns:
        float: Acceptance probability.
    """
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) / temperature)


def tsp_local_search(file_path, cutoff, seed):
    """
    Solves TSP using Simulated Annealing.
    Args:
        file_path (str): Path to the .tsp file.
        cutoff (int): Time cutoff (in seconds).
        seed (int): Random seed.
    Returns:
        tuple: (best_distance, best_route, total_time, full_tour)
    """
    random.seed(seed)

    # Parse the input file and compute distances
    coordinates = parse_tsp_file(file_path)
    num_cities = len(coordinates)
    cities = list(range(num_cities))

    # Precompute distances between all cities
    distances = [[euclidean_distance(coordinates[i], coordinates[j]) for j in range(num_cities)] for i in range(num_cities)]

    # Initialize variables
    current_route = cities[:]
    random.shuffle(current_route)
    current_distance = calculate_total_distance(current_route, distances)

    best_route = current_route[:]
    best_distance = current_distance

    start_time = time.time()
    temperature = 100000.0  # Initial temperature
    cooling_rate = 0.9999  # Cooling rate
    min_temperature = 1e-4  # Stopping temperature
    while time.time() - start_time < cutoff and temperature > min_temperature:
        # Generate a neighboring solution
        neighbor_route = get_neighbor(current_route)
        neighbor_distance = calculate_total_distance(neighbor_route, distances)

        # Decide whether to accept the new solution
        if acceptance_probability(current_distance, neighbor_distance, temperature) > random.random():
            current_route = neighbor_route
            current_distance = neighbor_distance

            # Update the best solution
            if current_distance < best_distance:
                best_route = current_route[:]
                best_distance = current_distance

        # Cool down the temperature
        temperature *= cooling_rate

    # Calculate total time taken
    total_time = time.time() - start_time

    # Check if a full tour is computed
    full_tour = len(best_route) == num_cities

    # Return the results
    return best_distance, best_route, total_time, full_tour


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-inst", required=True, help="Path to the .tsp file")
    parser.add_argument("-cutoff", type=int, required=True, help="Cutoff time in seconds")
    parser.add_argument("-seed", type=int, required=True, help="Random seed")
    parser.add_argument("-output", required=True, help="Output file")
    args = parser.parse_args()

    best_distance, best_route, total_time, full_tour = tsp_local_search(args.inst, args.cutoff, args.seed)

    # Write the output to the file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(f"Best Distance: {best_distance}\n")
        f.write(f"Route: {','.join(map(str, best_route))}\n")
        f.write(f"Time Taken: {total_time:.6f} seconds\n")
        f.write(f"Full Tour: {'Yes' if full_tour else 'No'}\n")
