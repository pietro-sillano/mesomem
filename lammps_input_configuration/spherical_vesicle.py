"""
Spherical Vesicle Generator for LAMMPS
======================================
This script generates a spherical vesicle by placing particles at the centers
of an icosphere's faces. It scales the resulting sphere so that the average
distance between neighboring particles matches a user-defined target distance.

Output:
- A LAMMPS data file containing atom positions, types, diameters,
  densities, charges, and orientation normals.
"""

import numpy as np
import matplotlib.pyplot as plt
from icosphere import icosphere
from sklearn.neighbors import BallTree
from scipy.spatial.distance import pdist

def write_positions(path, atom_positions, face_normals, pred_radius):
    """
    Writes particle data to a LAMMPS-compatible data file.

    Format: atom-ID atom-type x y z diameter density q mux muy muz molecule-ID
    """
    atomtype = 1
    density = 1.0
    diameter = 1.0
    mol_id = 1
    q = 1.0

    # Define simulation box boundaries based on sphere size (with padding)
    box_limit = atom_positions.max(0)[0] * 2.0

    header = f"""\
Generated Spherical Vesicle
Radius approximately {pred_radius:.6f}

{len(atom_positions)} atoms
1 atom types

{-box_limit:.6f} {box_limit:.6f} xlo xhi
{-box_limit:.6f} {box_limit:.6f} ylo yhi
{-box_limit:.6f} {box_limit:.6f} zlo zhi

Atoms
"""

    # Build the atom list: includes position and orientation (face normals)
    lines = []
    for i in range(atom_positions.shape[0]):
        atom_id = i + 1
        x, y, z = atom_positions[i]
        nx, ny, nz = face_normals[i]
        lines.append(f"{atom_id} {atomtype} {x:.6f} {y:.6f} {z:.6f} {diameter} {density} {q} {nx} {ny} {nz} {mol_id}")

    # Save to file
    filename = f"{path}/atom_data_R{pred_radius:.1f}_dist_{target_dist}.lammps"
    with open(filename, "w") as file:
        file.write(header + "\n".join(lines))

    print(f"Success: Generated '{filename}'")

# --- Configuration ---
NOISE = False
path = '.'
target_dist = 0.8  # Desired equilibrium distance between particles

# --- User Input & Estimation ---
print("Vesicle Generator")
print("Choose an iteration value (nu) to determine particle count:")

# Print a lookup table for the user
for nu_val in np.arange(5, 30, 5):
    nr_face = 20 * (nu_val**2)  # Number of faces = number of particles
    print(f"  Iteration: {nu_val:2} | Particles: {nr_face:5} | Estimated Radius: {nu_val / 1.1:.1f}")

nu = int(input("\nEnter iteration number (nu): "))

# --- Geometry Generation ---
# 1. Generate icosphere mesh
vertices, faces = icosphere(nu)
triangles = vertices[faces]

# 2. Calculate Face Normals (Orientation vectors for each particle)
face_normals = np.cross(vertices[faces[:, 1]] - vertices[faces[:, 0]],
                        vertices[faces[:, 2]] - vertices[faces[:, 0]])
# Normalize vectors to unit length
face_normals /= np.sqrt(np.sum(face_normals**2, axis=1, keepdims=True))

# 3. Place particles at the Center of Mass (CM) of each triangle face
face_centers = (triangles[:, 0, :] + triangles[:, 1, :] + triangles[:, 2, :]) / 3

# --- Scaling Logic ---
# Calculate current mean distance between neighboring face centers
tree = BallTree(face_centers)
dist_neighbors, _ = tree.query(face_centers, k=6) # Check 6 nearest neighbors
mean_dist = np.mean(dist_neighbors[:, 1:]) # Exclude distance to self (index 0)

# Scale vertices so the mean distance equals target_dist
scale_factor = target_dist / mean_dist
scaled_vertices = face_centers * scale_factor

print(f"Mean neighbor distance (pre-scale): {mean_dist:.4f}")
print(f"Scale factor applied: {scale_factor:.4f}")

# --- Visualization & Final Stats ---
plt.figure(figsize=(6,6))
plt.plot(face_centers[:, 0], face_centers[:, 1], 'bo', label='Original', alpha=0.5)
plt.plot(scaled_vertices[:, 0], scaled_vertices[:, 1], 'ro', label='Scaled', alpha=0.5)
plt.legend()
plt.title("Vesicle Cross-section (XY Plane)")
plt.axis('equal')
plt.show()

# Calculate final radius using the max distance between any two particles
final_radius = np.max(pdist(scaled_vertices, metric='euclidean')) / 2.0
print(f"Final calculated radius: {final_radius:.4f}")

# Save the LAMMPS file
write_positions(path, scaled_vertices, face_normals, final_radius)
