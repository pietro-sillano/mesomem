# mpirun -np 4 lmp_radial -in ../in.planar_v2.lmp -v rcut 2.5 -v wc 2.0 -v ktilt 10.0 -v ksplay 2.0 -v N 2500 -v T 0.2 -v zeta 6.0 -v d 0.80



python /martini/pietro/new_potential/Analysis/preprocess_csv.py     --data_dir phase_plot_1 --base_dir /martini/pietro/new_potential_v2/planar/ ;

python /martini/pietro/new_potential/Analysis/planar_analysis_v2.py --data_dir phase_plot_1/ --base_dir /martini/pietro/new_potential_v2/planar/

python stability.py
python diffusion.py
