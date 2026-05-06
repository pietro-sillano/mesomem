# Vesicle Volume Control
This simulation regulates the inner volume of a membrane vesicle by adding explicit solvent particles inside and outside the membrane.

### Key Parameters
* **Model Parameters**: `ktilt`, `ksplay`, `rcut`, and `wc` (refer to the paper for physical definitions).
* **Solvent Count**: `NIN` and `NOUT` set the number of particles inside and outside the vesicle.
* **Initial Radius**: `r_initial` must match the radius of the vesicle in your LAMMPS data file.

### Execution Command
Run the simulation using MPI (e.g., 8 processors) with the following command:

```bash
mpirun -np 8 lmp_radial -i in.volume_control.lmp \
  -v ktilt 15.0 -v ksplay 1.0 -v rcut 2.5 -v wc 2.0 \
  -v NOUT 15000 -v NIN 1000 -v r_initial 10.0
```
