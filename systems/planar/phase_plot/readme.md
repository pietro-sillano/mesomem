# Sistematic exploration for Gemini radial version

## Spamming jobs
- use `launch_planar_parallel.py` to submit parallel jobs defining number of jobs cpus etc


# Analysis

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
