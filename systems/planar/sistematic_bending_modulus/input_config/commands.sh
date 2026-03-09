python planar_lattice.py --path . --N 50 --PBC --d 0.80
mpirun -np 4 lmp_new -i in.planar.lmp -v ktilt 10.0 -v ksplay 10.0 -v N 2500 -v rcut 3.0 -v wc 3.0 -v input lattice_d_0.80_N_2500
# energy -10.11


python planar_lattice.py --path . --N 50 --PBC --d 0.85
mpirun -np 4 lmp_new -i in.planar.lmp -v ktilt 10.0 -v ksplay 10.0 -v N 2500 -v rcut 3.0 -v wc 3.0 -v input lattice_d_0.85_N_2500
# energy -10.11


python planar_lattice.py --path . --N 50 --PBC --d 1.00
mpirun -np 4 lmp_new -i in.planar.lmp -v ktilt 10.0 -v ksplay 10.0 -v N 2500 -v rcut 3.0 -v wc 3.0 -v input lattice_d_1.00_N_2500
# energy -9.22


python planar_lattice.py --path . --N 50 --PBC --d 1.12
mpirun -np 4 lmp_new -i in.planar.lmp -v ktilt 10.0 -v ksplay 10.0 -v N 2500 -v rcut 3.0 -v wc 3.0 -v input lattice_d_1.12_N_2500
# energy -9.19


python planar_lattice.py --path . --N 50 --PBC --d 1.3
mpirun -np 4 lmp_new -i in.planar.lmp -v ktilt 10.0 -v ksplay 10.0 -v N 2500 -v rcut 3.0 -v wc 3.0 -v input lattice_d_1.30_N_2500
# energy -4.69
