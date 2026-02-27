import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re

# 1. Configuration
# Threshold for R-squared
R2_THRESHOLD = 0.9
# Regex pattern to capture parameters from folder names
pattern = r"N_(?P<N>[\d.]+)_d_(?P<d>[\d.]+)_kt_(?P<kt>[\d.]+)_ks_(?P<ks>[\d.]+)_rcut_(?P<rcut>[\d.]+)_wc_(?P<wc>[\d.]+)_T_(?P<T>[\d.]+)_zeta_(?P<zeta>[\d.]+)"

results = []
base_dir = Path(".") 

# 2. Crawl directories and extract data
print(f"Scanning directories for fits with r2 > {R2_THRESHOLD}...")

for folder in base_dir.iterdir():
    if folder.is_dir():
        match = re.search(pattern, folder.name)
        if match:
            # Extract parameters and convert to float
            params = {k: float(v) for k, v in match.groupdict().items()}
            
            file_path = folder / "fit_report.dat"
            if file_path.exists():
                try:
                    # Read the fit report (handling space separation)
                    df_fit = pd.read_csv(file_path, sep='\s+', names=['modes','qmin','qmax','k','kerr','Q','r2'],skiprows=1)
                    
                    if not df_fit.empty:
                        # Find best fit row
                        best_idx = df_fit['Q'].idxmax()
                        best_r2 = float(df_fit.loc[best_idx, 'r2'])
                        
                        # 3. Apply R2 Threshold Filter
                        if best_r2 >= R2_THRESHOLD:
                            params['best_k'] = float(df_fit.loc[best_idx, 'k'])
                            params['best_r2'] = best_r2
                            params['k_err'] = float(df_fit.loc[best_idx,'kerr'])
                            params['best_Q'] = float(df_fit.loc[best_idx, 'Q'])
                            results.append(params)
                        else:
                            print(f"Skipping {folder.name}: r2 ({best_r2:.4f}) below threshold.")
                            
                except Exception as e:
                    print(f"Error processing {folder.name}: {e}")

# 4. Save to CSV
if results:
    df = pd.DataFrame(results)
    df.to_csv("simulation_summary_filtered.csv", index=False)
    print(f"\nSuccess! Found {len(df)} valid simulations.")
    print("Summary saved to 'simulation_summary_filtered.csv'")
else:
    print("No data found matching the criteria.")
    exit()



for N in [400,2500]:
    # Create a line plot with markers
    df_filt = df[df['N']==N]
    sns.lineplot(
        data=df_filt.sort_values('wc'), 
        x='wc', 
        y='best_k', 
        hue='kt', 
        style='ks',
        markers=True, 
        markersize=10,
        palette="viridis"
    )

    plt.title(r'$\kappa$'fr' N={N} (Threshold: $r^2$ > {R2_THRESHOLD})')
    plt.xlabel('wc (Cutoff Distance)')
    plt.ylabel('Best k (Stiffness)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save high-res plot
    filename = f"plot_k_vs_wc_N_{N}.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"High-res plot saved: {filename}")
    # plt.show()
    plt.close()







# # 5. Plotting
# def create_plots(df):
#     sns.set_theme(style="whitegrid", context="talk")
    
#     # We differentiate by 'kt' (ktilt) and 'zeta'
#     for comp in ['kt', 'N', 'ks']:
#         if comp in df.columns and df[comp].nunique() > 1:
#             plt.figure(figsize=(12, 8))
            
#             # Create a line plot with markers
#             sns.lineplot(
#                 data=df.sort_values('wc'), 
#                 x='wc', 
#                 y='best_k', 
#                 hue=comp, 
#                 style=comp,
#                 markers=False, 
#                 markersize=10,
#                 palette='viridis'
#             )
            
#             plt.title(f'Optimal k vs wc (Threshold: r2 > {R2_THRESHOLD})')
#             plt.xlabel('wc (Cutoff Distance)')
#             plt.ylabel('Best k (Stiffness)')
#             plt.legend(title=comp, bbox_to_anchor=(1.05, 1), loc='upper left')
            
#             # Save high-res plot
#             filename = f"plot_k_vs_wc_by_{comp}.png"
#             plt.tight_layout()
#             plt.savefig(filename, dpi=300)
#             print(f"High-res plot saved: {filename}")
#             # plt.show()
#             plt.close()

# create_plots(df_final)

# 4. Grid Plotting
# sns.set_theme(style="whitegrid")

# # Create the facet grid
# # x=wc, y=best_k, row=kt, col=ks, hue=zeta
# g = sns.relplot(
#     data=df_final,
#     x="wc", 
#     y="best_k",
#     hue="N",
#     row="kt", 
#     col="ks",
#     kind="line", 
#     marker="o",
#     palette = ['#56B4E9', '#E69F00', '#009E73'],
#     height=4, 
#     aspect=1.2,
#     facet_kws={'sharey': True, 'sharex': True}
# )

# # Adjust titles and labels
# g.set_axis_labels("wc (Cutoff)", r"$\kappa$")
# g.set_titles(row_template="kt: {row_name}", col_template="ks: {col_name}")
# g.tight_layout()

# # 5. Save high-res output
# output_filename = "grid_plot_k_vs_wc.png"
# g.savefig(output_filename, dpi=500)
# print(f"High-resolution grid plot saved as {output_filename}")
# plt.close()



# plt.figure(figsize=(12, 8))

