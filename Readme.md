# MesoMem: A mesoscale membrane model based on an additive potential

**Authors:** Pietro Sillano, Timon Idema, Siewert-Jan Marrink

**Affiliation:** TU Delft

**Correspondence:** t.idema@tudelft.nl, p.sillano@tudelft.nl

**Publication Status:** Available on [ArXiv](https://doi.org/10.48550/arXiv.2602.24123)

If you use this model or code in your research, please cite the following:

```bibtex
@misc{sillano2026mesomemmesoscalemembranemodel,
      title={MesoMem: A mesoscale membrane model based on an additive potential},
      author={Pietro Sillano and Siewert-Jan Marrink and Timon Idema},
      year={2026},
      eprint={2602.24123},
      archivePrefix={arXiv},
      primaryClass={cond-mat.soft},
      url={https://arxiv.org/abs/2602.24123},
}

```

![image](/systems/systems.png)

---

## 📂 Content and Structure

* **`Analysis/`**: Python scripts to perform analysis from the LAMMPS trajectoy files, in particular for planar systems.
* **`lammps_file/`**: C++ source files for the membrane potential (`pair_style membranesillanov2`) and custom pressure compute.
* **`lammps_input_configuration/`**: Python scripts to generate initial configurations (planar, tubes, and spheres).
* **`systems/`**: LAMMPS input scripts (`.lmp`) and analysis tools for various physical setups:
* `planar`: All planar membrane systems.
* `self_assembly`: Self-assembly simulations from random distributions.
* `spherical`: Vesicle-related simulations.
* `volume_control`: Simulations involving osmotic pressure or volume constraints.
* `wrapping`: Nanoparticle-membrane wrapping studies.
* **`benchmarks/`**: Scripts for evaluating model performance.

---

## How to use the model

### 1. Clone the Repository

```bash
git clone https://gitlab.tudelft.nl/idema-group/mesomem.git
```

### 2. LAMMPS Installation

This model requires building a custom version of LAMMPS.

1. **Download LAMMPS:**
```bash
wget --no-check-certificate https://download.lammps.org/tars/lammps-stable.tar.gz
tar -xvf lammps-stable.tar.gz
```


2. **Patch Source Files:** Run the provided setup script to move the MesoMem potential and modified pressure computes into the LAMMPS `src` directory.
```bash
cp mesomem/cpp_files/*.{cpp,h} path_to_lammps/src/
```


3. **Compile:**
```bash
cd path_to_lammps/
mkdir build && cd build
cmake -D BUILD_MPI=yes -D PKG_BROWNIAN=yes -D PKG_MOLFILE=yes -D PKG_EXTRA-PAIR=yes -D PKG_MOLECULE=yes -D PKG_DIPOLE=yes ../cmake
make -j8
```


---

## Running a Simulation

You can test the self-assembly of a vesicle using the following command:

```bash
mpirun -np 4 lmp -i systems/self_assembly/self_assembly.lmp -v ktilt 12.0 -v ksplay 1.0 -v N 400 -v rcut 2.5 -v wc 2.0 -v zeta 5.0 -v eps 1.0 -v T 0.2

```

### Key Parameters

| Variable | Description | Typical Range |
| --- | --- | --- |
| `ktilt` | Bending/Tilt modulus | 10.0 - 20.0 |
| `ksplay` | Splay modulus | 0.5 - 2.0 |
| `rcut` | Interaction cutoff distance | 2.5 - 3.0 |
| `wc` | Orientation cutoff distance | 1.8 - `rcut` |

**Visualization:** Use [OVITO](https://www.ovito.org/) with the `sphere-dipole-molecule` hybrid visualization to view the `position.lammpstrj` output.

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
