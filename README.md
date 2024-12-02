# CSE-Algos-TSP

Project Report- https://docs.google.com/document/d/1rjifyfigU993Dy9tk2OejNPqGFrITz-UV-PP_BDPdvM/edit?tab=t.0

Project Results- https://docs.google.com/spreadsheets/d/15jmbK0Oe3G6Sk5bFyIjX0at-Oj1hBsZ5ZYQ7JpJvHUM/edit?gid=0#gid=0

# Traveling Salesman Problem (TSP) Solver

This repository provides implementations for three distinct algorithms aimed at tackling the Traveling Salesman Problem:

* Brute Force (BF)
* Approximation Algorithm (Approx)
* Local Search with Simulated Annealing (LS)

These algorithms are written in Python and can be executed through an executable file generated using PyInstaller.

## Algorithms

### Brute Force (BF)

The Brute Force algorithm is a straightforward approach that explores all possible permutations of cities to determine the shortest tour. This method guarantees finding the optimal solution. However, due to its factorial time complexity, O(n!), it becomes computationally impractical for instances with a large number of cities.

**Key Features:**

* **Guaranteed optimality:** If allowed to run until completion, the Brute Force algorithm will always find the shortest possible tour.
* **Time cutoff:** The Python implementation incorporates a time cutoff feature to manage execution time for larger problem instances. This feature allows for quicker, albeit potentially suboptimal, solutions when dealing with a large number of cities.

### Approximation Algorithm (Approx)

The Approximation Algorithm offers an efficient method for finding a tour that is guaranteed to be within a factor of 2 of the optimal tour length. This approach leverages the Minimum Spanning Tree (MST) and follows a specific procedure:

1. **Input Parsing:** Extract node coordinates from the input .tsp file.
2. **MST Construction:** Construct the MST using Prim's Algorithm, prioritizing edges with the smallest weights to connect nodes greedily.
3. **Preorder Traversal:** Perform a depth-first preorder traversal of the constructed MST to establish a tour sequence.
4. **Cost Computation:** Calculate the total cost of the generated tour by summing the Euclidean distances between consecutive nodes in the tour, including the return to the starting node.
5. **Output Generation:** Produce an output containing the total tour cost and the sequence of nodes, adjusted for 1-based indexing.

### Local Search: Simulated Annealing (LS)

Local Search, specifically employing the Simulated Annealing heuristic, provides an alternative approach to finding approximate solutions for the TSP. The algorithm starts with a random tour and progressively refines it by exploring neighboring solutions.

**Simulated Annealing:**

* Plays a crucial role in preventing the algorithm from getting stuck in local optima, enabling the discovery of potentially better solutions by occasionally accepting worse solutions during the search process.
* This acceptance of worse solutions is governed by a temperature parameter that gradually decreases, reducing the probability of accepting inferior solutions as the algorithm progresses.

**Key Steps:**

1. **Initialization:** Start with a randomly generated solution and calculate its cost.
2. **Neighbor Generation:** Create a neighboring solution by swapping the positions of two cities within the current tour.
3. **Acceptance Criterion:** Determine whether to accept the newly generated neighbor based on an acceptance probability function. This function considers the difference in quality (cost) between the current solution and the neighbor, as well as the current temperature parameter.
4. **Cooling:** Systematically reduce the temperature parameter. This gradual reduction makes the algorithm less likely to accept worse solutions as it progresses.
5. **Termination:** The algorithm stops when the temperature drops below a predefined minimum threshold or when a specified time limit is reached.

## Python Code Structure

The Python codebase is structured into several files:

* `local_search.py`: Contains the core implementation of the Local Search with Simulated Annealing algorithm. It includes functions for tasks such as:
    * Parsing the input `.tsp` file to extract city coordinates
    * Computing the Euclidean distance between two cities
    * Calculating the total length of a given tour
    * Generating neighboring solutions by swapping cities in the tour
    * Determining the acceptance probability for new solutions
* `ls_driver.py`: Acts as a driver script for executing the Local Search algorithm multiple times across various problem instances and collecting the results. This script enables:
    * Running the Local Search algorithm repeatedly on a specific `.tsp` file to gather statistics like average runtime, solution quality, and relative error
    * Iterating through multiple `.tsp` files in a directory, conducting experiments, and storing the results in a CSV file for analysis
* `Main.py`: Serves as the entry point for executing the TSP solver. This script:
    * Parses command-line arguments to select the algorithm (`BF`, `Approx`, or `LS`), input file, and runtime cutoff
    * Calls the appropriate algorithm's implementation based on the selected method
    * Handles input parsing, result computation, and output file generation
    * Supports optional seed input for reproducibility when using the Local Search algorithm
    * Implements helper functions such as:
        * `parse_tsp_file(file_path)`: Parses `.tsp` files and extracts coordinates
        * `write_output(output_dir, file_name, best_distance, best_route, total_time, full_tour)`: Writes results to a `.sol` file
        * Handles Brute Force, Approximation, and Local Search algorithms using dedicated functions
* `brute_force.py`: Implements a brute force algorithm for solving the TSP:
    * **Key Features**:
        * Explores all permutations of cities to find the shortest tour
        * Includes a time cutoff to stop execution if the specified limit is reached
        * Outputs the best tour length and sequence to a solution file
        * Displays execution details such as cutoff time, solution quality, and whether the full tour was computed
    * **Usage**:
        ```
        python brute_force.py -inst <filename> -alg BF -time <cutoff_in_seconds>
        ```
* `approximate.py`: Implements an MST-based approximation algorithm for solving the TSP:
    * **Key Features**:
        * Constructs a Minimum Spanning Tree (MST) using Prim's algorithm
        * Performs a preorder traversal of the MST to generate a tour
        * Calculates the total cost of the generated tour
        * Outputs the tour and its cost to a solution file
    * **Usage**:
        ```
        python approximate.py -i <filename> -m Approx -s <seed>
        ```
## Executing the TSP Solver

**Executable File:**

* An executable file (`exec.exe`) can be generated using PyInstaller for running the TSP solver.
* This file is located in the `CODE/dist` directory.

**Command Line Arguments:**

* The executable accepts the following command-line arguments:
    * **`-inst <filename>`:** Specifies the .tsp input file containing city coordinates
    * **`-alg [BFS|Approx|LS]`:** Selects the algorithm (BFS, Approx, or LS) to be used
    * **`-time <cutoff>`:** Sets the maximum runtime (in seconds) for the program
    * **`-seed <seed>`:** An optional argument for specifying a random seed, particularly useful for the Local Search (LS) algorithm to enable result reproducibility

**Example Commands:**

* To solve the TSP for the "Atlanta.tsp" instance using the Brute Force algorithm with a runtime limit of 30 seconds:

```bash
exec.exe -inst Atlanta.tsp -alg BF -time 30
```
* To solve the same instance using the Local Search algorithm with a 30-second time limit and a random seed of 42:

```bash
exec.exe -inst Atlanta.tsp -alg LS -time 30 -seed 42
```
**Output:**

The output files generated by the executable are stored in the `output_exec` directory.
