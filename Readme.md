# MesoMem: A Mesoscale Membrane model based on an additive potential

**Authors:** Pietro Sillano, Siewert J. Marrink, Timon Idema

**Affiliation:** TU Delft

**Correspondence:** t.idema@tudelft.nl, p.sillano@tudelft.nl

**Publication:** [Phys. Rev. E **114**, 034412 (2026)](https://doi.org/10.1103/4dhv-8xd7) · preprint on [arXiv](https://arxiv.org/abs/2602.24123)

If you use this model or code in your research, please cite the following:

```bibtex
@article{4dhv-8xd7,
  title = {MesoMem: A mesoscale membrane model based on an additive potential},
  author = {Sillano, Pietro and Marrink, Siewert J. and Idema, Timon},
  journal = {Phys. Rev. E},
  volume = {114},
  issue = {3},
  pages = {034412},
  numpages = {11},
  year = {2026},
  month = {Sep},
  publisher = {American Physical Society},
  doi = {10.1103/4dhv-8xd7},
  url = {https://link.aps.org/doi/10.1103/4dhv-8xd7}
}
```

![image](/systems/systems.png)

---

## 📂 Content and Structure

* **`Analysis/`**: Python scripts to perform analysis from the LAMMPS trajectoy files, in particular for planar systems.
* **`lammps_file/`**: C++ source files for the membrane potential (`pair_style mesomem`) and custom pressure compute.
* **`lammps_input_configuration/`**: Python scripts to generate initial configurations (planar, tubes, and spheres).
* **`examples/`**: Ready-to-run inputs for a flat membrane, a spherical vesicle and self-assembly, using `pair_style mesomem/dipole` from LAMMPS.
* **`systems/`**: Original research input scripts (`.lmp`, older `pair_style mesomem`) and analysis tools for various physical setups:
* `planar`: All planar membrane systems.
* `self_assembly`: Self-assembly simulations from random distributions.
* `spherical`: Vesicle-related simulations.
* `volume_control`: Simulations involving osmotic pressure or volume constraints.
* `wrapping`: Nanoparticle-membrane wrapping studies.

---

## How to use the model
Now MesoMem is packaged into the latest release of LAMMPS: [MesoMem pair potential](https://docs.lammps.org/pair_mesomem_dipole.html) and ready to use. OpenMP and Kokkos (GPU) accelerated version are available too.
---

## Running a Simulation

The [`examples/`](examples/) folder has inputs for a flat membrane (`in.planar`), a spherical vesicle (`in.vesicle`) and self-assembly (`in.selfassembly`). Run them from that folder:

```bash
cd examples
mpirun -np 4 lmp -in in.selfassembly -var ktilt 12.0
```

See [`examples/README.md`](examples/README.md) for what each example does and all parameters.

The scripts in `systems/` use the older `pair_style mesomem` from `cpp_files/`, and their parameters are passed on the command line with `-v`.

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
