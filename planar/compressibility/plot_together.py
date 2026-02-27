import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import numpy as np

palette = ["#1f77b4",  # muted blue
           "#ff7f0e",  # orange
           "#2ca02c",  # green
           "#d62728",  # red
           "#9467bd",  # purple
           "#8c564b"]  # brown

# Load CSV file
csv_file = "simulation_summary.csv" 
df = pd.read_csv(csv_file)

wc = 2.0
wc = 2.2
N = 2500
if N==400:
    scale_factor = 40 # for N=2500
elif N==2500:
    scale_factor = 15 # for N=400

mask = (df['r2'] > 0.9) & (df['N']==N) & (df['T']<0.5) & (df['k']>0.0) & (df['wc']==wc)
df_filt = df[mask].copy()


df_filt['k_scaled'] = df_filt['k'] / df_filt['T'] * scale_factor
df_filt['kerr_scaled'] = df_filt['kerr'] / df_filt['T'] * scale_factor

# Get unique temperatures and sort them
temps = np.sort(df_filt['T'].unique())

# --- 2. Plotting Configuration ---
# Generate a color palette if 'palette' isn't defined externally
# if 'palette' not in locals():
    # consistent colors based on number of temperatures
colors = cm.viridis(np.linspace(0, 1, len(temps)))
# else:
    # colors = palette

# Use a style context for cleaner, publication-quality plots
with plt.style.context('seaborn-v0_8-whitegrid'):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Iterate and plot
    for i, T in enumerate(temps):
        # Filter and explicit sort by x-axis (zeta) to prevent "zigzag" lines
        subset = df_filt[df_filt['T'] == T].sort_values(by='zeta')
        
        # Select color
        c = colors[i] if isinstance(colors, list) else colors[i]

        ax.errorbar(
            subset['zeta'], 
            subset['k_scaled'], 
            yerr=subset['kerr_scaled'],
            label=f'T = {T}',
            color=c,
            marker='o',         # Circle markers
            markersize=8,       # Slightly larger markers
            linestyle='-',      # Continuous line
            linewidth=3,        # Thicker line for visibility
            capsize=8,          # Caps on error bars
            capthick=1.5,       # Thickness of caps
            elinewidth=1.5,     # Thickness of error bar lines
            alpha=0.9           # Slight transparency
        )

    # ax.set_ylim(0,200)
    # --- 3. Labels and Final Touches ---
    ax.set_title(r"Compressibility modulus $K_A$", fontsize=16, pad=15)
    ax.set_xlabel(r"$\zeta$", fontsize=14)
    ax.set_ylabel(r"$K_A \;\; [k_B T / \sigma^2]$", fontsize=14)
    
    # Improve tick readability
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Legend with slightly semi-transparent background
    ax.legend(title="Temperature (T)", title_fontsize=14, fontsize=14, frameon=True, framealpha=0.9)

    # Save
    plt.tight_layout()
    plt.savefig(f"ka_wc_{wc}_N_{N}.png",transparent=True, dpi=400)
    plt.show()




# Use a style context for cleaner, publication-quality plots
with plt.style.context('seaborn-v0_8-whitegrid'):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Iterate and plot
    for i, T in enumerate(temps):
        # Filter and explicit sort by x-axis (zeta) to prevent "zigzag" lines
        subset = df_filt[df_filt['T'] == T].sort_values(by='zeta')
        
        # Select color
        c = colors[i] if isinstance(colors, list) else colors[i]

        ax.plot(
            subset['zeta'], 
            subset['sigma_max'], 
            label=f'T = {T}',
            color=c,
            marker='o',         # Circle markers
            markersize=8,       # Slightly larger markers
            linestyle='-',      # Continuous line
            linewidth=3,        # Thicker line for visibility
            alpha=0.9           # Slight transparency
        )

    # ax.set_ylim(0,200)
    # --- 3. Labels and Final Touches ---
    ax.set_title(r"Maximum tension $\Sigma$", fontsize=16, pad=15)
    ax.set_xlabel(r"$\zeta$", fontsize=14)
    # ax.set_ylabel(r"$K_A \;\; [k_B T / \sigma^2]$", fontsize=14)
    
    # Improve tick readability
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Legend with slightly semi-transparent background
    ax.legend(title="Temperature (T)", title_fontsize=14, fontsize=14, frameon=True, framealpha=0.9)

    # Save
    plt.tight_layout()
    plt.savefig(f"sigma_max_wc_{wc}_N_{N}.png",transparent=True, dpi=400)
    plt.show()



mask = (df['r2'] > 0.9) & (df['N']==N) & (df['T']<0.5) & (df['strain_max']>0.0) & (df['wc']==wc)
df_filt = df[mask].copy()

# Use a style context for cleaner, publication-quality plots
with plt.style.context('seaborn-v0_8-whitegrid'):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Iterate and plot
    for i, T in enumerate(temps):
        # Filter and explicit sort by x-axis (zeta) to prevent "zigzag" lines
        subset = df_filt[df_filt['T'] == T].sort_values(by='zeta')
        
        # Select color
        c = colors[i] if isinstance(colors, list) else colors[i]

        ax.plot(
            subset['zeta'], 
            subset['strain_max'], 
            label=f'T = {T}',
            color=c,
            marker='o',         # Circle markers
            markersize=8,       # Slightly larger markers
            linestyle='-',      # Continuous line
            linewidth=3,        # Thicker line for visibility
            alpha=0.9           # Slight transparency
        )

    # ax.set_ylim(0,200)
    # --- 3. Labels and Final Touches ---
    ax.set_title(r"Maximum strain $(A-A_0)/A_0$", fontsize=16, pad=15)
    ax.set_xlabel(r"$\zeta$", fontsize=14)
    ax.set_ylabel(r"$(A-A_0)/A_0$", fontsize=14)
    
    # Improve tick readability
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Legend with slightly semi-transparent background
    ax.legend(title="Temperature (T)", title_fontsize=14, fontsize=14, frameon=True, framealpha=0.9)

    # Save
    plt.tight_layout()
    plt.savefig(f"strain_max_wc_{wc}_N_{N}.png",transparent=True, dpi=400)
    plt.show()
