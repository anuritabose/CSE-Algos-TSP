"""
 * TSP_BruteForce.py
 *
 * This file implements a brute force algorithm to solve the Traveling Salesman Problem (TSP).
 * It reads city coordinates from a file, attempts to find the shortest tour visiting all cities
 * exactly once, and returns to the starting city. The algorithm uses a time cutoff to limit
 * execution time for large instances.
 *
 * Key features:
 * - Brute force approach: Generates all possible permutations of cities
 * - Time cutoff: Stops execution if the specified time limit is reached
 * - Solution output: Writes the best found tour and its length to a file
 * - Terminal output: Displays cutoff time, solution quality, and completion status
 *
 * Usage: python TSP_BruteForce.py -inst <filename> -alg BF -time <cutoff_in_seconds>
"""

import sys
import math
import time
import os
from typing import List, Tuple

MAX_CITIES = 1000

class City:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y

class TSPSolver:
    def __init__(self, filename: str, cutoff_time: int):
        self.filename = filename
        self.cutoff_time = cutoff_time
        self.cities: List[City] = []
        self.num_cities = 0
        self.best_tour: List[int] = []
        self.best_tour_length = float('inf')
        self.start_time = 0
        self.time_exceeded = False

    def distance(self, city1: City, city2: City) -> int:
        return round(math.sqrt((city2.x - city1.x)**2 + (city2.y - city1.y)**2))

    def calculate_tour_length(self, tour: List[int]) -> float:
        return sum(self.distance(self.cities[tour[i]], self.cities[tour[(i + 1) % self.num_cities]]) 
                   for i in range(self.num_cities))

    def check_time(self) -> bool:
        if time.time() - self.start_time >= self.cutoff_time:
            self.time_exceeded = True
            return False
        return True

    def update_best_tour(self, current_tour: List[int]) -> None:
        current_length = self.calculate_tour_length(current_tour)
        if current_length < self.best_tour_length:
            self.best_tour_length = current_length
            self.best_tour = current_tour.copy()

    def brute_force(self, tour: List[int], start: int) -> None:
        if not self.check_time():
            return
        
        if start == self.num_cities - 1:
            self.update_best_tour(tour)
        else:
            for i in range(start, self.num_cities):
                tour[start], tour[i] = tour[i], tour[start]
                self.brute_force(tour, start + 1)
                tour[start], tour[i] = tour[i], tour[start]
                if self.time_exceeded:
                    return

    def read_tsp_file(self) -> None:
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                node_coord_section = False
                for line in lines:
                    if "NODE_COORD_SECTION" in line:
                        node_coord_section = True
                        continue
                    if node_coord_section and line.strip() != "EOF":
                        parts = line.split()
                        if len(parts) == 3:
                            id, x, y = map(float, parts)
                            self.cities.append(City(int(id), x, y))
                            self.num_cities += 1
                            if self.num_cities >= MAX_CITIES:
                                print("Warning: Maximum number of cities reached")
                                break
            print(f"Read {self.num_cities} cities from file")
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    def write_solution(self, method: str) -> None:
        base_name = os.path.basename(self.filename)
        instance_name = os.path.splitext(base_name)[0]
        filename = f"{instance_name}_{method}_{self.cutoff_time}.sol"
        
        try:
            with open(filename, 'w') as file:
                file.write(f"{self.best_tour_length:.2f}\n")
                file.write(','.join(str(self.cities[i].id) for i in self.best_tour))
                file.write('\n')
            print(f"Solution written to {filename}")
        except IOError as e:
            print(f"Error writing solution file: {e}")

    def solve(self) -> None:
        self.read_tsp_file()
        current_tour = list(range(self.num_cities))
        self.start_time = time.time()
        self.brute_force(current_tour, 0)

        print(f"Cutoff time: {self.cutoff_time} seconds")
        print(f"Solution quality: {self.best_tour_length:.2f}")
        print(f"Full tour computed: {'No' if self.time_exceeded else 'Yes'}")

        self.write_solution("BF")

def main() -> None:
    if len(sys.argv) != 7:
        print(f"Usage: {sys.argv[0]} -inst <filename> -alg BF -time <cutoff_in_seconds>")
        sys.exit(1)

    filename = sys.argv[2]
    algorithm = sys.argv[4]
    cutoff_time = int(sys.argv[6])

    if algorithm != "BF":
        print("Error: Only Brute Force (BF) algorithm is supported.")
        sys.exit(1)

    solver = TSPSolver(filename, cutoff_time)
    solver.solve()

if __name__ == "__main__":
    main()