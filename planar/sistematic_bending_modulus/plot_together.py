import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

def extract_wc(path_str):
    """
    Attempts to extract 'wc' value from a path string like '..._wc_2.5_...'
    Returns the path name if regex fails.
    """
    # Regex for wc followed by float/int
    match = re.search(r'wc_?([0-9]*\.?[0-9]+)', path_str)
    if match:
        return f"$w_c = {match.group(1)}$"
    return path_str # Fallback

def main():
    parser = argparse.ArgumentParser(description="Plot 3 spectra together")
    parser.add_argument('paths', nargs=3, help="Paths to the 3 simulation folders")
    parser.add_argument('--out', default="comparison_spectrum.png", help="Output filename")
    args = parser.parse_args()

    plt.figure(figsize=(7, 6))

    # Colors for distinct plotting
    colors = ['#0072B2', '#D55E00', '#F0E442']
    colors = ['#56B4E9', '#E69F00', '#009E73'] 

    x_min_plot = 0.09
    x_max_plot = 2
    
    # x_min_fit = 0.13
    # x_max_fit = 0.8
    
    labels=[r'$w_c=1.8$',r'$w_c=2.0$',r'$w_c=2.2$']

    for i, p_str in enumerate(args.paths):
        path = Path(p_str)
        csv_path = path / "spectrum.csv"

        if not csv_path.exists():
            print(f"Warning: {csv_path} not found. Skipping.")
            continue

        # Read Data
        df = pd.read_csv(csv_path)
        
        df2 = pd.read_csv(path / "fit_report.dat", sep=' ', names=['modes','qmin','qmax','k','kerr','Q','r2'],skiprows=1)
        

        # Assume columns are q, v (value), e (error)
        # If 'u' exists as string representation of ufloat, might need parsing,
        # but usually 'v' and 'e' are saved separately in previous scripts.
        if 'v' not in df.columns:
            # Fallback for complex parsing if needed, but assuming standard format
            continue

        q = df['q']
        v = df['v']
        mask = (q > x_min_plot) & (q < x_max_plot)
        q = q[mask]
        v = v[mask]

        # Find the value of 'k' where 'r2' is at its maximum
        best_k = float(df2.loc[df2['r2'].idxmax(), 'k'])
        
        x_min_fit = df2['qmin']
        x_min_fit = 0.14
        x_max_fit = df2['qmax']

        # Label extraction
        # label = extract_wc(str(path.name))

        plt.loglog(q, v, marker='+', linestyle='-', linewidth=0,
                   markersize=4, color=colors[i], label=labels[i], alpha=1.0)
        
        x_guide = np.linspace(x_min_fit, x_max_fit, 20)
        plt.plot(x_guide, (0.25/best_k)*x_guide**-4, color=colors[i],alpha=1.0)
        

    # Styling
    plt.xlabel(r"Wavenumber $q / \sigma^{-1}$", fontsize=12)
    plt.ylabel(r"Scaled power $\langle h^2 \rangle L^2 / \sigma^4$", fontsize=12)

    # Add a guide to the eye (q^-4)
    plt.xticks([0.1,0.5,1.0],[0.1,0.5,1.0])

    # plt.ylim(1e-2,1e2)
    plt.legend(frameon=False, fontsize=12)
    plt.grid(True, which='major', linestyle='-', alpha=0.2)
    plt.tight_layout()

    print(f"Saving comparison plot to {args.out}")
    plt.savefig(args.out,dpi=500,transparent=True)
    plt.show()

if __name__ == "__main__":
    
    # python plot_together.py N_2500_d_0.8_kt_15.0_ks_15.0_rcut_2.5_wc_2.0_T_0.25_zeta_6 N_2500_d_0.8_kt_15.0_ks_15.0_rcut_2.5_wc_1.8_T_0.25_zeta_6 N_2500_d_0.8_kt_15.0_ks_15.0_rcut_2.5_wc_1.6_T_0.25_zeta_6 --out comparison_spectrum.png

    main()
