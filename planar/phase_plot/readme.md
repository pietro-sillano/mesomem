# Sistematic exploration for Gemini radial version

## Spamming jobs
- use `launch_planar_parallel.py` to spam parallel jobs defining number of jobs cpus etc

```
python3 launch_planar_parallel.py --path /home/pietro/martini/new_potential/planar/phase_plot_radial --name in.planar_radial --lmp_bin lmp_radial --nprocs 4 --total_cpus 12
```

for some reason that i do not understand the only way to occupy all cpus is to use 4 mpi task per simulation, running 3 simulation in parallel to fill the 12 cpus

## varying parameters and setting up simulations
- the minimal energy lattice for rcut=2.5 is d=0.75, BUT we are not at T=0 so we should consider that, maybe it is better to use d=0.85
- We can start with N=400 and move to N=2500 later

- HP1: see zeta and T influence on system phases. Tmax=0.3. ks=5.0 kt=8.0 wc=1.6 rcut=2.5



# to perform analysis

move all dir in new folder `data` inside data_dir

Launching from the analysis folder:


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
