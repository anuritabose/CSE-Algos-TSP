import os
import subprocess

# Path to the folder containing data files
data_folder = "DATA"

# Path to the executable
exec_path = "dist\exec.exe"

# List of algorithms
algorithms = ["BF", "Approx", "LS"]

# Cutoff time
cutoff_time = 30

#seed
seed = 42

# Check if the data folder exists
if not os.path.exists(data_folder):
    print(f"Error: The folder '{data_folder}' does not exist.")
    exit()

# Iterate through all files in the folder
for filename in os.listdir(data_folder):
    # Construct the full path to the file
    filepath = os.path.join(data_folder, filename)
    
    # Check if it is a file
    if os.path.isfile(filepath):
        for alg in algorithms:
            # Construct the command
            command = [exec_path, "-inst", filepath, "-alg", alg, "-time", str(cutoff_time), "-seed", str(seed)]
            
            print(f"Running: {' '.join(command)}")
            
            try:
                # Run the command
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while running command: {' '.join(command)}")
                print(f"Error details: {e}")
print("Completed run on all files successfully.")