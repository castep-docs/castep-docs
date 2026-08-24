# Python Scripts to caclulate Elastic Constants

Andrew Walker (building on work by Dan Wilson) provided some python scripts for calculating elastic constants using CASTEP, available from <https://github.com/andreww/elastic-constants>, the scripts are also distributed with the CASTEP source code and can be found `Utilities/elastic_constants` directory.

The tool comes in two parts - first is generate_strain.py, this takes the results of a successful variable cell geometry optimisation and creates a set of input files to be run through CASTEP. The second part is elastics.py, which takes the CASTEP results and constructs the matrix of elastic constants, Young's modulus, Poisson's ratios and bulk and shear moduli. Usage information for each script can be obtained by using the --help option.

The Elastic constants for a particular system can calculated using these scripts in the following way:

* Perform a variable cell geometry optimisation and make sure to include calculate_stress
* Use the `generate_strain.py` script to generate a set of `.cell` files deformed according to the appropriate strain pattern. The command `generate_strain.py <seedname>` should be sufficient.
* Run CASTEP on each sets of generated input files. Note that the cell distortions can break the symmetry of the crystal.
* Use the `elastics.py` script to read the results of the previous calculations and obtain the elastic constants.

A tutorial for using these scripts can be found in the `Tutorial/Tools` section of this site.
