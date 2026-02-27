# Measuring Bending Modulus
There are couple of ways to compute bending modulus of a membrane bilayer:
- Measuring the fluctuation spectrum of a tensionless membrane (most common). One example of implementation is Fowler [5]. It is difficult to get accurate measurements from it, see Deserno paper for a in-depth discussion[4]. It is also tricky to get enough sampling for large fluctuating modes. This can be checked measuring autocorrelation of these modes.

- From the relation of a lipid tube radius with the applied tension, see Membrane tutorials [1]

- From buckling membrane, see [3]]


# Fluctuation Spectrum
## Content
- `baro_ADAM.lmp` is a lammps simulation file that it has been adapted from Adam Prada original script (he used on Yuan model). it runs a quite big membrane plane with zero lateral tension barostat.

- `spectrum_pietro.py` folder contains Pietro implementation for calculating the spectrum
  - `read_data_lammps.py` and `spectrum_tools.py` python utilities collection.

  - `spectrum.py` analyze simulation trajectory and produce a fluctuation spectrum plot and a fit. It is not satisfying enough but it is a starting point.

- `fancy_calculations` is an adaptation from Membrane tutorials [1], initially used for Cooke Deserno model. It is still not getting us so nice results, but it is worth understanding it more. Quite refined method, details on the theory of this implementation in Archea paper [2].

- `autocorr_fourier_modes.py` contains a script to process a LAMMPS simulation and plot autocorrelation of fluctuating modes.

# Relaxing tube
Check [1] and [3]

# Buckled membrane
Check [3]



# References
[1] M. Muñoz Basagoiti, F. Frey, B. Meadowcroft, M. Amaral, A. Prada, and A. Saric, “A tutorial for mesoscale computer simulations of lipid membranes: tether pulling, tubulation and fluctuations,” Soft Matter, p. 10.1039.D5SM00148J, 2025, doi: 10.1039/D5SM00148J.
[2] M. Amaral, F. Frey, X. Jiang, B. Baum, and A. Šarić, “Stability vs flexibility: reshaping archaeal membranes in silico,” Aug. 18, 2025. doi: 10.7554/eLife.105432.2.
[3] https://www.cmu.edu/biolphys/deserno/mbtools/mbtools_tutorial-2015.pdf
[4] M. F. Ergüder and M. Deserno, “Identifying systematic errors in a power spectral analysis of simulated lipid membranes,” The Journal of Chemical Physics, vol. 154, no. 21, p. 214103, June 2021, doi: 10.1063/5.0049448.
[5] P. W. Fowler, J. Hélie, A. Duncan, M. Chavent, H. Koldsø, and M. S. P. Sansom, “Membrane stiffness is modified by integral membrane proteins,” Soft Matter, vol. 12, no. 37, pp. 7792–7803, 2016, doi: 10.1039/C6SM01186A.
