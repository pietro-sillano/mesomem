# Code used for MesoMem: A mesoscale membrane model based on an additive potential

**Authors:** Pietro Sillano, Timon Idema ...
**Affiliation:** TU Delft
**Correspondence:** p.sillano@tudelft.nl
**Publication Status:** on Arxiv

The link to the publication can be found here. Please cite the below if you use anything from this repository:

```
cite key
```

---

## Content and structure
- `Analysis` folder: it contains various python script to perform analysis from the LAMMPS trajectoy files. Some of them are for properties we dont care anymore and others might need some updates, but they form the base for analysis scripts.

- `benchmarks`: scripts for testing performances.

- `lammps_file`: it contains c++ files for membrane potential and for custom pressure compute.

- `lammps_input_configuration`: it  contains the python script to generate plane, tube and spheres initial configurations.

- `planar`: flat bilayer simulation.

- `python_test`: it contains python scripts used for prelimary testing of the potential.

- `self_assembly`:  self assembly simulation.

- `spherical`:  spherical vesicle simulation.

- `tube`:  lipid tube simulation.

- `volume_control`:  volume controlled simulation.

- `wrapping`: particle wrapping simulation.


# How to use this repository
- Download the repository using the TU Delft credentials (netID and password) or set up the ssh authorization keys.

```
git clone https://gitlab.tudelft.nl/ig-projects/new_potential.git
```

- you will need python, numpy and matplotlib
```
pip install numpy matplotlib
```

- you will also need LAMMPS https://download.lammps.org/tars/lammps-stable.tar.gz


# LAMMPS building instructions
1. Download and unpack with
```
wget --no-check-certificate https://download.lammps.org/tars/lammps-stable.tar.gz
tar -xvf lammps-stable.tar.gz
cd lammps-29Aug2024/
```

2. Move `pair_membrane_sillano_v2.cpp` and `pair_membrane_sillano_v2.h` files from `lammps_file/cpp_files`
 in `src` lammps directory. These files are the new potential and enable the pair_style 'membrane_new' in LAMMPS.

3. Move `compute_pressure.cpp` and `compute_pressure.h` in `src` overwriting the already existing files. This add an additional parameter control in the pressure computing by LAMMPS. Used when we apply a barostat to the simulation.

4. Install or load required compilation tools
```
apt-get install cmake openmpi # if you are using linux/ubuntu/WSL
```
```
module load 2024r1 cmake openmpi # if you are using DelftBlue
```
5. Compile
```
mkdir build
cd build
ccmake  -D BUILD_MPI=yes -D PKG_BROWNIAN=yes -D PKG_MOLFILE=yes -D PKG_EXTRA-PAIR=yes -D PKG_MOLECULE=yes -D PKG_DIPOLE=yes ../cmake
make -j8
make install
```

# Self assembly run
You can run a simple test simulation with `mpirun -np 4 lmp -i self_assembly/self_assembly.lmp -v ktilt 12.0 -v ksplay 1.0 -v N 400 -v rcut 2.5 -v wc 2.0 -v zeta 5.0 -v eps 1.0 -v T 0.2`

Most of simulation produce a `position.lammpstrj` trajectory file that can be visualized with OVITO.

## 📄 License

This project is licensed under the [MIT License / CC-BY 4.0] - see the LICENSE file for details.
