import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
# import seaborn as sn
from sklearn.neighbors import BallTree
from scipy.spatial.distance import pdist
import argparse


def count_samples_dump_file(filename):
  """
  Counts the number of samples (timesteps) in a dump file.

  Args:
      filename: The path to the dump file.

  Returns:
      A tuple containing the number of samples and a list of timesteps.
  """
  with open(filename) as fh:
    num_samples = 0
    timesteps = []
    for line in fh:
      if line.strip() == "ITEM: TIMESTEP":
        num_samples += 1
        timesteps.append(int(next(fh).strip()))
  return num_samples, timesteps

def count_atoms_dump_file(filename):
    try:
        fh = open(filename)
    except OSError as e:
        raise OSError(f"Error opening file {filename}: {e}")
    timestring = "ITEM: NUMBER OF ATOMS"
    for line in fh:
        print(line)
        if  line.strip() == timestring:
            return int(fh.readline().strip())
        
def count_atoms_dump_file(filename):
    try:
        fh = open(filename)
    except OSError as e:
        raise OSError(f"Error opening file {filename}: {e}")
    timestring = "ITEM: NUMBER OF ATOMS"
    for line in fh:
        if line.strip() == timestring:
            return int(fh.readline().strip())
    fh.close()
    raise ValueError(f"Could not find '{timestring}' in {filename}")

def read_box(filename):
    """
    Parameters:
    - Single dump filename (no wildcards)

    Returns:
    - Length of the simulation box
    """
    fh = open(filename,'r')
    fh.readline()
    t = int(fh.readline().strip())
    fh.readline()
    N_ATOMS = int(fh.readline().strip())
    fh.readline()
    xlo, xhi = fh.readline().strip().split()
    ylo, yhi = fh.readline().strip().split()
    zlo, zhi = fh.readline().strip().split()

    xlo = float(xlo)
    ylo = float(ylo)
    zlo = float(zlo)
    xhi = float(xhi)
    yhi = float(yhi)
    zhi = float(zhi)

    Lx = xhi - xlo
    Ly = yhi - ylo
    Lz = zhi - zlo
    
    if np.max([Lx-Ly,Ly-Lz]) > 1.0 :
        print(f"System box not cubic, edge diff: {np.max([Lx-Ly,Ly-Lz])}")
    return Lx,Ly,Lz

def process_single_dump_file_images(filename, N_SAMPLES_MAX=100000000,SKIP_SAMPLES = 0, STRIDE = 1):
    N_SAMPLES,_ = count_samples_dump_file(filename)
    N_ATOMS = count_atoms_dump_file(filename)

    N_SAMPLES = min(N_SAMPLES,N_SAMPLES_MAX)
    print(N_ATOMS)
    coords = np.empty((N_SAMPLES, N_ATOMS, 3), dtype=np.float64) # type: ignore
    v = np.empty((N_SAMPLES, N_ATOMS, 3), dtype=np.float64) # type: ignore
    mu = np.empty((N_SAMPLES, N_ATOMS, 3), dtype=np.float64) # type: ignore
    omega = np.empty((N_SAMPLES, N_ATOMS, 3), dtype=np.float64) # type: ignore
    f = np.empty((N_SAMPLES, N_ATOMS, 3), dtype=np.float64) # type: ignore
    torque = np.empty((N_SAMPLES, N_ATOMS, 3), dtype=np.float64) # type: ignore


    t = []
    idx_time = 0

    fh = open(filename)
    # while idx_time < N_SAMPLES:
    for idx_time in tqdm(range(N_SAMPLES)):
        # print(idx_time)
        fh.readline()
        t.append(int(fh.readline().strip()))
        fh.readline()
        fh.readline()
        fh.readline()

        xlo, xhi = fh.readline().strip().split()
        ylo, yhi = fh.readline().strip().split()
        zlo, zhi = fh.readline().strip().split()

        xlo = float(xlo)
        ylo = float(ylo)
        zlo = float(zlo)
        xhi = float(xhi)
        yhi = float(yhi)
        zhi = float(zhi)

        Lbox_x = xhi - xlo
        Lbox_y = yhi - ylo
        Lbox_z = zhi - zlo

        fh.readline()

        for i in range(N_ATOMS):

            s = fh.readline().strip().split()
            # print(s)

            if len(s) != 23 and len(s) != 11 and len(s) !=5:
                print(filename)
                print(s)
                raise ValueError('Unexpected number of columns in the dump file \n the correct columns are: \n id type x y z ix iy iz vx vy vz mux muy muz omegax omegay omegaz fx fy fz tqx tqy tqz')

            if len(s)==11:
                idx = int(s[0])
                x = float(s[2])
                y = float(s[3])
                z = float(s[4])

                ix = float(s[5])
                iy = float(s[6])
                iz = float(s[7])

                mux = float(s[8])
                muy = float(s[9])
                muz = float(s[10])

                vx = 0.0
                vy = 0.0
                vz = 0.0
                fx = 0.0
                fy = 0.0
                fz = 0.0
                omegax = 0.0
                omegay = 0.0
                omegaz = 0.0
                tx = 0.0
                ty = 0.0
                tz = 0.0

            if len(s)==13:
                idx = int(s[0])
                # type = int(s[1])
                # ITEM: ATOMS id type x y z vx vy vz mux muy muz omegax omegay omegaz

                x = float(s[2])
                y = float(s[3])
                z = float(s[4])

                ix = float(s[5])
                iy = float(s[6])
                iz = float(s[7])

                vx = float(s[8])
                vy = float(s[9])
                vz = float(s[10])

                mux = float(s[11])
                muy = float(s[12])
                muz = float(s[13])

                omegax = float(s[14])
                omegay = float(s[15])
                omegaz = float(s[16])

                fx = float(s[17])
                fy = float(s[18])
                fz = float(s[19])

                tx = float(s[20])
                ty = float(s[21])
                tz = float(s[22])

            if len(s)==5:

                idx = int(s[0]) # type = int(s[1])
                x = float(s[1])
                y = float(s[2])
                z = float(s[3])
                p_type = int(s[4])
                vx = 0
                vy = 0
                vz = 0
                omegax= 0
                omegay=0
                omegaz=0
                mux = 0
                muy=0
                muz=0
                fx=0
                fy=0
                fz=0
                tx=0
                ty=0
                tz=0



            coords[idx_time,idx-1, 0] = x
            coords[idx_time,idx-1, 1] = y
            coords[idx_time,idx-1, 2] = z

            # print("unwrapped: ",coords[idx_time,idx-1, 0])

            v[idx_time,idx-1, 0] = vx
            v[idx_time,idx-1, 1] = vy
            v[idx_time,idx-1, 2] = vz

            mu[idx_time,idx-1, 0] = mux
            mu[idx_time,idx-1, 1] = muy
            mu[idx_time,idx-1, 2] = muz

            omega[idx_time,idx-1, 0] = omegax
            omega[idx_time,idx-1, 1] = omegay
            omega[idx_time,idx-1, 2] = omegaz

            f[idx_time,idx-1, 0] = fx
            f[idx_time,idx-1, 1] = fy
            f[idx_time,idx-1, 2] = fz

            torque[idx_time,idx-1, 0] = tx
            torque[idx_time,idx-1, 1] = ty
            torque[idx_time,idx-1, 2] = tz

        idx_time = idx_time + 1

    fh.close()

    t = np.array(t)
    return t[SKIP_SAMPLES::STRIDE], coords[SKIP_SAMPLES::STRIDE], v[SKIP_SAMPLES::STRIDE], mu[SKIP_SAMPLES::STRIDE], omega[SKIP_SAMPLES::STRIDE]

def wrap_coordinates(positions, x_end, y_end, z_end, lx, ly, lz):
    """wrap_coordinates 

    Args:
        positions (_type_): _description_
        x_end (_type_): min value for x of the wrapped box
        y_end (_type_): min value for y of the wrapped box
        z_end (_type_): min value for z of the wrapped box
        lx (_type_): box length x axis
        ly (_type_): box length y axis
        lz (_type_): box length z axis

    Returns:
        _type_: wrapped coordinates
    """
    # Define box limits and lengths
    box_mins = np.array([-x_end, -y_end, -z_end])
    box_lengths = np.array([lx, ly, lz])

    # Shift, wrap with modulo, then shift back
    wrapped = (positions - box_mins) % box_lengths + box_mins
    return wrapped


def calc_interparticle_distances(coords,std_dev=False):
    """
    Calculate average distance between every particle pairs over time.
    Parameters:
    -
    Returns:
    -
    """
    num_frames = coords.shape[0]
    mean_dist = np.zeros((num_frames))
    if std_dev:
        std_dist = np.zeros((num_frames))

    for frame in range(num_frames):
        pair_dist = pdist(coords[frame], metric='euclidean')
        mean_dist[frame] = np.mean(pair_dist)
        if std_dev:
            std_dist[frame] = np.std(pair_dist)

    if std_dev:
        return mean_dist, std_dist
    else:
        return mean_dist

def calc_dist_neighbours(coords,n_neighbours,Lbox,MEAN_OVER_FRAMES=False):
    """calc_dist_neighbours In principle I need to evaluate the minimum distance considering the presence of the PBCs. look at POLY routine.

    1. Calculate for every particle its distance with its first n_neighbours neighbours.
    2. Average the distance over the neighbours getting a N_ATOMS averaged neighbour distance
    3. Average this last quantity over all the particles and taking the std deviations over all this particle

    Args:
        coords (_type_): _description_
        n_neighbours (_type_): _description_
        MEAN_OVER_FRAMES (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    num_frames = coords.shape[0]
    dist_over_neighbours = np.zeros((num_frames,coords.shape[1]))
    std_over_particles = np.zeros((num_frames))



    for frame in range(num_frames):

        tree = cKDTree(coords[frame],boxsize=Lbox) # check if it works
        dist_neighbours, indexes = tree.query(coords[frame], k=n_neighbours)
        # print(dist_neighbours.shape)

        dist_over_neighbours[frame] = np.mean(dist_neighbours,axis=1) # average over neighbours

        # print(dist_over_neighbours[frame].shape)
        # std_over_particles[frame]= np.std(dist_over_neighbours[frame],axis=1) # std dev of neighbouring distance

    # time evolution of mean interparticle distance
    dist_over_all_particles = np.mean(dist_over_neighbours,axis=1) # average over all particles
    # print(dist_over_all_particles.shape) # 1D Array num of frames long

    std_over_particles = np.std(dist_over_neighbours,axis=1)

    # print("std: ",std_over_particles.shape)
    # print("std: ",std_over_particles[0])

    # print(dist_mean_for_point.shape)
    if MEAN_OVER_FRAMES:
        dist_over_frames = np.mean(dist_over_all_particles,axis=0)
        std = np.mean(std_over_particles,axis=0)
        return dist_over_frames, std # you get one values for d and his std deviation
    else:
        return dist_over_all_particles, std_over_particles



def gyration_radius(coords):
    """
    Computes the radius of gyration for each frame in a trajectory.

    Parameters:
    - coords: np.ndarray of shape (n_frames, n_atoms, 3)

    Returns:
    - radii: np.ndarray of shape (n_frames,), radius of gyration per frame
    """
    # Compute center of mass for each frame: shape (n_frames, 1, 3)
    cm = np.mean(coords, axis=1, keepdims=True)

    # Compute displacement from CM: shape (n_frames, n_atoms, 3)
    diff = coords - cm

    # Compute squared distances and average over atoms: shape (n_frames,)
    diff_squared = np.sum(diff**2, axis=2)  # shape: (n_frames, n_atoms)
    mean_squared = np.mean(diff_squared, axis=1)

    # Return square root to get radius of gyration
    return np.sqrt(mean_squared)


def gyration_tensor(coords):
    # coords here are cordinate of a single frame
    cm = np.sum(coords, axis=0) / coords.shape[0]
    cm = cm[np.newaxis, :]
    # print(cm.shape)
    diff = coords - cm
    # print(diff.shape)
    T = np.zeros((3,3))
    for i in [0,1,2]:
        for j in [0,1,2]:
            T[i,j] = (np.sum(diff[:,i] * diff[:,j],axis=0)) / coords.shape[0]

    # print(T.shape)
    return T

def gyration_tensor_2(coords):
    """
    Computes the gyration tensor for each frame in a trajectory.

    Parameters:
    - coords: np.ndarray of shape (n_frames, n_atoms, 3)

    Returns:
    - T_all: np.ndarray of shape (n_frames, 3, 3), gyration tensor per frame
    """
    # Center each frame
    cm = np.mean(coords, axis=1, keepdims=True)  # shape: (n_frames, 1, 3)
    diff = coords - cm  # shape: (n_frames, n_atoms, 3)

    # Compute tensor using einsum over batch (frames)
    T_all = np.einsum('fni,fnj->fij', diff, diff) / coords.shape[1]

    return T_all



def calc_asphericity(gyration_tensor):
    eig, _ = np.linalg.eigh(gyration_tensor)
    b = eig[0] - 0.5 * (eig[1] + eig[2])
    return b

import numpy as np
from scipy.spatial import cKDTree
from multiprocessing import Pool, cpu_count


class UnionFind:
    def __init__(self, n):
        self.parent = np.arange(n)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr != yr:
            self.parent[yr] = xr

    def get_components(self):
        groups = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            groups.setdefault(root, []).append(i)
        return list(groups.values())


def process_snapshot(args):
    """
    Process one snapshot: find clusters using KD-tree and Union-Find.
    """
    t_idx, positions, min_dist, min_size, box_size = args
    num_particles = positions.shape[0]
    corr_positions = np.zeros_like(positions)
    # print(positions[0])

    # if box_size is not None:
    #     corr_positions[:,0] = positions[:,0] + 0.5*box_size[0]
    #     corr_positions[:,1] = positions[:,1] + 0.5*box_size[1]
    #     corr_positions[:,2] = positions[:,2] + 0.5*box_size[2]

        # # corr_positions = positions + 0.5 * box_size

        # print(np.count_nonzero(corr_positions>20.0))
        # print(np.count_nonzero(corr_positions<0.0))


    # Handle periodic boundaries if box_size is given
    tree = cKDTree(corr_positions, boxsize=box_size if box_size is not None else None)

    # Get all pairs within min_dist
    pairs = tree.query_pairs(min_dist)

    # Union-Find to group pairs
    uf = UnionFind(num_particles)
    for i, j in pairs:
        uf.union(i, j)

    clusters = [comp for comp in uf.get_components() if len(comp) >= min_size]
    if clusters:
        return (t_idx, clusters)
    return None

from scipy.spatial.distance import pdist, squareform

def calculate_radius_of_gyration(cluster_positions, box_dims):
    """Calculates the radius of gyration for a single cluster, handling PBCs."""
    # Step 1: Unwrap coordinates to handle PBCs for center of mass calculation
    # We choose the first particle as a reference and shift others relative to it.
    ref_pos = cluster_positions[0]
    deltas = cluster_positions - ref_pos
    deltas -= box_dims * np.round(deltas / box_dims)
    unwrapped_positions = ref_pos + deltas

    # Step 2: Calculate the center of mass
    center_of_mass = np.mean(unwrapped_positions, axis=0)

    # Step 3: Calculate squared distances from the center of mass
    squared_distances = np.sum((unwrapped_positions - center_of_mass)**2, axis=1)

    # Step 4: Compute the radius of gyration
    rg = np.sqrt(np.mean(squared_distances))
    return rg

def find_clusters(
    positions,
    box_size,
    min_distance,
    min_cluster_size=2
):
    """
    Identifies clusters of particles and calculates their properties.

    This function analyzes particle positions over time to find clusters based on
    a minimum distance criterion, applying the Minimum Image Convention for
    periodic boundary conditions. It also calculates the radius of gyration
    for each cluster.

    Args:
        positions (np.ndarray): A 3D NumPy array of shape (n_frames, n_particles, 3).
        box_size (float or np.ndarray): The size of the simulation box.
        min_distance (float): The maximum distance between two particles.
        min_cluster_size (int, optional): The minimum number of particles per cluster.

    Returns:
        dict: A dictionary where keys are frame indices. Values are another
              dictionary containing 'clusters' (a dict of cluster IDs to particle lists)
              and 'properties' (a dict of cluster IDs to their calculated properties like Rg).

    Raises:
        ValueError: If no clusters are found in any frame.
    """
    if not isinstance(positions, np.ndarray) or positions.ndim != 3 or positions.shape[2] != 3:
        raise ValueError("Input 'positions' must be a NumPy array with shape (n_frames, n_particles, 3).")

    all_frames_data = {}
    box_dims = np.array(box_size) if isinstance(box_size, (list, tuple)) else np.full(3, box_size)

    for frame_idx in range(positions.shape[0]):
        frame_positions = positions[frame_idx]

        # Calculate pairwise distances with Minimum Image Convention
        deltas = frame_positions[:, np.newaxis, :] - frame_positions[np.newaxis, :, :]
        deltas -= box_dims * np.round(deltas / box_dims)
        dist_matrix = np.sqrt(np.sum(deltas**2, axis=-1))

        adjacency_matrix = dist_matrix < min_distance

        n_particles = frame_positions.shape[0]
        visited = np.zeros(n_particles, dtype=bool)
        frame_clusters = {}
        cluster_properties = {}
        cluster_id = 0

        for i in range(n_particles):
            if not visited[i]:
                cluster_particles = []
                q = [i]
                visited[i] = True

                head = 0
                while head < len(q):
                    u = q[head]
                    head += 1
                    cluster_particles.append(u)

                    neighbors = np.where(adjacency_matrix[u])[0]
                    for v in neighbors:
                        if not visited[v]:
                            visited[v] = True
                            q.append(v)

                if len(cluster_particles) >= min_cluster_size:
                    frame_clusters[cluster_id] = cluster_particles

                    # Calculate properties for this cluster
                    cluster_pos = frame_positions[cluster_particles]
                    rg = calculate_radius_of_gyration(cluster_pos, box_dims)
                    cluster_properties[cluster_id] = {
                        'size': len(cluster_particles),
                        'radius_of_gyration': rg
                    }
                    cluster_id += 1

        if frame_clusters:
            all_frames_data[frame_idx] = {
                'clusters': frame_clusters,
                'properties': cluster_properties
            }

    if not all_frames_data:
        raise ValueError("No clusters found with the given criteria.")

    return all_frames_data

def visualize_frame_clusters(frame_positions, frame_data, box_size, frame_idx):
    """Generates a 2D visualization of clusters for a specific frame."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 10))

    n_particles = frame_positions.shape[0]
    # FIX: Initialize the colors array to hold RGBA values.
    # Gray is represented by [0.5, 0.5, 0.5] with an alpha of 0.8.
    colors = np.full((n_particles, 4), [0.5, 0.5, 0.5, 0.8])
    print(colors.shape)
    clusters = frame_data.get('clusters', {})
    cmap = plt.get_cmap('plasma')
    cluster_colors = cmap(np.linspace(0, 1, len(clusters)))

    for i, (cid, particles) in enumerate(clusters.items()):
        colors[particles] = cluster_colors[i]

    # Plot particles (projected onto XY plane)
    ax.scatter(frame_positions[:, 0], frame_positions[:, 1], c=colors, s=15, alpha=0.8)

    ax.set_title(f'Cluster Visualization for Frame {frame_idx}', fontsize=16)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    ax.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Custom plot styles (as hex colors from your gnuplot lines)
PLOT_STYLES = {
    "ls1": {'color': '#00008B', 'linewidth': 3},
    "ls2": {'color': '#2B5FA8', 'linewidth': 3},
    "ls3": {'color': '#568FC6', 'linewidth': 3},
    "ls4": {'color': '#82BFE3', 'linewidth': 3},
    "ls5": {'color': '#ADD8E6', 'linewidth': 3},
    "diffusion": {'color': 'black', 'linestyle': '--', 'linewidth': 2}
}


def plot_msd(msd_file='msd.dat', output_file='msd.png'):
    """Plot Mean Squared Displacement (MSD) with logscale."""
    
    try:
        data = np.loadtxt(msd_file)
        time = data[:, 0]
        x = data[:, 1]
        y = data[:, 2]
        z = data[:, 3]
        msd2 = data[:,4]
        
        plt.figure(figsize=(19.2, 10.8))
        plt.xscale('log')
        plt.yscale('log')
        
        # plt.xlim()
        plt.ylim(1,100000)
        plt.plot(time, msd2, marker='o', label='msd',**PLOT_STYLES["ls4"])
        plt.plot(time, time, label='Diffusion',**PLOT_STYLES["diffusion"])
        
        plt.xlabel("Time")
        plt.ylabel("MSD")
        plt.legend(loc='lower right')
        plt.grid(True, which='both', ls='--', lw=0.5)
        plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
    
    except:
        print(f"MSD file corrupted: {msd_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze interparticle distances from a LAMMPS dump file.")
    parser.add_argument("dump_file", help="Path to the LAMMPS dump file")
    args = parser.parse_args()


    t, coords, v, mu, omega = process_single_dump_file_images(
        args.dump_file,
    )
    Lx,Ly,Lz = read_box(args.dump_file)
    coords = wrap_coordinates(coords, 0.0, 0.0, 0.0, Lx,Ly,Lz)


    mean_dist, std_dist = calc_interparticle_distances(coords, std_dev=True)
    neighbour_dist, neighbour_std = calc_dist_neighbours(coords, 6)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t, mean_dist, label="Mean Interparticle Distance")
    plt.fill_between(t, mean_dist-std_dist, mean_dist+std_dist, alpha=0.2)
    plt.xlabel("Timestep")
    plt.ylabel("Distance")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(t, neighbour_dist, label=f"Mean {6}-Neighbour Distance")
    plt.fill_between(t, neighbour_dist-neighbour_std, neighbour_dist+neighbour_std, alpha=0.2)
    plt.xlabel("Timestep")
    plt.ylabel("Neighbour Distance")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.dump_file+"_distance_plot.png",dpi=200)
    plt.show()


    min_cluster_size = 2
    all_data = find_clusters(
            positions=coords,
            box_size=Lx,
            min_distance=1.0,
            min_cluster_size=min_cluster_size
        )
    ## data is a dict of dicts of dicts
    ## data = {frame1:{
        #               cluster_id:[2,3,5...],
        #               }, 
        #               properties:{}
        #               }
        #      }
    last_frame_with_clusters = -1
    for frame, data in all_data.items():
        print(f"\n--- Frame {frame} ---")
        clusters = data['clusters']
        properties = data['properties']

        # --- Print Cluster Properties ---
        for cid, particles in clusters.items():
            props = properties[cid]
            print(f"  Cluster {cid}: Size={props['size']}, Rg={props['radius_of_gyration']:.3f}")

        # --- Analyze and Print Size Distribution ---
        sizes = [p['size'] for p in properties.values()]
        if sizes:
            hist, edges = np.histogram(sizes, bins=np.arange(min_cluster_size, max(sizes) + 2))
            print("\n  Cluster Size Distribution:")
            for i in range(len(hist)):
                if hist[i] > 0:
                    print(f"    Size {int(edges[i])}: {hist[i]} cluster(s)")
        last_frame_with_clusters = frame

    # --- Visualize the last frame that contained clusters ---
    if last_frame_with_clusters != -1:
        print(f"\nVisualizing clusters for Frame {last_frame_with_clusters}...")
        visualize_frame_clusters(
            coords[last_frame_with_clusters],
            all_data[last_frame_with_clusters],
            Lx,
            last_frame_with_clusters
        )


    plt.hist(sizes, bins=np.arange(min_cluster_size, max(sizes) + 2,10))
    plt.show()



if __name__ == "__main__":
    main()

