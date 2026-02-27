# Spherical
## Running a simulation
This is the simplest spherical vesicle you can simulate.

You can run a simulation with the following commands:
- serial simulation (one cpu)
```bash
lmp -i in.spherical.lmp -v ktilt 12.0 -v ksplay 1.0 -v rcut 2.5 -v wc 2.0
```

- parallel simulation (4 cpu) if you have openmpi
```
mpirun -np 4 lmp_radial -i in.spherical.lmp -v ktilt 12.0 -v ksplay 1.0 -v rcut 2.5 -v wc 2.0
```

## Modification
- you can generate smaller or bigger vesicle using the python script in lammps_inout_configuration in the main folder.

## Note
- The parameters I listed above are the most stabke but you can experiment with changing kt,ks,wc,rcut or simulation temperature.



# old test
## test 1
Increasing Ksplay increase the potential energy, less stable. but then lowering to 3,0 is not making a great difference

mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 10.0 -v ksplay 10.0 -v rcut 2.5 -v wc 1.6 -v T 0.2    u: -3.0
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 10.0 -v ksplay 20.0 -v rcut 2.5 -v wc 1.6 -v T 0.2    u: -2.95
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 10.0 -v ksplay 50.0 -v rcut 2.5 -v wc 1.6 -v T 0.2    u: -2.85
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 10.0 -v ksplay 3.0 -v rcut 2.5 -v wc 1.6 -v T 0.2     u: -3.0


# test 2
increasing ktilt decrease also a bit the potential energy
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 10.0 -v ksplay 10.0 -v rcut 2.5 -v wc 1.6 -v T 0.2    u: -3.0
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 20.0 -v ksplay 10.0 -v rcut 2.5 -v wc 1.6 -v T 0.2    u: -2.98
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 50.0 -v ksplay 10.0 -v rcut 2.5 -v wc 1.6 -v T 0.2    u: -2.90

# test 3
minimum ktilt before having a double layer
mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 5.0 -v ksplay 10.0 -v rcut 2.5 -v wc 1.6 -v T 0.2   double layer is more favorable than single layer(-5 vs -3)

mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 8.0 -v ksplay 10.0 -v rcut 2.5 -v wc 1.6 -v T 0.2   double layer is more favorable than single layer(-3.6 vs -3)

mpirun -np 4 lmp_new -i in.spherical.lmp -v ktilt 5.0 -v ksplay 50.0 -v rcut 2.5 -v wc 1.6 -v T 0.2   got a pancake splattered


# test 4
if you increase ksplay a lot a flatter conformation is encouraged.
with smaller ks it seems to have more spherical fluctuations.





