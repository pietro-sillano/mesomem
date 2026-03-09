import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D

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
    # Change bilayer to False for these entries
    df.loc[mask, 'bilayer'] = False

# if alpha is lower than 0.6 set D_2d to zero
df.loc[df['alpha'] < 0.5, 'D_2d'] = 0.0



########################################
# plot with the scaling temperature
########################################
# df_filt = df[(df['ks'] == 10.0) & (df['kt'] == 10.0)]
# df_filt = df
# unique_T = df_filt['T'].unique()
# # Continuous colormap
# cmap = cm.viridis  
# # Use your raw T values for limits
# vmin, vmax = df_filt['T'].min(), df_filt['T'].max()
# norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

# fig, ax = plt.subplots(figsize=(7, 5))
# for i, T in enumerate(unique_T):
#     df_filt_T = df_filt[(df_filt['T'] == T)]
#     y1 = df_filt_T[(df_filt_T['rcut'] == 3.0)]
#     y2 = df_filt_T[(df_filt_T['rcut'] == 2.6)]
#     y1_sorted = y1.sort_values('zeta')
#     y2_sorted = y2.sort_values('zeta')

#     plt.errorbar(
#         y2_sorted['zeta'], y2_sorted['D_2d'],
#         label='rcut=2.6', fmt='s--', color=cmap(norm(T)), capsize=5, elinewidth=2, markeredgewidth=2
#     )
#     plt.errorbar(
#         y1_sorted['zeta'], y1_sorted['D_2d'], label='rcut=3.0', fmt='o-', color=cmap(norm(T)), capsize=5, elinewidth=2, markeredgewidth=2
#     )
    
# # Create colorbar with real T values
# sm = cm.ScalarMappable(cmap=cmap, norm=norm)
# sm.set_array([])  
# cbar = fig.colorbar(sm, ax=ax)   # <--- explicitly bind to 'ax'
# cbar.set_label("T")
# cbar.set_ticks(sorted(df_filt['T'].unique()))   # ticks exactly at your T values

# plt.ylim(-0.001, 0.02)  # Set y-axis range
# plt.xlabel(r"$\zeta$")
# plt.ylabel(r"D $[\sigma^2 \tau^{-1}]$")
# plt.title(r"Diffusion coefficient $w_c=2.6$")
# # legend = plt.legend(title="Rcut Value", loc="best")
# # Custom legend: only two entries
# custom_handles = [
#     Line2D([0], [0], color='black', alpha=0.7, linestyle='--', marker='s', label=r"$r_{\text{cut}}=2.6$"),
#     Line2D([0], [0], color='black', alpha=0.7, linestyle='-',  marker='o', label=r"$r_{\text{cut}}=3.0$"),
# ]
# ax.legend(handles=custom_handles, title=r"", loc="best")
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.tight_layout()
# plt.savefig("diff_coeff_zeta_T.png", dpi=300)
# plt.close()



########################################
# plot with the scaling temperature
########################################


for kt in [15.0]:
    for ks in [1.0]:
        for wc in [2.0]:
            df_filt = df[(df['wc'] == wc) & (df['kt']==kt) & (df['ks']==ks)]    
            unique_T = df_filt['T'].unique()
            # Continuous colormap
            cmap = cm.viridis  
            # Use your raw T values for limits
            vmin, vmax = df_filt['T'].min(), df_filt['T'].max()
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

            fig, ax = plt.subplots(figsize=(7, 5))
            for i, T in enumerate(unique_T):
                df_filt_T = df_filt[(df_filt['T'] == T)]
                y1 = df_filt_T[(df_filt_T['rcut'] == 2.5)]
                y1_sorted = y1.sort_values('zeta')
                plt.errorbar(
                    y1_sorted['zeta'], y1_sorted['D_2d'], label='rcut=3.0', fmt='o-', color=cmap(norm(T)), capsize=5, elinewidth=2, markeredgewidth=2
                )
                
            # Create colorbar with real T values
            sm = cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])  
            cbar = fig.colorbar(sm, ax=ax)   # <--- explicitly bind to 'ax'
            cbar.set_label("T")
            cbar.set_ticks(sorted(df_filt['T'].unique()))   # ticks exactly at your T values

            plt.ylim(-0.0001, 0.004)  # Set y-axis range
            plt.xlabel(r"$\zeta$")
            plt.ylabel(r"D $[\sigma^2 \tau^{-1}]$")
            plt.title(r"Diffusion coefficient")
            # legend = plt.legend(title="Rcut Value", loc="best")
            # Custom legend: only two entries
            # custom_handles = [
            #     Line2D([0], [0], color='black', alpha=0.7, linestyle='--', marker='s', label=r"$r_{\text{cut}}=2.6$"),
            #     Line2D([0], [0], color='black', alpha=0.7, linestyle='-',  marker='o', label=r"$r_{\text{cut}}=3.0$"),
            # ]
            # ax.legend(handles=custom_handles, title=r"", loc="best")
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            plt.savefig(f"diff_wc_{wc}_kt_{kt}_ks_{ks}.png", dpi=300,transparent=True)
            plt.close()