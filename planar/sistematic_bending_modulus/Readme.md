# Content


# check autocorrelation times

```
mpirun -np 4 lmp_radial -in ../test_acorr.lmp -v ktilt 12.0 -v ksplay 1.0 -v N 2500 -v rcut 2.5 -v wc 2.0 -v zeta 5.0 -v T 0.25
```

mpirun -np 4 lmp_radial -in ../test_acorr.lmp -v ktilt 12.0 -v ksplay 1.0 -v N 2500 -v rcut 2.5 -v wc 2.0 -v zeta 5.0 -v T 0.25 -v t_dump 1000 -v seed 12234


# Pipeline

```python
python launching_baro.py --path /martini/pietro/new_potential/planar/fluctuation_pipeline/ --name in.baro --lmp_bin lmp_radial --nprocs 4 --total_cpus 28
```

```
nohup python launching_baro.py --path /martini/pietro/new_potential/planar/fluctuation_pipeline/ --name in.baro --lmp_bin lmp_radial --nprocs 4 --total_cpus 24 > log.out 2>&1  &!

```

This for the panel plot, three plots together with fit:
```
python plot_together.py N_2500_d_0.9_kt_12.0_ks_1.0_rcut_2.5_wc_2.2_T_0.25_zeta_5/ N_2500_d_0.9_kt_30_ks_1.0_rcut_2.5_wc_2.2_T_0.25_zeta_5 N_2500_d_0.9_kt_50_ks_1.0_rcut_2.5_wc_2.2_T_0.25_zeta_5

```




