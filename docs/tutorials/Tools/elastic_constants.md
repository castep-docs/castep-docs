# Elastic Constants python scripts tutorial

Andrew Walker (building on work by Dan Wilson) provides some python scripts for calculating elastic constants using CASTEP, available from <https://github.com/andreww/elastic-constants>. The tool comes in two parts - first is generate_strain.py, this takes the results of a successful variable cell geometry optimisation and creates a set of input files to be run through CASTEP. The second part is elastics.py, which takes the CASTEP results and constructs the matrix of elastic constants, Young's modulus, Poisson's ratios and bulk and shear moduli. Usage information for each script can be obtained by using the `--help` option.

For this exercise we will use rutile - titanium dioxide. Below are example `.cell` and `.param` files to start from. It is assumed that the scripts `generate_strain.py` and `elastics.py` are in your PATH and that python is installed.

```text
#TiO2.cell
 %BLOCK lattice_cart
 4.594 0.000 0.000
 0.000 4.594 0.000
 0.000 0.000 2.959
 %ENDBLOCK lattice_cart

 %BLOCK positions_frac
 Ti  0.000  0.000  0.000
 Ti  0.500  0.500  0.500
 O   0.305  0.305  0.000
 O  -0.305 -0.305  0.000
 O   0.805  0.195  0.500
 O  -0.805 -0.195  0.500
 %ENDBLOCK positions_frac

 symmetry_generate

 kpoint_mp_grid 3 3 3
```

```text
#TiO2.param
 task             : geometryoptimisation
 cutoff_energy    : 700 eV
 xc_functional    : PBE
 max_scf_cycles   : 100
 calculate_stress : true
 opt_strategy     : speed
 num_dump_cycles  : 0
```

* Task 1: Perform a variable cell geometry optimisation and make sure to include calculate_stress : true in your param file. Test the kinetic energy cut-off and k-point grid such that the stress is converged to within the default geom_stress_tol value. (Hint: Use CASTEP's built-in help utility to find the default.)

* Task 2: Use the `generate_strain.py` script to generate a set of .cell files deformed according to the appropriate strain pattern. The command `generate_strain.py TiO2` should be sufficient.
You should now have twelve (in this case) sets of input files - individual .cell files and corresponding `.param`, symbolically linked to the original `TiO2.param` file. Notice that the new .cell files all have the `FIX_ALL_CELL true` option set.

* Task 3: Run CASTEP on each of the 12 sets of input files. Note that the cell distortions can break the symmetry of the crystal, hence changing the number of k-points in the symmetry reduced sample. The `-dryrun` option of CASTEP can be used to do a quick check for how many k-points are required. This can help when selecting how many cores to run the calculation on if you are running CASTEP in parallel.

* Task 4: Run the `elastics.py` script to obtain the elastic constants. The command `elastics.py TiO2` will print the results to the terminal. The `--latex` option generates a LaTeX formatted summary of the results and the `--graphics` option produces a graphical representation of the stress-strain fits in a .png file.

* Task 5: Investigate how the results and their errors change with smaller values of the `elec_energy_tol` parameter. Also investigate the effect of changing the `--strain` option to `generate_strain.py`. Move any old `*cij*.castep` files to another directory - the `elastics.py` script only checks the first set of data in a concatenated `.castep` file.
