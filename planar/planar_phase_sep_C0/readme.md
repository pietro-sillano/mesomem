#


this one with half red half blue separated already is bending, see position_separating.lammpstrj
```
mpirun -np 8 lmp_radial -i ../in.phase.lmp -v ktilt 20.0 -v ksplay 20.0 -v rcut 2.5 -v wc 1.5 -v zeta 5.0 -v alpha1 -0.4 -v alpha2 0.4 -v alpha12 0.0
```

- it seems that if alpha is negative is not really influencing much what is happening
