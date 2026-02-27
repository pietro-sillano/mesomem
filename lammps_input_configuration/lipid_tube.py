import os,sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

DESCRIPTION = """
This script initializes a squared hexagonal grid configuration for LAMMPS simulations.
Available arguments:

--path  path of the output files
--N     Number of particles for square edge
--d     Distance between particles
--PBC   if insert PBC system is generated
--plot  to plot the lattice
--h     print this help message

Example of script with arguments

python lipid_tube.py --path . --R 8.0 --d 0.80 --plot
"""

def parse_arguments():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(usage=DESCRIPTION,description=DESCRIPTION)

    parser.add_argument("--path", type=str, help="Path to save the configuration files",required=True)

    parser.add_argument("--R", type=float, help="radius of the tube",default=10.0)
    parser.add_argument("--d", type=float, help="Distance between particles",default=0.80)

    parser.add_argument("--plot", action="store_true", help="Generate a plot of the configuration",default=False)

    return parser.parse_args()

def write_positions(outfile,x,y,z,mux,muy,muz,Lbox_x,Lbox_y,Lbox_z):

    # Define LAMMPS atom data file content

    # atom-ID atom-type x y z diameter density q mux muy muz molecule-ID

    # density = 1.0 / (4.0/3.0*np.pi)
    density = 1.0
    diameter = 1.0
    mol_id = 1
    q = 1.0 # charge
    type = 1


    lammps_data = f"""

    {len(x)} atoms

    1 atom types

    {-Lbox_x/2.0:.6f} {Lbox_x/2.0:.6f} xlo xhi
    {-Lbox_y/2.0:.6f} {Lbox_y/2.0:.6f} ylo yhi
    0.0 {Lbox_z:.6f} zlo zhi


    Atoms \n
    """
    # atom-ID atom-type x y z diameter density q mux muy muz molecule-ID

    # Append atom positions to the LAMMPS data
    idx = 1
    for i in range(x.shape[0]):
        lammps_data += f"{idx:d} {type:d} {x[i]:.6f} {y[i]:.6f} {z[i]:.6f} {diameter} {density} {q} {mux[i]:.6f} {muy[i]:.6f} {muz[i]:.6f} {int(mol_id):d} \n"
        idx = idx + 1

    # Write the LAMMPS data to a file
    with open(outfile, "w") as file:
        file.write(lammps_data)

    print(f"LAMMPS data file {outfile} has been generated.")


def create_dir(path):
    base_name = os.path.basename(path)
    parent_dir = os.path.dirname(path)

    # If the directory exists, rename it with a GROMACS-style suffix
    if os.path.exists(path):
        suffix_num = 0
        new_name = f"#{base_name}#"

        # Check for existing folders with the pattern and increment as needed
        while os.path.exists(os.path.join(parent_dir, new_name)):
            suffix_num += 1
            new_name = f"#{base_name}.{suffix_num}#"

        renamed_path = os.path.join(parent_dir, new_name)
        os.rename(path, renamed_path)
        print(f"Existing folder renamed to: {renamed_path}")

    # Create the new directory
    os.makedirs(path)
    print(f"New directory created: {path}")

    return path

def cylinder_mesh(radius, height, spacing):
    """
    Generate an open-ended cylinder triangular mesh.
    
    Parameters
    ----------
    radius : float
        Radius of the cylinder.
    height : float
        Height of the cylinder.
    spacing : float
        Approximate distance between mesh vertices.
    
    Returns
    -------
    vertices : np.ndarray
        Array of shape (N, 3) containing vertex coordinates.
    faces : np.ndarray
        Array of shape (M, 3) containing triangular face indices.
    """
    # Number of divisions along circumference and height
    n_theta = max(3, int(2 * np.pi * radius / spacing))
    n_z = max(2, int(height / spacing))
    
    # Create grid
    thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
    zs = np.linspace(0, height, n_z)
    vertices = []
    for z in zs:
        for theta in thetas:
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            vertices.append([x, y, z])
    vertices = np.array(vertices)
    
    # Create triangular faces
    faces = []
    for i in range(n_z - 1):
        for j in range(n_theta):
            # Current ring indices
            curr = i * n_theta + j
            next = i * n_theta + (j + 1) % n_theta
            # Next ring indices
            curr_up = (i + 1) * n_theta + j
            next_up = (i + 1) * n_theta + (j + 1) % n_theta
            
            # Two triangles per quad
            faces.append([curr, next, curr_up])
            faces.append([next, next_up, curr_up])
    
    faces = np.array(faces, dtype=int)
    
    return vertices, faces


def plot_hexagonal_grid(hex_centers):
    """
    Plot the hexagonal grid using matplotlib.
    """
    plt.figure()
    plt.plot(hex_centers[:, 0], hex_centers[:, 1], 'o')
    plt.title("Hexagonal Grid of Particles")
    plt.axis('equal')
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid()
    plt.show()


def main():
    args = parse_arguments()

    radius = args.R
    height = 40.0
    spacing =  args.d

    vertices, faces = cylinder_mesh(radius, height, spacing)
    triangles = vertices[faces]
    
    # calculate face normals
    face_normals = np.cross(vertices[faces[:, 1]]-vertices[faces[:, 0]],
                            vertices[faces[:, 2]]-vertices[faces[:, 0]])
    face_normals /= np.sqrt(np.sum(face_normals**2, axis=1, keepdims=True))

    # calculate the center of mass of the triangles
    cm = (triangles[:, 0, :] + triangles[:, 1, :] + triangles[:, 2, :]) / 3
    coords = cm  # Use the center of mass of the triangle as position for the particle

    x = coords[:,0]
    y = coords[:,1]
    z = coords[:,2]
    
    mux = face_normals[:,0]
    muy = face_normals[:,1]
    muz = face_normals[:,2]
    
    Lbox_x = 2*radius+20.0
    Lbox_y = 2*radius+20.0
    Lbox_z = np.max(z)

    outfile = os.path.join(args.path, f'tube_R_{radius}_d_{spacing}.data')

    # Save particle positions
    write_positions(outfile, x, y, z, mux, muy, muz, Lbox_x, Lbox_y, Lbox_z)


    # Plot configuration if requested
    if args.plot:
        plot_hexagonal_grid(coords)

if __name__ == "__main__":
    main()