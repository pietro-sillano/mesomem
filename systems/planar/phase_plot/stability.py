import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


plt.rc("font", size=10)  # controls default text size
plt.rc("axes", titlesize=10)  # fontsize of the title
plt.rc("axes", labelsize=10)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=10)  # fontsize of the x tick labels
plt.rc("ytick", labelsize=10)  # fontsize of the y tick labels
plt.rc("legend", fontsize=6)  # fontsize of the legend
plt.rcParams.update({"font.family": "arial"})
cm = 1 / 2.54  # centimeters in inches (for matplotlib figure size)



palette = ["#1f77b4",  # muted blue
           "#ff7f0e",  # orange
           "#2ca02c",  # green
           "#d62728",  # red
           "#9467bd",  # purple
           "#8c564b"]  # brown

# Load CSV file
csv_file = "simulation_summary.csv" 
df = pd.read_csv(csv_file)


# Print entries where bilayer is True but stability is -1
mask = (df['bilayer'] == True) & (df['valid'] == -1)
if df[mask].shape[0] > 0:
    print("Entries with bilayer=True and stability=-1:")
    print(df[mask])
    print(df[mask]['path'],df[mask]['zeta'])
    # Change bilayer to False for these entries
    df.loc[mask, 'bilayer'] = False


df['alpha'] = df['alpha'].fillna(0)

wc = 2.0
kt = 5.0
ks = 0.0


for kt in [15.0]:
    for ks in [1.0]:
        for wc in [2.0]:
            df_filt = df[(df['wc'] == wc) & (df['kt']==kt) & (df['ks']==ks)]
            

            df_filt1 = df_filt[(df_filt['rcut'] == 2.5)]
            
            pivot_table = df_filt1.pivot_table(index='T', columns='zeta', values='alpha', aggfunc='mean')
            
            # Heatmap of n_clusters as a function of zeta and T
            # fig_size = (12 * cm, 5 * cm)
            plt.figure(figsize=(8, 6))
            ax = sns.heatmap(pivot_table, cmap="viridis", annot=True,fmt=".2f",cbar=False)
            ax.invert_yaxis()
            cbar = plt.colorbar(ax.collections[0], ax=ax, extend='max')
            cbar.set_label(r'$\alpha$')
            # cbar.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
            ax.collections[0].set_clim(0, 2.0)
            plt.title(f"alphas wc:{wc} kt:{kt} ks:{ks}")
            plt.xlabel(r"$\zeta$")
            plt.ylabel(r"T")
            plt.tight_layout()
            plt.savefig(f"alphas_wc_{wc}_kt_{kt}_ks_{ks}.png",dpi=500)
            plt.close()