# Sistematic exploration for Gemini radial version

# notes for v2

- it seems that ks should be smaller than kt, probably also smaller than kt/2.0.
- increasing wc or rcut it generally stabilize the plane.
- I think I can use rcut = 2.5 and wc = 1.8
- at least kt=10 and ks=2 to have a stable bilayer
- if you use zeta small you are getting a double layer


this one is vesiculating very easily but in a double layer: `N_2500_d_0.8_eps_1.0_sigma_1.0_kt_10.0_ks_3.0_rcut_2.5_wc_1.7_T_0.3_zeta_5/position.lammpstrj`


good bilayer`N_2500_d_0.8_eps_1.0_sigma_1.0_kt_10.0_ks_2.0_rcut_2.5_wc_1.7_T_0.3_zeta_5/position.lammpstrj`


this one very good bilayer
 N_2500_d_0.8_eps_1.0_sigma_1.0_kt_20.0_ks_5.0_rcut_2.5_wc_2.0_T_0.3_zeta_5/position.lammpstrj


### after analysis
- if you look at stability_plot2.png:




# to perform analysis

```
python preprocess_csv.py --data_dir phase_plot_radial/
```

```
python planar_analysis_v2.py --data_dir phase_plot_radial/
```

```
python stability.py # for alpha exponent
python diffusion.py # for diffusion coefficient
```

# for new version v2

```
mpirun -np 4 lmp_radial -i in.phase.lmp -v ktilt 12.0 -v ksplay 3.0 -v N 2500 -v rcut 2.5 -v wc 1.8 -v zeta 6.0
```
