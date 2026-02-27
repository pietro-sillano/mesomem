best not breaking but almost completely wrapped
nohup mpirun -np 8 lmp_gpu -i wrapping.lmp -v ktilt 14.0 -v ksplay 10.0 -v rcut 2.6 -v wc 2.6 -v zeta 4.0 -v e 8.0 -v r 4.0 > log.out &!



```
mpirun -np 16 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 2.0

```




# plotting thermo information
gnuplot -p -e 'set term qt;plot "thermo_pe.out" u 1:2 w l title "pe particle","thermo_pe.out" u 1:3 w l title "pe mem"'





mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 2.0;

mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 3.0;

mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 4.0;


mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 5.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 5.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 5.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 5.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 5.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 5.0;



mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 5.0;

mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 2.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 3.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 4.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 5.0;


mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 1.0;
mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 1.0;

nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 2.0 > log.out 2>&1 &!

nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 3.0 > log.out 2>&1 &!

nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 4.0 > log.out 2>&1 &!


nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 5.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 5.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 5.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 5.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 5.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 6.0 -v r 5.0 > log.out 2>&1 &!



nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 7.0 -v r 5.0 > log.out 2>&1 &!

nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 2.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 3.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 4.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 8.0 -v r 5.0 > log.out 2>&1 &!


nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 1.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 2.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 3.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 4.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0 -v e 5.0 -v r 1.0 > log.out 2>&1 &!
nohup mpirun -np 6 lmp_radial -i wrapping_radial.lmp -v ktilt 15 -v ksplay 15 -v rcut 2.5 -v wc 1.6 -v zeta 5.0
