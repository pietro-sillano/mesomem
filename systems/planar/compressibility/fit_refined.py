import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import re
import matplotlib
import multiprocessing
from tqdm import tqdm  # Import tqdm for progress bar

def load_data(file_path):
    """Loads data safely from file."""
    try:
        data = np.loadtxt(file_path, skiprows=1)
        return data
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def analyze_and_plot(data, tmin, tmax, params,filename_prefix="sim", show_plot=False,):
    """
    Plots quantities in a 2x2 grid, highlights the interval, 
    and calculates both Slope (m) and Compressibility Modulus (K)
    using the initial area A0 derived from the fit intercept.
    """
    
    # 1. Unpack Full Data
    VERSION = 'v2'
    
    if VERSION == 'v1':
        t_full = data[:, 0]
        lx_full = data[:, 1]
        ly_full = data[:, 2]
        area_full = data[:, 3]
        tension_full = - data[:, 4] # Assuming tension is negative pressure
        
    if VERSION == 'v2':
        t_full = data[:, 0]
        lx_full = data[:, 1]
        ly_full = data[:, 2]
        lz_full = data[:, 3]
        
        area_full = data[:, 4]
        tension_full = - data[:, 5] 
        tension_sigma = - data[:, 6] 
        tension_sigma_lz = - data[:, 7] 


    # 2. Filter Data (active interval)
    mask = (t_full >= tmin) & (t_full <= tmax)
    
    if not np.any(mask):
        print(f"Warning: No data found in interval {tmin}-{tmax}")
        return None

    t_fit = t_full[mask]
    area_fit = area_full[mask]
    tension_fit = tension_full[mask]
    lx_fit = lx_full[mask]
    ly_fit = ly_full[mask]

    # 3. Perform Fits

    # --- Fit A: Tension vs Time (Drift check) ---
    p_tens, V_tens = np.polyfit(t_fit, tension_fit, 1, cov=True)
    m_tens_drift = p_tens[0] 
    
    # --- Fit B: Area vs Tension (m = dA/dTension) ---
    # Linear equation: Area = m * Tension + A0
    p_area, V_area = np.polyfit(tension_fit, area_fit, 1, cov=True)
    m_slope = p_area[0]       # The slope (dA / dSigma)
    b_intercept = p_area[1]   # The intercept (Area at zero tension -> A0)
    m_slope_err = np.sqrt(V_area[0][0])
    
    # Define A0 from the fit intercept (Equilibrium Area)
    A0_fit = b_intercept 
    # A0_fit = lx_fit[0]*ly_fit[0]
    
    
    
    # print(f"intercept:{b_intercept}, A0:{A0_fit}")
    # print(f"Fitted A0 (Area at zero tension): {A0_fit:.4f}")
    
    # --- Calculation C: Compressibility Modulus (K_A) ---
    # Relation: Sigma = K * (A - A0) / A0
    # Rearranged: A = (A0/K) * Sigma + A0
    # Therefore: Slope m = A0 / K  ->  K = A0 / m
    
    if m_slope != 0:
        K_modulus = A0_fit / m_slope
        # Error propagation: dK = K * (dm/m)
        K_err = np.abs(K_modulus * (m_slope_err / m_slope))
    else:
        K_modulus = 0
        K_err = 0

    # Calculate R-squared
    area_predicted = np.polyval(p_area, tension_fit)
    residuals = area_fit - area_predicted
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((area_fit - np.mean(area_fit))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # 4. Create Subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Analysis Interval: {tmin:.1e} to {tmax:.1e}", fontsize=14)

    # --- Top Left: Area vs Time ---
    ax = axes[0, 0]
    ax.plot(t_full, area_full/params['N'], 'k-', alpha=0.2, label='Full Sim')
    ax.plot(t_fit, area_fit/params['N'], 'b-', label='Fit Region')
    ax.set_ylim(0.2,2.0)
    ax.axvspan(tmin, tmax, color='yellow', alpha=0.1) 
    ax.set_ylabel(r'Area ($\sigma^2$)')
    ax.set_xlabel('Time (LJ)')
    ax.legend(loc='best')
    ax.set_title('Time evolution of Area per Particle')

    # --- Top Right: Tension vs Strain ---
    ax = axes[0, 1]
    
    # Calculate Strain using the fitted A0
    # Strain = (A - A0) / A0
    strain_fit = (area_fit - A0_fit) / A0_fit

    
    ax.plot(strain_fit, tension_fit, 'ro', alpha=0.3, label='Data') 
    
    # Optional: Plot the K slope on the strain graph to verify
    # Sigma = K * Strain
    strain_range = np.linspace(min(strain_fit), max(strain_fit), 10)
    ax.plot(strain_range, K_modulus * strain_range, 'k--', alpha=0.6, label=f'Slope $K_A$')

    ax.legend(loc='best')    
    ax.set_ylabel(r'Tension $\Sigma$')
    ax.set_xlabel(r'Area Strain $(A - A_0) / A_0$')
    ax.set_title('Stress-Strain Relationship')

    # --- Bottom Left: Tension vs Time ---
    ax = axes[1, 0]
    ax.plot(t_full, tension_full, 'k-', alpha=0.2)
    ax.plot(t_fit, tension_fit, 'g-')
    ax.axvspan(tmin, tmax, color='yellow', alpha=0.1)
    ax.set_ylabel('Tension (LJ units)')
    ax.set_xlabel('Time (LJ)')
    ax.set_title(f'Tension Drift Rate: {m_tens_drift:.2e}')

    # --- Bottom Right: Area vs Tension (The Fitting) ---
    ax = axes[1, 1]
    # Sort for plotting line
    sort_idx = np.argsort(tension_fit)
    ax.scatter(tension_fit, area_fit, c='gray', alpha=0.5, s=15, label='Data')
    ax.plot(tension_fit[sort_idx], np.polyval(p_area, tension_fit[sort_idx]), 
            'r--', lw=2, label='Linear Fit')
    
    ax.set_xlabel('Tension (LJ units)')
    ax.set_ylabel(r'Area ($\sigma^2$)')
    
    # Add text box with fit results
    textstr = '\n'.join((
        f'$R^2 = {r_squared:.4f}$',
        f'Slope $m = {m_slope:.2f} \pm {m_slope_err:.2f}$',
        f'$A_0 (fit) = {A0_fit:.2f}$',
        r'$K_A = \frac{A_0}{m} = %.2f \pm %.2f$' % (K_modulus, K_err)
    ))
    props = dict(boxstyle='round', facecolor='white', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    ax.set_title('Constitutive Law (Area vs Tension)')

    plt.tight_layout()
    plt.savefig(f"{filename_prefix}/fit_{int(tmin)}_{int(tmax)}.png", dpi=300)
    
    if show_plot:
        plt.show()
    plt.close()
    
    sigma_max = np.max(tension_full)
    idx_sigma_max = np.argmax(tension_full)
    strain_max = (area_full[idx_sigma_max] - A0_fit) / A0_fit
    print(strain_max)



    return {
        'tmax': tmax,
        'r2': r_squared,
        'm': m_slope,
        'm_err': m_slope_err,
        'A0': A0_fit,
        'K': K_modulus,
        'K_err': K_err,
        'sigma_max':sigma_max,
        'strain_max':strain_max
    }


# ==========================================
# Worker Function
# ==========================================
def process_directory(args):
    """
    Worker function to process a single directory.
    Args:
        args: tuple containing (root, dir_name)
    Returns:
        dict: Result parameters if successful
        None: If skipped or failed
    """
    root, dir_name = args
    full_path = os.path.join(root, dir_name)
    
    # 1. Parse Parameters
    param_matches = param_pattern.findall(dir_name)
    if not param_matches:
        return None

    params = {key: float(value) if '.' in value else int(value)
              for key, value in param_matches}

    # 2. Filter Condition
    # Using .get() is safer in case 'd' is missing from folder name
    # if params.get('d') != 0.80:
    #     return None
    
    # if params.get('kt') != 10.0:
    #     return None

    OUTPUT_FILE = os.path.join(full_path, "area.dat")
    # print(OUTPUT_FILE)
    if not os.path.exists(OUTPUT_FILE):
        return None

    try:
        data = load_data(OUTPUT_FILE)
        if data is None:
            return None

        # print(params)
        # 3. Run Analysis Loop
        if params['N']==2500:
            tmin_values = [x * 1e5 for x in [1.0]]
            tmax_values = [x * 1e5 for x in [1.1,1.2,1.3,1.4,1.50, 2.0]] 

        if params['N']==400:
            tmin_values = [x * 1e5 for x in [1.0,]]
            tmax_values = [x * 1e5 for x in [1.50,1.6,1.7]] 
        results = []

        for t_m in tmax_values:
            for tmin in tmin_values:
                
                res = analyze_and_plot(data, tmin=tmin, tmax=t_m,params=params, show_plot=False, filename_prefix=str(full_path))
                if res:
                    results.append(res)

        if not results:
            return None

        # 4. Generate Summary Plot
        tmax_list = [r['tmax'] for r in results]
        K_list = [r['K'] for r in results]
        Kerr_list = [r['K_err'] for r in results]
        r2_list = [r['r2'] for r in results]
        sigma_max_list = [r['sigma_max'] for r in results]
        strain_max_list = [r['strain_max'] for r in results]

        fig, ax1 = plt.subplots(figsize=(9, 6))

        # Left Axis: R^2
        color = 'tab:blue'
        ax1.set_xlabel(r'Integration limit $t_{max}$')
        ax1.set_ylabel(r'$R^2$ Score', color=color)
        ax1.plot(tmax_list, r2_list, color=color, marker='o', linestyle='-', label='$R^2$')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_ylim(0, 1.05)

        # Right Axis: Compressibility Modulus K
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel(r'Modulus $K_A$ (LJ units)', color=color)
        ax2.errorbar(tmax_list, K_list, yerr=Kerr_list, color=color, fmt='-o', capsize=4, label='$K_A$')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title(r'Stability of Modulus $K_A$ vs Time Interval')
        fig.tight_layout()
        png_file = os.path.join(full_path, "modulus_stability.png")
        plt.savefig(png_file, dpi=300)
        plt.close(fig) 
        
        # 5. Extract Best Results
        best_idx = np.argmax(r2_list)
        best_r2 = r2_list[best_idx]
        best_k =  K_list[best_idx]
        best_kerr = Kerr_list[best_idx]
        best_sigma_max = sigma_max_list[best_idx]
        best_strain_max = strain_max_list[best_idx]

        
        # Update params dictionary
        params['r2'] = best_r2
        params['k'] = best_k
        params['kerr'] = best_kerr
        params['sigma_max'] = best_sigma_max
        params['strain_max'] = best_strain_max


        return params

    except Exception as e:
        print(e)
        return None

# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    
    
    # ==========================================
# Configuration & Setup
# ==========================================

    # Set non-interactive backend for parallel plotting
    matplotlib.use('Agg') 

    base_dir = "/home/pietro/martini/new_potential_v2/area_strain/area_growing_tension"
    output_file = "simulation_summary.csv"
    output_path = os.path.join(base_dir, output_file)

    # Regex Pattern
    param_pattern = re.compile(r'(?:^|_)([a-zA-Z]+)_([\d.]+)')
    
    # 1. Collect all tasks first
    tasks = []
    print("Scanning directories...")
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            tasks.append((root, dir_name))
    
    print(f"Found {len(tasks)} directories. Starting parallel processing...")

    # 2. Run Multiprocessing Pool
    # Uses all available cores by default
    num_processes = multiprocessing.cpu_count() 
    num_processes = 12
    
    data_dict = []
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Use tqdm to wrap the iterator for the progress bar
        # total=len(tasks) helps tqdm estimate ETA
        # unit="dir" labels the counter
        for result in tqdm(pool.imap_unordered(process_directory, tasks), total=len(tasks), unit="dir"):
            if result is not None:
                data_dict.append(result)

    # 3. Write CSV
    if data_dict:
        fieldnames = sorted(set(k for d in data_dict for k in d.keys()))

        with open(output_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_dict)

        print(f"\nSuccessfully exported {len(data_dict)} entries to {output_path}")
    else:
        print("\nNo data found or processed.")
