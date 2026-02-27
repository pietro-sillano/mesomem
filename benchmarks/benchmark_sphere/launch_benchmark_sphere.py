import subprocess
import os
import argparse
import time
import matplotlib.pyplot as plt
import csv
import pandas as pd



def create_dir(directory_path):
    os.makedirs(directory_path, exist_ok=True)


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_problem_scaling(csv_file='benchmark_results.csv'):
    # Load data
    df = pd.read_csv(csv_file)
    
    # Calculate Parallel Efficiency (Speedup / Number of CPUs)
    # Efficiency of 1.0 (100%) is perfect linear scaling.
    # df['Efficiency'] = df['Speedup'] / df['CPU']

    # Setup the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Get unique CPU counts to create different lines
    unique_cpus = sorted(df['CPU'].unique())
    
    # Use a color map to differentiate CPU counts clearly
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_cpus)))

    for i, cpu in enumerate(unique_cpus):
        # Skip the base case (1 CPU) if speedup is always 1.0, 
        # but usually it's good to keep for reference or start from 2.
        if cpu == 1:
            continue

        # Filter for this specific CPU count and sort by N_atoms (Problem Size)
        subset = df[df['CPU'] == cpu].sort_values('N_atoms')
        
        # Plot Speedup vs N_atoms
        # We add markers to see the exact data points
        ax1.plot(subset['N_atoms'], subset['Efficiency'], 
                 marker='o', label=f'{cpu} CPUs', color=colors[i], linewidth=2)

    # Formatting X-Axis (Problem Size)
    ax1.set_xscale('log')
    ax1.set_xlabel('Total Number of Atoms ($N_{atoms}$)', fontsize=12)
    ax1.set_ylabel('Efficiency (Higher is more effficient)', fontsize=12)
    ax1.set_title('Efficiency by Problem Size', fontsize=14)
    # ax1.set_yticks([1,10,50,100],[1,10,50,100])
    
    # Add a reference line for N=2500 and N=50k to help you read the graph
    plt.axvline(x=2500, color='gray', linestyle=':', alpha=0.7)
    plt.text(2500, ax1.get_ylim()[1]*0.9, ' N=2.5k', color='gray', verticalalignment='top')
    
    plt.axvline(x=10000, color='gray', linestyle=':', alpha=0.7)
    plt.text(10000, ax1.get_ylim()[1]*0.9, ' N=10k', color='gray', verticalalignment='top')
    
        
    plt.axvline(x=100000, color='gray', linestyle=':', alpha=0.7)
    plt.text(100000, ax1.get_ylim()[1]*0.9, ' N=100k', color='gray', verticalalignment='top')

    # Add Grid and Legend
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.legend(title="Parallelism", loc='upper left')

    plt.tight_layout()
    plt.savefig('problem_size_scaling.png', dpi=300)
    print("[✓] Plot saved as problem_size_scaling.png")


def plot_grain_size_vs_speedup(csv_file='benchmark_results.csv'):
    # Load the data from the CSV
    df = pd.read_csv(csv_file)
    
    # Calculate Grain Size (Workload per Core)
    df['Atoms_per_Core'] = df['N_atoms'] / df['CPU']
    
    plt.figure(figsize=(10, 6))
    
    # We group by CPU to see how speedup for a specific core count 
    # reacts to increasing the workload density
    unique_cpus = sorted(df['CPU'].unique())
    base_cpu = unique_cpus[0]

    for cpu in unique_cpus:
        # We focus on parallel runs (Speedup > 1)
        if cpu == base_cpu:
            continue
            
        subset = df[df['CPU'] == cpu].sort_values('Atoms_per_Core')
        plt.plot(subset['Atoms_per_Core'], subset['Speedup'], 
                 marker='o', label=f'{cpu} MPI Tasks')

    # Log scale is recommended as grain size often spans orders of magnitude
    plt.xscale('log')
    plt.xlabel('Grain Size ($N_{atoms} / CPU$)', fontsize=12)
    plt.ylabel('Speedup', fontsize=12)
    plt.title('Speedup vs. Workload Density (Grain Size)', fontsize=14)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(title="Parallelism")
    
    plt.tight_layout()
    plt.savefig('grain_size_speedup_plot.png', dpi=500, transparent=True)
    print("[✓] Plot saved as grain_size_speedup_plot.png")

def plot_benchmarks_from_csv(csv_file='benchmark_results.csv'):
    # Load the data
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"[X] Error: {csv_file} not found.")
        return

    system_sizes = sorted(df['N_atoms'].unique())
    min_cpu = df['CPU'].min()
    max_cpu = df['CPU'].max()

    # --- Figure 1: Speedup Plot ---
    plt.figure(figsize=(8, 6))
    for n_tot in system_sizes:
        # Filter and sort by CPU count
        data = df[df['N_atoms'] == n_tot].sort_values('CPU')
        plt.plot(data['CPU'], data['Speedup'], marker='o', label=f'$N_{{atoms}} = {n_tot}$')

    # Plot Ideal Linear Speedup line
    # Ideal Speedup = Current_CPU / Base_CPU (usually 1 if base is 1)
    # If base is e.g. 4, ideal is current/4.
    base_cpu = min_cpu
    plt.loglog([min_cpu, max_cpu], [1, max_cpu / base_cpu], 'k--', label='Ideal Scaling', alpha=0.7)

    plt.xlabel('Number of MPI Tasks')
    plt.ylabel('Speedup (relative to base)')
    plt.xticks(df['CPU'].unique(), [str(x) for x in df['CPU'].unique()])
    plt.title('LAMMPS Benchmark: Parallel Speedup')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.savefig('speedup_plot.png', dpi=500, transparent=True)
    print("[✓] Speedup plot saved as speedup_plot.png")
    plt.close()

    # --- Figure 2: Efficiency Plot ---
    plt.figure(figsize=(8, 6))
    for n_tot in system_sizes:
        data = df[df['N_atoms'] == n_tot].sort_values('CPU')
        plt.plot(data['CPU'], data['Efficiency'], marker='o', label=f'$N_{{atoms}} = {n_tot}$')

    # Plot Ideal Efficiency line (constant 1.0)
    plt.axhline(y=1.0, color='k', linestyle='--', label='Ideal (100%)', alpha=0.7)

    plt.xlabel('Number of MPI Tasks')
    plt.ylabel('Parallel Efficiency')
    plt.title('LAMMPS Benchmark: Efficiency')
    plt.ylim(0, 1.1)  # Efficiency is usually between 0 and 1
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.savefig('efficiency_plot.png', dpi=500, transparent=True)
    print("[✓] Efficiency plot saved as efficiency_plot.png")
    plt.close()
    
    
    # --- Figure 3: speedup time Plot ---
    plt.figure(figsize=(8, 6))
    for n_tot in system_sizes:
        data = df[df['N_atoms'] == n_tot].sort_values('CPU')
        plt.plot(data['CPU'], data['Speed_up_time'], marker='o', label=f'$N_{{atoms}} = {n_tot}$')

    # Plot Ideal Efficiency line (constant 1.0)
    # plt.axhline(y=1.0, color='k', linestyle='--', label='Ideal (100%)', alpha=0.7)


    plt.xlabel('Number of MPI Tasks')
    plt.ylabel('Time speedup')
    plt.title('LAMMPS Benchmark: Time speedup')
    # plt.ylim(0, 1.1)  # Efficiency is usually between 0 and 1
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.savefig('time_speedup.png', dpi=500, transparent=True)
    print("[✓] Speed up time plot saved as time_speedup.png")
    plt.close()

def parse_log(log_path):
    """
    Parses the log.lammps file to find the last occurrence of the performance line.
    Target format: "Performance: 803288.941 tau/day, 929.733 timesteps/s, ..."
    """
    timesteps_per_sec = None
    
    if not os.path.exists(log_path):
        print(f"[!] Log file not found: {log_path}")
        return None

    with open(log_path, 'r') as f:
        for line in f:
            if "Performance:" in line and "timesteps/s" in line:
                # Example split: ['Performance: 803288.941 tau/day', ' 929.733 timesteps/s', ' ...']
                parts = line.split(',')
                for p in parts:
                    if "timesteps/s" in p:
                        # Extract the number before "timesteps/s"
                        try:
                            timesteps_per_sec = float(p.strip().split()[0])
                        except ValueError:
                            pass
    return timesteps_per_sec



def single_sim(args, n_tot, n_cpu):
    """
    Runs a single simulation and returns performance metrics.
    """
    # Calculate total atoms (approx n_side^2) for naming/logging
    
    sim_folder = os.path.join(args.path, f"N_{n_tot}_cpu_{n_cpu}")
    create_dir(sim_folder)
    
    # 2. Prepare LAMMPS command
    # Using absolute path for input file if it's in the root benchmark folder
    input_script_path = os.path.abspath(f"{args.name}.lmp") 
    
    # Switch context to sim folder
    original_dir = os.getcwd()
    os.chdir(sim_folder)
    
    print(f"--- Running N={n_tot} on {n_cpu} CPUs ---")
        
    if n_tot> 10000 and n_cpu <= 16:
        trun = 100
    else:
        trun = 5000
    bash_command = (f"mpirun -np {n_cpu} -bind-to core -use-hwthread-cpus  {args.lmp_bin} -in {input_script_path} -v N {n_tot} -v t_run {trun}")

    start_time = time.time()
    timesteps_per_sec = 0.0
    wall_time = 0.0

    try:
        # Redirect stdout to a specific log file or let LAMMPS handle log.lammps default
        subprocess.run(bash_command, check=True, shell=True, stdout=subprocess.DEVNULL)
        
        end_time = time.time()
        wall_time = end_time - start_time
        if n_tot> 10000 and n_cpu <= 16:
            wall_time = wall_time * 50
        
        # 3. Parse output
        log_file = "log.lammps"
        timesteps_per_sec = parse_log(log_file)
        
        print(f"[✓] Done. Wall Time: {wall_time:.2f}s | Speed: {timesteps_per_sec} steps/s")

    except subprocess.CalledProcessError as e:
        print(f"[X] Simulation failed: {e}")
    
    # Restore directory
    os.chdir(original_dir)
    
    return wall_time, timesteps_per_sec



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default=os.getcwd())
    parser.add_argument("--name", type=str, default='in.sphere_benchmark')
    parser.add_argument("--lmp_bin", type=str, default="lmp_radial")
    
    args = parser.parse_args()
    
    csv_file = "benchmark_results.csv"
    COMPUTE = True
    PLOT = True
    
    
    # python launch_benchmark.py
    
    if COMPUTE:
        # Simulation Parameters
        # N represents the side length for planar_lattice.py
        # Resulting atoms approx N^2: 20->400, 50->2500, 100->10k, 320->102.4k
        
        
        n_atoms = [500,2000,8000,18000,50000] 
        cpu_list = [128,64,32,16,8,4,2,1]
               
        # Store results: (N_total, cpu, wall_time, timesteps_per_sec)
        results = []

        print(f"Starting Benchmark...")
        print(f"Sizes (side): {n_atoms}")
        print(f"CPUs: {cpu_list}")
        print("------------------------------------------------")

        for n in n_atoms:
            for cpu in cpu_list:         
                wall, tps = single_sim(args, n, cpu)
                if tps is not None:
                    results.append((n, cpu, wall, tps))
                    


        # 1. Identify baseline performance (TPS) and baseline CPU count for each system size
        baselines = {}
        unique_sizes = set(r[0] for r in results)

        for n_size in unique_sizes:
            size_results = [r for r in results if r[0] == n_size]
            # Find the entry with the minimum CPU count for this specific N
            base_case = min(size_results, key=lambda x: x[1]) 
            baselines[n_size] = {
                'tps': base_case[3],
                'time':base_case[2],
                'cpu': base_case[1]
            }

        # 2. Prepare final data with Speedup and Efficiency calculations
        final_data = []
        for n_tot, cpu, wall, tps in results:
            base_tps = baselines[n_tot]['tps']
            base_cpu = baselines[n_tot]['cpu']
            base_time = baselines[n_tot]['time']
            
            # Speedup: How much faster is this compared to the base?
            speedup = tps / base_tps
            speedup_time = base_time / wall
            
            # Efficiency: Speedup / (CPU Ratio)
            # If using 4 CPUs as base and 8 CPUs as current, ratio is 2.0.
            cpu_ratio = cpu / base_cpu
            efficiency = speedup / cpu_ratio
            
            final_data.append((n_tot, cpu, wall, round(tps, 2), round(speedup, 3), round(efficiency, 3), round(speedup_time, 3),))

        # 3. Save to CSV
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["N_atoms", "CPU", "Wall_Time_s", "Timesteps_per_s", "Speedup", "Efficiency","Speed_up_time"])
            writer.writerows(final_data)

        print(f"[✓] Results with Efficiency saved to {csv_file}")
    
    if PLOT:
        plot_benchmarks_from_csv(csv_file=csv_file)
        plot_grain_size_vs_speedup()
        plot_problem_scaling()


if __name__ == "__main__":
    main()
    
    # mpirun -np 24 -bind-to core -use-hwthread-cpus lmp_radial  -in in.planar_radial.lmp -v N 2500
