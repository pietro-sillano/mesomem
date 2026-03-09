import os
import re
import csv
import socket
import argparse
from utilities import *

# hostname = socket.gethostname()
# if hostname == "mi-notebook":
#     base_dir = "/home/pietro/Desktop/new_potential_timon/spherical"
# elif hostname.startswith("md"):
#     base_dir = "/martini/pietro/new_potential/spherical/"
#     base_dir = "/martini/pietro/new_potential/planar/"



parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, default='sistematic_k/', help='Relative path to data directory')
parser.add_argument('--base_dir', type=str, default="/martini/pietro/new_potential/planar/", help='Parent directory')


args = parser.parse_args()
data_dir = args.data_dir
base_dir = args.base_dir

# Pattern: captures key-value pairs like _kt_0.5 or _N_100
param_pattern = re.compile(r'(?:^|_)([a-zA-Z]+)_([\d.]+)')
output_file = "simulation_summary.csv"
nframes_expected = 102

# Output list
data = []

# Walk through the directory
for root, dirs, files in os.walk(os.path.join(base_dir, data_dir)):
    print(dirs)
    for dir_name in dirs:
        full_path = os.path.join(root, dir_name)
        param_matches = param_pattern.findall(dir_name)
        if param_matches:
            params = {key: float(value) if '.' in value else int(value)
                      for key, value in param_matches}
            log_path = os.path.join(full_path, "log.lammps")
            traj_path = os.path.join(full_path, "position.lammpstrj")
            

            if not (os.path.isfile(log_path) and os.path.isfile(traj_path)):
                params["valid"] = 0
                print(f"trajectory file is missing: {traj_path}")
            else:
                nframes,_ = count_samples_dump_file(traj_path)
                N_ATOMS = count_atoms_dump_file(traj_path)
                t, coords, v, mu, omega  = process_single_dump_file_images(traj_path,SKIP_SAMPLES = 0, STRIDE = 1)
                
                if coords.shape[0] != nframes:
                    print(f"trajectory file is not containing the right number of frames: {traj_path}")
                    
                if coords.shape[0] != nframes_expected:
                    print(f"trajectory file is not containing the expected number of frames: {traj_path}")
                    with open(os.path.join(base_dir, data_dir, "bad_traj_files.txt"), "a") as badfile:
                        badfile.write(f"{traj_path}, {coords.shape[0]}\n")


                with open(log_path, 'r') as log_file:
                    if any("ERROR: Lost atoms" in line for line in log_file):
                        print(f"Lost atoms")
                        with open(os.path.join(base_dir, data_dir, "bad_traj_files.txt"), "a") as badfile:
                            badfile.write(f"{traj_path}, lost atoms too\n")
                        params["valid"] = -1
                    else:
                        params["valid"] = 1

            # Save relative path of the trajectory (optional)
            params["path"] = dir_name
            data.append(params)

# Output fieldnames: collect all unique keys
fieldnames = sorted(set(k for d in data for k in d.keys()))

# Write CSV
output_path = os.path.join(base_dir, data_dir, output_file)
with open(output_path, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Exported {len(data)} entries to {output_path}")
