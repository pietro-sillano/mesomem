import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


plt.rc("font", size=12)  # controls default text size
plt.rc("axes", titlesize=12)  # fontsize of the title
plt.rc("axes", labelsize=12)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=12)  # fontsize of the x tick labels
plt.rc("ytick", labelsize=12)  # fontsize of the y tick labels
plt.rc("legend", fontsize=16)  # fontsize of the legend
plt.rcParams.update({"font.family": "arial"})
cm = 1 / 2.54  # centimeters in inches (for matplotlib figure size)



palette = ["#1f77b4",  # muted blue
           "#ff7f0e",  # orange
           "#2ca02c",  # green
           "#d62728",  # red
           "#9467bd",  # purple
           "#8c564b"]  # brown

df = pd.read_csv("simulation_summary.csv")


# 2. Define Facet variables
kts = sorted(df['kt'].unique())
kss = sorted(df['ks'].unique())

# Define mapping for bilayer status
# 0: Unstable (Red 'X'), 1: Stable (Green 'o')
mapping = {
    0: {"color": "red", "marker": "X", "label": "Unstable"},
    1: {"color": "green", "marker": "o", "label": "Stable"}
}

# 3. Create the figure and axes grid
fig, axes = plt.subplots(
    nrows=len(kts), 
    ncols=len(kss), 
    figsize=(len(kss) * 4, len(kts) * 4), 
    sharex=True, 
    sharey=True,
    constrained_layout=True
)

# If there's only one row or column, subplots returns a 1D array; force it to 2D
if len(kts) == 1: axes = axes[None, :]
if len(kss) == 1: axes = axes[:, None]

# 4. Iterate through the grid and plot
for i, kt in enumerate(kts):
    for j, ks in enumerate(kss):
        ax = axes[i, j]
        subset = df[(df['kt'] == kt) & (df['ks'] == ks)]
        
        # Plot Stable (1) and Unstable (0)
        for state, style in {0: ('red', 'X', 'Unstable'), 1: ('green', 'o', 'Stable')}.items():
            data = subset[subset['bilayer'] == state]
            ax.scatter(
                data['rcut'], data['wc'], 
                c=style[0], marker=style[1], label=style[2],
                s=150, edgecolor="black", linewidth=0.8
            )
        
        # Labels and Titles
        if i == 0: ax.set_title(rf"$k_s = {ks}$")
        if j == 0: ax.set_ylabel(rf"$w_c$ (at $k_t={kt}$)")
        if i == len(kts) - 1: ax.set_xlabel(r"$r_{cut}$")
        
        # # Set ticks using the sorted labels
        # ax.set_xticks(range(len(rcut_order)))
        # ax.set_xticklabels(rcut_order)
        # ax.set_yticks(range(len(wc_order)))
        # ax.set_yticklabels(wc_order)
        


handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), title="Bilayer State", 
           loc='center right', bbox_to_anchor=(1.1, 0.7),fontsize=14)

fig.suptitle("Stability Grid ", fontsize=24)

plt.savefig("stability_plot.png", dpi=500, bbox_inches='tight')
plt.close()




#################################################################
#### PLOT #######################################################

df = pd.read_csv("simulation_summary.csv")


# 2. Define Facet variables
rcuts = sorted(df['rcut'].unique())
wcs = sorted(df['wc'].unique())

# Define mapping for bilayer status
# 0: Unstable (Red 'X'), 1: Stable (Green 'o')
mapping = {
    0: {"color": "red", "marker": "X", "label": "Unstable"},
    1: {"color": "green", "marker": "o", "label": "Stable"}
}

# 3. Create the figure and axes grid
fig, axes = plt.subplots(
    nrows=len(rcuts), 
    ncols=len(wcs), 
    figsize=(len(wcs) * 4, len(rcuts) * 4), 
    sharex=True, 
    sharey=True,
    constrained_layout=True
)

# If there's only one row or column, subplots returns a 1D array; force it to 2D
if len(rcuts) == 1: axes = axes[None, :]
if len(wcs) == 1: axes = axes[:, None]

# 4. Iterate through the grid and plot
for i, rcut in enumerate(rcuts):
    for j, wc in enumerate(wcs):
        ax = axes[i, j]
        subset = df[(df['rcut'] == rcut) & (df['wc'] == wc)]
        
        # Plot Stable (1) and Unstable (0)
        for state, style in {0: ('red', 'X', 'Unstable'), 1: ('green', 'o', 'Stable')}.items():
            data = subset[subset['bilayer'] == state]
            ax.scatter(
                data['kt'], data['ks'], 
                c=style[0], marker=style[1], label=style[2],
                s=150, edgecolor="black", linewidth=0.8
            )
        
        # Labels and Titles
        if i == 0: ax.set_title(rf"$w_c = {wc}$")
        if j == 0: ax.set_ylabel(rf"$k_s$ (at $r_c={rcut}$)")
        if i == len(rcuts) - 1: ax.set_xlabel(r"$k_t$")
        
        # # Set ticks using the sorted labels
        # ax.set_xticks(range(len(rcut_order)))
        # ax.set_xticklabels(rcut_order)
        # ax.set_yticks(range(len(wc_order)))
        # ax.set_yticklabels(wc_order)
        


handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), title="Bilayer State", 
           loc='center right', bbox_to_anchor=(1.1, 0.7),fontsize=14)

fig.suptitle("Stability Grid ", fontsize=24)

plt.savefig("stability_plot2.png", dpi=500, bbox_inches='tight')
plt.close()
