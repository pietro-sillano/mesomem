import subprocess
import os
import argparse
import itertools
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def create_dir(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def check_dependencies(args):
    """Checks if the LAMMPS file and binary actually exist."""
    # 1. Check Input File
    lmp_file = os.path.join(args.path, f"{args.name}.lmp")
    if not os.path.exists(lmp_file):
        print(f"[CRITICAL ERROR] LAMMPS input file not found: {lmp_file}")
        return False

    # 2. Check Binary (if it's a command like 'lmp_gpu', shutil.which checks PATH)
    if not shutil.which(args.lmp_bin) and not os.path.exists(args.lmp_bin):
        print(f"[CRITICAL ERROR] LAMMPS binary '{args.lmp_bin}' not found in PATH or current directory.")
        return False
        
    return True

def validate_lammps_script(lmp_bin, lmp_file, params,sim_folder):
    # We allow stdout to be hidden, but we capture stderr to show you errors if it fails
    command = f"{lmp_bin} -in {lmp_file} -v eps {params['eps']} -v sigma {params['sigma']} -v ktilt {params['ktilt']} -v ksplay {params['ksplay']} -v rcut {params['rcut']} -v wc {params['wc']} -v T {params['T']} -v zeta {params['zeta']} -v N {params['N']} -v d {params['d']:.2f} -skiprun"
    # print(command)
    # mpirun -np 4 lmp_radial -i in.growing_tension.lmp -v eps 1.0 -v sigma 1.0 -v ktilt 30.0 -v ksplay 30.0 -v rcut 2.8 -v wc 1.6 -v zeta 4.0 -v d 0.80 -v N 400

    
    try:
        # Capture stderr so we can print it only if it fails
        subprocess.run(command, check=True, shell=True,cwd=sim_folder, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True, ""
    except subprocess.CalledProcessError as e:
        # Return the error message from LAMMPS
        error_msg = e.stderr.decode('utf-8') if e.stderr else "Unknown error"
        return False, error_msg

def single_sim(args, params):
    sim_id = f"N_{params['N']}_d_{params['d']}_eps_{params['eps']}_sigma_{params['sigma']}_kt_{params['ktilt']}_ks_{params['ksplay']}_rcut_{params['rcut']}_wc_{params['wc']}_T_{params['T']}_zeta_{params['zeta']}"
    
    # 1. Logic Check
    if params['wc'] > params['rcut']:
        return f"[SKIP] {sim_id}: wc > rcut"

    sim_folder = os.path.join(args.path, sim_id)
    create_dir(sim_folder)
    
    lmp_file = os.path.join(args.path, f"{args.name}.lmp")
    
    # 2. Validation Step
    valid, err_msg = validate_lammps_script(args.lmp_bin, lmp_file, params,sim_folder)
    if not valid:
        # We write the error to a file so you can debug it
        with open(os.path.join(sim_folder, "error_dryrun.log"), "w") as f:
            f.write(err_msg)
        return f"[FAIL] {sim_id}: Validation failed (see error_dryrun.log)"

    # 3. Execution Step
    bash_command = (f"mpirun -np {args.nprocs} --bind-to none {args.lmp_bin} -in {lmp_file} -v eps {params['eps']} -v sigma {params['sigma']} -v ktilt {params['ktilt']} -v ksplay {params['ksplay']} -v rcut {params['rcut']} -v wc {params['wc']} -v T {params['T']} -v zeta {params['zeta']} -v N {params['N']} -v d {params['d']:.2f}")
    
    # print(bash_command)
    
    if not args.dryrun:
        try:
            with open(os.path.join(sim_folder, "sim.log"), "w") as logfile:
                subprocess.run(bash_command, check=True, shell=True, cwd=sim_folder, stdout=logfile, stderr=subprocess.STDOUT)
            return f"[DONE] {sim_id}"
        except subprocess.CalledProcessError:
            return f"[ERROR] {sim_id}: Simulation crashed (check sim.log)"
    else:
        return f"[DRY RUN] {sim_id}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default=os.getcwd())
    parser.add_argument("--name", type=str, default='self_assembly')
    parser.add_argument("--dryrun", action='store_true')
    parser.add_argument("--lmp_bin", type=str, default="lmp_2025")
    parser.add_argument("--nprocs", type=int, default=2)
    parser.add_argument("--total_cpus", type=int, default=os.cpu_count()) 

    args = parser.parse_args()

    # --- Pre-flight Check ---
    if not check_dependencies(args):
        return # Stop immediately if files/binaries are missing
    
    params = {
        "ktilt": [15.0],
        "ksplay": [1.0],
        "rcut": [2.5],
        "wc": [2.0],
        "T": [0.1,0.15,0.2,0.25,0.3,0.35,0.4],
        "eps": [1.0],
        "sigma":[1.0],
        "zeta": [2,3,4,5,6,7,8,9],
        "N": [2500],
        "d": [0.80]
    }
    
    # mpirun -np 4 lmp_radial -i in.growing_tension.lmp -v eps 1.0 -v sigma 1.0 -v ktilt 30.0 -v ksplay 30.0 -v rcut 2.5 -v wc 1.6 -v zeta 8.0 -v d 0.85 -v N 400
    
    # Calculate Workers
    max_workers = args.total_cpus // args.nprocs
    if max_workers < 1: max_workers = 1
    
    print(f"--- Configuration ---")
    print(f"Base Path: {args.path}")
    print(f"LAMMPS Binary: {args.lmp_bin}")
    print(f"Concurrent jobs: {max_workers}")
    print(f"---------------------")

    # Prepare Jobs
    job_list = []
    keys, values = zip(*params.items())
    for combination in itertools.product(*values):
        combo_dict = dict(zip(keys, combination))
        if combo_dict['zeta'] == 3 or combo_dict['zeta'] == 4:
            combo_dict['d'] = 0.80
        elif combo_dict['zeta'] == 5 or combo_dict['zeta'] == 6:
            combo_dict['d'] = 0.85
        elif combo_dict['zeta'] == 7 or combo_dict['zeta'] == 8:
            combo_dict['d'] = 0.90
        
        # CORRECTED LOGIC HERE:
        if combo_dict['rcut'] >= combo_dict['wc']:
            job_list.append(combo_dict)

    if not job_list:
        print("[WARNING] No jobs generated! Check your parameter combinations (rcut vs wc).")
        return

    print(f"Queuing {len(job_list)} simulations...")

    # Run Pool
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(single_sim, args, p): p for p in job_list}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Simulations"):
            result = future.result()
            if "[ERROR]" in result or "[FAIL]" in result:
                tqdm.write(result)

if __name__ == "__main__":

# python3 launch_planar_parallel.py --path /home/pietro/martini/new_potential_v2/planar/phase_plot_1 --name in.planar_v2 --lmp_bin lmp_radial --nprocs 2 --total_cpus 24    
    
# nohup python3 launch_planar_parallel.py --path /home/pietro/martini/new_potential_v2/planar/phase_plot_1 --name in.planar_v2 --lmp_bin lmp_radial --nprocs 2 --total_cpus 24 > log.out 2>&1 &!
    
    main()
