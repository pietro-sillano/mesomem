# MesoMem examples

Example inputs for the MesoMem membrane model, written in the same style as the
example in the LAMMPS distribution (`examples/PACKAGES/mesomem`). They need a
LAMMPS build that has [`pair_style mesomem/dipole`](https://docs.lammps.org/pair_mesomem_dipole.html)
(DIPOLE package). Run them from this folder, because each input reads its data file
from the current directory:

```bash
cd examples
mpirun -np 4 lmp -in in.planar
```

| Input | Data file | System |
| --- | --- | --- |
| `in.planar` | `data.planar` | Flat membrane of 2125 particles that spans the periodic box. After equilibration at constant area, a barostat on x and y relaxes it to zero tension. The thermo output reports the projected area. |
| `in.vesicle` | `data.vesicle` | Spherical vesicle of 2000 particles with radius 10.88. The thermo output reports the radius of gyration. |
| `in.selfassembly` | `data.selfassembly` | 1500 particles that start as small aggregates and grow into flat membrane patches. The thermo output reports the number of clusters, the largest cluster and the number of free particles. These files are the same as the ones shipped with LAMMPS. |

The model parameters are set with `index` variables at the top of each input. You can
change them from the command line:

```bash
lmp -in in.vesicle -var ktilt 12.0 -var T 0.25
```

| Variable | Meaning | Default |
| --- | --- | --- |
| `eps` | Depth of the isotropic potential minimum | 1.0 |
| `rcut` | Cutoff of the isotropic potential | 2.5 |
| `ktilt` | Tilt stiffness | 15.0 |
| `ksplay` | Splay stiffness | 1.0 |
| `wc` | Cutoff of the tilt and splay energies (`wc` ≤ `rcut`) | 2.0 |
| `zeta` | Width of the attractive branch (larger is narrower); sets the in-plane diffusivity | 5.0 |
| `c0` | Spontaneous curvature | 0.0 |
| `T` | Temperature of the Langevin thermostat | 0.2 |

To write a trajectory or images, uncomment the `dump` lines in an input.
