import argparse
import os
import math
from heapq import heappop, heappush
from collections import defaultdict, deque
import time


def parse_tsp_file(file_path):
    """
    Parses a .tsp file and extracts the node coordinates.
    Args:
        file_path (str): Path to the .tsp file.
    Returns:
        list: List of tuples representing coordinates of the locations [(x1, y1), (x2, y2), ...].
    """
    coordinates = []
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


def construct_mst(coordinates):
    """
    Constructs a Minimum Spanning Tree (MST) using Prim's algorithm.
    Args:
        coordinates (list): List of tuples representing node coordinates.
    Returns:
        list: MST as a list of edges [(u, v), ...].
    """
    n = len(coordinates)
    mst = []
    visited = [False] * n
    min_heap = []
    visited[0] = True

    # Push all edges from the first node into the heap
    for i in range(1, n):
        heappush(min_heap, (euclidean_distance(coordinates[0], coordinates[i]), 0, i))

    while len(mst) < n - 1:
        weight, u, v = heappop(min_heap)
        if not visited[v]:
            visited[v] = True
            mst.append((u, v))
            for w in range(n):
                if not visited[w]:
                    heappush(min_heap, (euclidean_distance(coordinates[v], coordinates[w]), v, w))

    return mst


def preorder_traversal(mst, n):
    """
    Perform a preorder traversal of the MST.
    Args:
        mst (list): MST as a list of edges [(u, v), ...].
        n (int): Number of nodes.
    Returns:
        list: Preorder traversal tour of the MST.
    """

    # Build adjacency list
    adj = defaultdict(list)
    for u, v in mst:
        adj[u].append(v)
        adj[v].append(u)

    # Perform preorder traversal
    visited = [False] * n
    tour = []

    def dfs(node):
        visited[node] = True
        tour.append(node)
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    dfs(0)  # Start traversal from node 0
    return tour


def calculate_cost(tour, coordinates):
    """
    Calculate the total cost of the TSP tour.
    Args:
        tour (list): List of node indices representing the tour.
        coordinates (list): List of tuples representing node coordinates.
    Returns:
        float: Total cost of the tour.
    """
    cost = 0
    n = len(tour)
    for i in range(n - 1):
        cost += euclidean_distance(coordinates[tour[i]], coordinates[tour[i + 1]])
    cost += euclidean_distance(coordinates[tour[-1]], coordinates[tour[0]])  # Return to start
    return cost


def approximation_tsp(coordinates):
    """
    Solves TSP using the MST-based approximation algorithm.
    Args:
        coordinates (list): List of tuples representing node coordinates.
    Returns:
        tuple: (approx_cost, approx_tour)
    """
    # Constructing MST
    mst = construct_mst(coordinates)

    # Performing preorder traversal of the MST
    tour = preorder_traversal(mst, len(coordinates))

    # Calculating the cost of the tour
    cost = calculate_cost(tour, coordinates)

    return cost, tour


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Solve TSP using Approximation Algorithm.")
    parser.add_argument("-i", required=True, help="Input filename of the TSP dataset.")
    parser.add_argument("-m", required=True, choices=["Approx"], help="Method to use: Approx.")
    parser.add_argument("-s", required=True, type=int, help="Random seed (only for randomized algorithms).")
    args = parser.parse_args()

    file_name = args.i
    method = args.m

    # Parse the TSP file
    coordinates = parse_tsp_file(file_name)

    # Start measuring time before running the algorithm
    start_time = time.time()

    # Solve the TSP using the Approximation algorithm
    cost, tour = approximation_tsp(coordinates)

    # End time
    end_time = time.time() - start_time

    # Check if a full tour is computed
    full_tour = len(tour) == len(coordinates)

    # Print elapsed time and tour completion status
    print(f"Time taken: {end_time:.6f} seconds")
    print(f"Full tour computed: {full_tour}")

    # Generate the output filename
    instance_name = os.path.splitext(os.path.basename(file_name))[0].lower()
    seed = args.s
    output_file = f"output/approximate/{instance_name}_approx_{seed}.sol"

    # Write the results to the output file
    with open(output_file, "w") as f:
        f.write(f"{cost}\n")
        f.write(",".join(map(str, [node + 1 for node in tour])))


if __name__ == "__main__":
    main()
