import pandas as pd
import matplotlib.pyplot as plt
# from Analysis.spherical_analysis import MSDfit
from utilities import *
import socket
from scipy.optimize import curve_fit
from tqdm import tqdm
import numpy as np
import argparse
import multiprocessing
from sklearn.metrics import r2_score


def diffusion(t,D):
    return D*t # 4 because of 2D diffusion

def diffusion_generic(t,D,alpha):
    return D*t**alpha # 4 because of 2D diffusion

def constant(x, c):
    return c * np.ones_like(x)

def build_path(row):
    return f"N_{int(row['N'])}_kt_{(row['kt'])}_ks_{(row['ks'])}_rcut_{row['rcut']}_wc_{row['wc']}_T_{row['T']}"

# hostname = socket.gethostname()
# if hostname == "mi-notebook":
#     base_dir = "/home/pietro/Desktop/new_potential_timon/planar/sistematic/"
# elif hostname.startswith("md"):
#     base_dir = "/martini/pietro/new_potential/planar/"


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, default='sistematic_k/data/', help='Relative path to data directory')

parser.add_argument('--base_dir', type=str, default="/martini/pietro/new_potential/planar/", help='Parent directory')


args = parser.parse_args()
data_dir = args.data_dir
base_dir = args.base_dir

BILAYER = True
MSD = True
MSDfit_v2 = True
CLUSTER = False
DISTANCE = False

SEQUENTIAL = True
SINGLE=False
 

def process_row(args):
    index, row = args
    dict_df = {}
    # Distance
    if DISTANCE:
        
        # if 'mean_dist' not in df.columns:
        #     df['mean_dist'] = np.nan
        # if 'mean_std' not in df.columns:
        #     df['mean_std'] = np.nan

        # # distance neighbours
        # if 'mean_dist_n' not in df.columns:
        #     df['mean_dist_n'] = np.nan
        # if 'mean_std_n' not in df.columns:
        #     df['mean_std_n'] = np.nan


        coords_file = base_dir + data_dir + row['path'] + "/position.lammpstrj"
        t, coords, v, mu, omega = process_single_dump_file_images(coords_file,STRIDE=1)
        Lx,Ly,Lz = read_box(coords_file)
        coords = wrap_coordinates(coords, 0.0, 0.0, 0.0, Lx,Ly,Lz)

        mean_dist, std_dist = calc_interparticle_distances(coords, std_dev=True)
        mean_dist_ave = np.mean(mean_dist) # average over time
        std_dist_ave = np.mean(std_dist)   # average over time

        neighbour_dist, neighbour_std = calc_dist_neighbours(coords, 6,[Lx,Ly,Lz])
        
        mask_min_time = 15000
        mask = t > mask_min_time
        
        
        neighbour_dist_ave = np.mean(neighbour_dist[mask]) # average over time
        neighbour_std_ave  = np.mean(neighbour_std[mask]) # std over time

        # df.at[index, 'mean_dist'] = mean_dist_ave
        # df.at[index, 'mean_std'] = std_dist_ave

        # df.at[index, 'mean_dist_n'] = neighbour_dist_ave
        # df.at[index, 'mean_std_n'] = std_dist_ave
        
        dict_df['mean_dist'] = mean_dist_ave
        dict_df['mean_std'] = std_dist_ave
        dict_df['mean_dist_n'] = neighbour_dist_ave
        dict_df['mean_std_n'] = neighbour_std_ave



        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(t, mean_dist, label="Mean Interparticle Distance")
        plt.fill_between(t, mean_dist-std_dist, mean_dist+std_dist, alpha=0.2)
        # plt.ylim(0,25)
        plt.xlim(0,50000)
        plt.xlabel("Timestep")
        plt.ylabel("Distance")
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(t, neighbour_dist, label=f"Mean {6}-Neighbour Distance")
        plt.fill_between(t, neighbour_dist-neighbour_std, neighbour_dist+neighbour_std, alpha=0.2)
        plt.ylim(0,1.8)
        plt.xlim(0,50000)
        plt.xlabel("Timestep")
        plt.ylabel("Neighbour Distance")
        plt.legend()
        plt.tight_layout()
        plt.savefig(base_dir + data_dir + f"plot/dist_{row['path']}.png",dpi=200)
        plt.close()
        # plt.show()
        
        # # Save distance data to CSV
        # distance_data = pd.DataFrame({
        # "timestep": t,
        # "mean_interparticle_distance": mean_dist,
        # "std_interparticle_distance": std_dist,
        # "mean_neighbour_distance": neighbour_dist,
        # "std_neighbour_distance": neighbour_std
        # })
        # distance_csv_path = base_dir + data_dir + f"/csv/dist_{row['path']}.csv"
        # distance_data.to_csv(distance_csv_path, index=False)
     

    # Cluster


    if CLUSTER:
        if 'coords' not in locals():
            coords_file = base_dir + data_dir + row['path'] + "/position.lammpstrj"
            t, coords, v, mu, omega = process_single_dump_file_images(coords_file,STRIDE=1)
            Lx,Ly,Lz = read_box(coords_file)
            coords = wrap_coordinates(coords, 0.0, 0.0, 0.0, Lx,Ly,Lz)
        
        min_cluster_size = 1
        all_data = find_clusters(
                positions=coords,
                box_size=Lx,
                min_distance=1.0,
                min_cluster_size=min_cluster_size
            )

        size_mean = []
        size_std  = []
        rgyr_mean = []
        rgyr_std  = []
        last_frame_with_clusters = -1
        for frame, frame_data in all_data.items():
            size = []
            rgyr = []
            clusters = frame_data['clusters']
            properties = frame_data['properties']
            for cid, particles in clusters.items():
                props = properties[cid]
                size.append(props['size'])
                rgyr.append(props['radius_of_gyration'])


            size_mean.append(np.mean(size))
            size_std.append(np.std(size))
            rgyr_mean.append(np.mean(rgyr))
            rgyr_std.append(np.std(rgyr))


        size_mean = np.array(size_mean)
        size_std = np.array(size_std)
        rgyr_mean = np.array(rgyr_mean)
        rgyr_std = np.array(rgyr_std)

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(t, size_mean,"-",label="Mean size")
        plt.fill_between(t, size_mean-size_std, size_mean+size_std, alpha=0.2)
        plt.ylim(0,1000)
        plt.xlim(0,500000)
        plt.xlabel("Frame")
        plt.ylabel("Clusters size")
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(t, rgyr_mean ,"-",label="Mean Rg")
        plt.fill_between(t, rgyr_mean-rgyr_std, rgyr_mean+rgyr_std, alpha=0.2)
        plt.ylim(0,10)
        plt.xlim(0,500000)
        plt.xlabel("Frame")
        plt.ylabel("Cluster gyration radius")
        plt.legend()
        plt.tight_layout()
        plt.savefig(base_dir + data_dir + f"/plot/cluster_{row['path']}.png",dpi=200)
        # plt.show()
        plt.close()
        
        # Save distance data to CSV
        distance_data = pd.DataFrame({
        "timestep": t,
        "mean_size": size_mean,
        "std_size": size_std,
        "mean_gyr_radius": rgyr_mean,
        "std_gyr_radius": rgyr_std
        })
        
        distance_csv_path = base_dir + data_dir + f"/csv/dist_{row['path']}.csv"
        distance_data.to_csv(distance_csv_path, index=False)



    # MSD plotting

    if MSD:
        # Add columns 'D' and 'D_2d' to the DataFrame if they don't exist
        # if 'D' not in df.columns:
        #     df['D'] = np.nan
        # if 'D_2d' not in df.columns:
        #     df['D_2d'] = np.nan
    
        msd_file = base_dir + data_dir + row['path'] + "/" + "msd.dat"
        msd_png = base_dir + data_dir + f"plot/msd_{row['path']}.png"
        plot_msd(msd_file,msd_png)
        
    mask_min_time = 40000
    if MSDfit_v2:

        def fit_model(model, x, y, p0=None, maxfev=5000):
            """Try to fit a model, return params, covariance, R² score."""
            try:
                popt, pcov = curve_fit(model, x, y, p0=p0, maxfev=maxfev)
                y_pred = model(x, *popt)
                r2 = r2_score(y, y_pred)
                return popt, pcov, r2
            except Exception as e:
                print(f"Fit failed for {model.__name__}: {e}")
                return None, None, None
        # dict_df = {}

        try:
            # --- Load data ---
            msd_data = np.loadtxt(msd_file)
            time = msd_data[:, 0]
            x, y, z = msd_data[:, 1:4].T
            msd2, msd2d = msd_data[:, 4], x + y

            # --- Apply mask for 2D fit ---
            mask = time > mask_min_time
            t_masked, msd2d_masked = time[mask], msd2d[mask]

            # --- 2D linear fit ---
            popt2d, _, r2_2d = fit_model(diffusion, t_masked, msd2d_masked)
            if popt2d is not None:
                dict_df['D_2d'] = popt2d[0]
                dict_df['exp_diff'] = 1.0
                dict_df['r2_2d'] = r2_2d

            # --- Generic fit ---
            popt_gen, _, r2_gen = fit_model(diffusion_generic, t_masked, msd2d_masked)
            if popt_gen is not None:
                dict_df['D_generic'] = popt_gen[0]
                dict_df['alpha'] = popt_gen[1]
                dict_df['r2_generic'] = r2_gen
            else:
                # fallback constant
                popt_c, _, _ = fit_model(constant, t_masked, msd2d_masked)
                if popt_c is not None:
                    dict_df['alpha'] = 0.0
                    dict_df['const'] = popt_c[0]

            # --- Plot ---
            plt.figure(figsize=(19.2, 10.8))
            plt.xscale('log')
            plt.yscale('log')
            # plt.xlim(500, 50000)
            # plt.ylim(1, 100000)

            # raw data
            plt.plot(time, msd2d, 'o', label='MSD 2D')

            # fitted curves
            # if popt3d is not None:
            #     plt.plot(time, diffusion(time, *popt3d),
            #             label=f"3D fit: D={popt3d[0]:.3g}, R²={r2_3d:.3f}")
            
            if popt2d is not None:
                plt.plot(t_masked, diffusion(t_masked, *popt2d),
                        label=f"2D fit: D={popt2d[0]:.3g}, R²={r2_2d:.3f}")
            if popt_gen is not None:
                plt.plot(t_masked, diffusion_generic(t_masked, *popt_gen), '--',
                        label=f"2D Generic fit: D={popt_gen[0]:.3g}, α={popt_gen[1]:.2f}, R²={r2_gen:.3f}")

            plt.xlabel("Time")
            plt.ylabel("MSD")
            plt.legend(loc='lower right')
            plt.grid(True, which='both', ls='--', lw=0.5)
            plt.savefig(msd_png, dpi=200, bbox_inches='tight', facecolor='white')
            plt.close()

        except Exception as e:
            print(f"MSD processing failed: {e}")
    
    
    # check last frame of the trajectory if it has many clusters label the simulation as unstable or not bilayer
    if BILAYER:
        if 'bilayer' not in df.columns:
            df['bilayer'] = np.nan

        coords_file = base_dir + data_dir + row['path'] + "/position.lammpstrj"
        n_frames, _ = count_samples_dump_file(coords_file)
        if n_frames > 10:
            t, coords, v, mu, omega = process_single_dump_file_images(coords_file,STRIDE=1,SKIP_SAMPLES=n_frames-1)
            Lx,Ly,Lz = read_box(coords_file)
            coords = wrap_coordinates(coords, 0.0, 0.0, 0.0, Lx,Ly,Lz)
            
            N_ATOMS = coords.shape[1]
            
            min_cluster_size = 1
            last_frame_data = find_clusters(
                    positions=coords,
                    box_size=Lx,
                    min_distance=1.0,
                    min_cluster_size=min_cluster_size
                )
            
            last_frame_idx = next(iter(last_frame_data))
        
            data_idx = last_frame_data[last_frame_idx]
            
            clusters = data_idx['clusters']
            properties = data_idx['properties']

            n_clusters = len(clusters.keys())
            # print(f"N clusters: {n_clusters}")
                        
            size = [properties[cid]['size'] for cid in clusters.keys()]
            size.sort()
            mean_size = np.mean(size[-10:])
            max_size  = np.max(size)
            dict_df['max_size'] = max_size
            dict_df['mean_size'] = mean_size
            dict_df['n_clusters'] = n_clusters
            
            
            if (max_size < 0.8*N_ATOMS) or (n_clusters > 0.05*N_ATOMS):
                # df.at[index, 'bilayer'] = 0
                dict_df['bilayer'] = 0
                # print("Unstable")
            else:
                # df.at[index, 'bilayer']  = 1
                dict_df['bilayer'] = 1
                # print("Stable")
        else:
            print(f"Too few frames: {n_frames}")
            # df.at[index, 'bilayer'] = 0
            dict_df['bilayer'] = 0
        
        dict_df['processed'] = 1

        
    return index,dict_df


# Load data
output_file = "simulation_summary.csv"
df = pd.read_csv(base_dir+data_dir+output_file)

# analysis of a single simulation

if SINGLE:
    # Example: extract index and row for specific parameters
    params = {
        'N': 2500,
        'kt': .0,
        'ks': 10.0,
        'rcut': 2.0,
        'wc': 2.0,
        'T': 1.0
    }


    row_match = df[
        (df['wc'] == params['wc']) &
        (df['rcut'] == params['rcut']) &
        (df['N'] == params['N']) &
        (df['kt'] == params['kt']) &
        (df['ks'] == params['ks']) &
        (df['T'] == params['T'])
    ]

    if not row_match.empty:
        index = row_match.index[0]
        row = row_match.iloc[0]
    else:
        raise ValueError("No matching row found for the given parameters.")
    index, data = process_row((index,row))
    
    for key in data.keys():
        df.at[index,key] = data[key]
        
    df.to_csv(base_dir + data_dir + output_file, index=False)


# analysis of the full CSV
if SEQUENTIAL:
    # for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing simulations"):
    #     df = process_row((index,row))
    #     df.to_csv(base_dir + data_dir + output_file, index=False)
    if 'processed' in df.columns:
        df = df[df['processed']!=1] # filter for what has not been preprocessed yet
    
    row_args = [(index, row) for index, row in df.iterrows()]

    n_jobs = multiprocessing.cpu_count()
    n_jobs = 16

    with multiprocessing.Pool(processes=n_jobs) as pool:
        results = list(tqdm(pool.imap(process_row, row_args),  
        ncols=50,
        dynamic_ncols=False,
        desc="Processing simulations",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"))

    for index, data in results:
        for key in data.keys():
            df.at[index,key] = data[key]

    df.to_csv(base_dir + data_dir + output_file, index=False)
