import subprocess
import os
import argparse
import itertools
import shutil
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

# --- 1. THE JAILBREAK: Force Python to see all CPUs ---
def unrestrict_cpus(total_cpus):
    """
    Forces the current process to reset its CPU affinity to ALL available CPUs.
    This breaks the 'Core 0 Jail' often caused by nohup or cluster schedulers.
    """
    try:
        all_cpus = list(range(total_cpus))
        os.sched_setaffinity(0, all_cpus)
        # Verify it worked
        current_affinity = os.sched_getaffinity(0)
        if len(current_affinity) < total_cpus:
            print(f"[WARNING] Could not unrestrict CPUs. Visible CPUs: {current_affinity}")
        else:
            print(f"[SUCCESS] Python process unrestrained. Visible CPUs: {len(current_affinity)}")
    except AttributeError:
        # Happens on macOS or Windows where sched_setaffinity doesn't exist
        pass
    except Exception as e:
        print(f"[WARNING] Failed to reset affinity: {e}")

def create_dir(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def check_dependencies(args):
    lmp_file = os.path.join(args.path, f"{args.name}.lmp")
    if not os.path.exists(lmp_file):
        print(f"[CRITICAL ERROR] LAMMPS input file not found: {lmp_file}")
        return False
    if not shutil.which(args.lmp_bin) and not os.path.exists(args.lmp_bin):
        print(f"[CRITICAL ERROR] LAMMPS binary '{args.lmp_bin}' not found.")
        return False
    return True

def validate_lammps_script(lmp_bin, lmp_file, params, sim_folder):
    command = f"{lmp_bin} -in {lmp_file} -v ktilt {params['ktilt']} -v ksplay {params['ksplay']} -v rcut {params['rcut']} -v wc {params['wc']} -v T {params['T']} -v zeta {params['zeta']} -v N {params['N']} -v d {params['d']:.2f} -skiprun"
    try:
        # Check happens serially, no need for complex MPI binding here
        subprocess.run(command, check=True, shell=True, cwd=sim_folder, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True, ""
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8') if e.stderr else "Unknown error"
        return False, error_msg

def single_sim(args, params, core_queue):
    # Unrestrict Python to ensure we can see all cores
    unrestrict_cpus(args.total_cpus)

    sim_id = f"N_{params['N']}_d_{params['d']}_kt_{params['ktilt']}_ks_{params['ksplay']}_rcut_{params['rcut']}_wc_{params['wc']}_T_{params['T']}_zeta_{params['zeta']}"

    if params['wc'] > params['rcut']:
        return f"[SKIP] {sim_id}: wc > rcut"

    sim_folder = os.path.join(args.path, sim_id)
    create_dir(sim_folder)
    lmp_file = os.path.join(args.path, f"{args.name}.lmp")

    # --- 1. GET TICKET (Core Range) ---
    assigned_cores_str = core_queue.get() 
    
    try:
        # Parse "4-7" into [4, 5, 6, 7]
        start_core, end_core = map(int, assigned_cores_str.split('-'))
        core_list = list(range(start_core, end_core + 1))

        # --- 2. GENERATE RANKFILE (FIXED SYNTAX) ---
        rankfile_path = os.path.join(sim_folder, "rankfile.txt")
        
        # We use socket.gethostname() to be safe, or just 'localhost'
        # If 'localhost' fails again, replace this variable with the output of `hostname` command (e.g., 'md63')
        host_name = "localhost" 

        with open(rankfile_path, "w") as f:
            for rank_idx, core_idx in enumerate(core_list):
                # FIXED SYNTAX: "rank 0=localhost slot=4"
                f.write(f"rank {rank_idx}={host_name} slot={core_idx}\n")

        # Validation
        command = f"-in {lmp_file} -v ktilt {params['ktilt']} -v ksplay {params['ksplay']} -v rcut {params['rcut']} -v wc {params['wc']} -v T {params['T']} -v zeta {params['zeta']} -v N {params['N']} -v d {params['d']:.2f} -skiprun"
        valid, err_msg = validate_lammps_script(args.lmp_bin, lmp_file, params, sim_folder)
        if not valid:
            with open(os.path.join(sim_folder, "error_dryrun.log"), "w") as f:
                f.write(err_msg)
                f.write(command)
            return f"[FAIL] {sim_id}: Validation failed"

        # --- 3. EXECUTION ---
        bash_command = (
            f"mpirun -np {args.nprocs} "
            f"-rf {rankfile_path} "  # Use the rankfile
            f"{args.lmp_bin} -in {lmp_file} "
            f"-v ktilt {params['ktilt']} "
            f"-v ksplay {params['ksplay']} "
            f"-v rcut {params['rcut']} "
            f"-v wc {params['wc']} "
            f"-v T {params['T']} "
            f"-v zeta {params['zeta']} "
            f"-v N {params['N']} "
            f"-v d {params['d']:.2f}"
            f"-v T {params['T']:.2f}"

        )

        if not args.dryrun:
            env = os.environ.copy()
            env['OMP_NUM_THREADS'] = '1'
            
            try:
                with open(os.path.join(sim_folder, "sim.log"), "w") as logfile:
                    subprocess.run(bash_command, check=True, shell=True, cwd=sim_folder, stdout=logfile, stderr=subprocess.STDOUT, env=env)
                return f"[DONE] {sim_id} (Cores {assigned_cores_str})"
            except subprocess.CalledProcessError:
                return f"[ERROR] {sim_id}: Crashed"
        else:
            return f"[DRY RUN] {sim_id} (Cores {assigned_cores_str})"

    finally:
        # --- 4. RETURN TICKET ---
        core_queue.put(assigned_cores_str)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default=os.getcwd())
    parser.add_argument("--name", type=str, default='self_assembly')
    parser.add_argument("--dryrun", action='store_true')
    parser.add_argument("--lmp_bin", type=str, default="lmp_2025")
    parser.add_argument("--nprocs", type=int, default=4)
    parser.add_argument("--total_cpus", type=int, default=os.cpu_count()) # Default to auto-detect

    args = parser.parse_args()

    # --- APPLY JAILBREAK IN MAIN ---
    unrestrict_cpus(args.total_cpus)

    if not check_dependencies(args): return

    params = {
        "ktilt": [12.0,15.0,20.0,30.0,40.0,50.0],
        "ksplay": [0.5,1.0],
        "rcut": [2.5],
        "wc": [2.4],
        "T": [0.25],
        "zeta": [5],
        "N": [2500],
        "d": [0.90]
    }

    # Calculate Workers
    max_workers = args.total_cpus // args.nprocs
    if max_workers < 1: max_workers = 1

    print(f"--- Configuration ---")
    print(f"Total CPUs: {args.total_cpus}")
    print(f"MPI Ranks per Sim: {args.nprocs}")
    print(f"Concurrent Jobs: {max_workers}")
    print(f"---------------------")

    # Initialize Core Queue
    m = multiprocessing.Manager()
    core_queue = m.Queue()

    # Create Core Slots (e.g., 0-3, 4-7, 8-11)
    for i in range(max_workers):
        start = i * args.nprocs
        end = start + args.nprocs - 1
        core_range = f"{start}-{end}"
        core_queue.put(core_range)
        print(f"Initialized Slot {i}: Cores {core_range}")

    # Prepare Jobs
    job_list = []
    keys, values = zip(*params.items())
    for combination in itertools.product(*values):
        combo_dict = dict(zip(keys, combination))
        if combo_dict['rcut'] >= combo_dict['wc']:
            job_list.append(combo_dict)

    print(f"Queuing {len(job_list)} simulations...")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(single_sim, args, p, core_queue): p for p in job_list}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Simulations"):
            result = future.result()
            if "[ERROR]" in result or "[FAIL]" in result:
                tqdm.write(result)

if __name__ == "__main__":
    main()

# python launching_baro.py --path /martini/pietro/new_potential_v2/planar/fluctuation_pipeline/ --name in.baro --lmp_bin lmp_radial --nprocs 2 --total_cpus 24


# nohup python launching_baro.py --path /martini/pietro/new_potential_v2/planar/fluctuation_pipeline/ --name in.baro --lmp_bin lmp_radial --nprocs 4 --total_cpus 16 > log.out 2>&1  &!


