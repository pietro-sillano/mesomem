import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import re

# Import tools from your provided library
from fancy_spectrum import (
    calc_hfield,
    thermo_2_df_pietro,
    zL2u,
    Model_f_u_k,
    series2ufloat
)

def analyze_and_fit(path: Path, filename, n_modes: int, q_ranges: list):
    """
    1. loads/calculates spectrum
    2. saves spectrum.csv
    3. loops over q_ranges to fit and plot
    """

    # --- 1. PREPARE DATA ---
    # Check for Box Size
    box_file = path / "boxsize.dat"
    if not box_file.exists():
        print(f"Error: {box_file} not found. Cannot calculate L_avg.")
        return

    df_box = thermo_2_df_pietro(box_file)
    # Filter valid data (simple equilibration cut example)
    step_discard = 1e5
    df_valid = df_box[df_box["step"] > step_discard]

    lx_ufloat = series2ufloat(np.array(df_valid["f_avg_lx"]))
    L_avg = lx_ufloat.n
    print(f"L_avg: {L_avg:.4f}")

    # Calculate or Load Spectrum
    spectrum_csv_path = path / "spectrum.csv"

    # If we want to recalculate or it doesn't exist
    global RECALC
    if not spectrum_csv_path.exists()  or RECALC:
        print("Calculating Height Field and Spectrum...")
        Z = calc_hfield(path / filename, n_modes=n_modes, sel=slice(0, -1, 1))

        # Convert to Spectrum
        # (Assuming step discard logic is applied to the dataset indices)
        z_ds = Z.sel(step=slice(step_discard, None)).swap_dims({"step": "time"})

        u = zL2u(z_ds, L_avg=L_avg)
        spectrum = (
            u.to_dataframe()
            .drop(columns=["nx", "ny"])
            .rename(columns={"nn": "n"})
            .reset_index()
            .sort_values("n")
        )
        spectrum.to_csv(spectrum_csv_path)
    else:
        print("Loading existing spectrum.csv...")
        spectrum = pd.read_csv(spectrum_csv_path)

    # Filter valid modes
    spectrum = spectrum.query("ok")

    # --- 2. FIT AND PLOT LOOP ---
    # Append to report
    with open(path / "fit_report.dat", "w") as f:
            f.write("n_modes  qmin  qmax  k  kerr  Q  r2\n")
            
            
    for (qmin, qmax) in q_ranges:
        print(f"Fitting range: {qmin} - {qmax}")

        # Prepare Data for Fit
        if "u" in spectrum:
            # Handle if u is ufloat (unlikely after CSV read, usually string or float columns)
            # If reading from CSV, columns are likely 'q', 'v', 'e' (value, error)
            pass

        # Robust column extraction assuming CSV structure from fancy_spectrum
        x = spectrum["q"].values
        y = spectrum["v"].values if "v" in spectrum else spectrum["u"].apply(lambda x: x.n).values
        e = spectrum["e"].values if "e" in spectrum else spectrum["u"].apply(lambda x: x.s).values

        # Selection
        mask = (x >= qmin) & (x <= qmax)
        x_fit, y_fit, e_fit = x[mask], y[mask], e[mask]

        if len(x_fit) < 3:
            print(f"Skipping range {qmin}-{qmax}: Not enough points.")
            continue

        # Fit
        model = Model_f_u_k()
        res = model.fit(x_fit, y_fit, e_fit)


        # Plot
        plt.figure(figsize=(6, 5))
        plt.loglog(x, y, 'o', markersize=2, color='black', alpha=0.6, label='Data')

        # Plot Theory over range
        x_line = np.logspace(np.log10(qmin), np.log10(qmax), 100)
        y_line = model.func(x_line, *res.popt)
        plt.plot(x_line, y_line, 'r--', lw=2, label=rf'Fit $\kappa={res.popt[0]:.2f}$')

        # Formatting
        # Scientific notation for Q, 3 decimal float for R2
        title_str = rf"$Q = {res.Q:.3e} \quad R^2 = {res.r2:.3f}$"
        plt.title(title_str, fontsize=14)
        plt.xlabel(r"$q$")
        plt.ylabel(r"Spectrum $u(q)$")
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.4)

        # Significant Filename
        out_name = f"spectrum_fit_qmin_{qmin:.2f}_qmax_{qmax:.2f}.pdf"
        plt.savefig(path / out_name)
        plt.close()

        # Append to report
        with open(path / "fit_report.dat", "a") as f:
             f.write(f"{n_modes} {qmin} {qmax} {res.popt[0]:.4f} {res.perr[0]:.2f} {res.Q:.4e} {res.r2:.4f}\n")

def main():
    
    # Regex pattern to capture parameters from folder names
    pattern = r"N_(?P<N>[\d.]+)_d_(?P<d>[\d.]+)_kt_(?P<kt>[\d.]+)_ks_(?P<ks>[\d.]+)_rcut_(?P<rcut>[\d.]+)_wc_(?P<wc>[\d.]+)_T_(?P<T>[\d.]+)_zeta_(?P<zeta>[\d.]+)"

    base_dir = Path(".") 

    # 2. Crawl directories and extract data
    print(f"Scanning directories for processing dumps")

    for folder in base_dir.iterdir():
        if folder.is_dir():
            match = re.search(pattern, folder.name)
            if match:
                # Extract parameters and convert to float
                params = {k: float(v) for k, v in match.groupdict().items()}
                
                if params['N']==400:
                    nmodes = 20
                    fit_ranges = [(0.2,1.0),(0.2,1.2),(0.2,1.5)
                    ]
                elif params['N']==2500:
                    nmodes = 50
                    fit_ranges = [(0.1,0.7),(0.1,0.8)]
                                    
                file_path = folder  
                coords_file = "position_run.lammpstrj"
                if file_path.exists():
                    analyze_and_fit(file_path, coords_file, nmodes, fit_ranges)

if __name__ == "__main__":
    RECALC  = False  # produce the spectrum again (and spectrum.csv)

    main()
