
Instead of using the forces to optimise the structure of the system, CASTEP can instead use the forces to accelerate the atoms (and cell-shape) in order to simulate dynamical properties - a method known as "Molecular Dynamics" or simply "MD". To perform this kind of calculation, set

task : MD

in your param file.

CASTEP has a wide range of Molecular Dynamics (MD) capabilities, and can do equilibrium MD using a variety of ensembles:

* NVE - the microcanonical ensemble - with fixed number of atoms, volume of cell, and total energy conserved
* NVT - the canonical ensemble - with constant temperature not constant energy - due to the application of a thermostat
* NPH - constant external pressure and enthalpy - due to the application of a barostat
* NPT - constant external pressure and temperature - due to the application of a barostat and a thermostat
* HUG - ??

Of these, NPT is the closest to most real-life experiments.

Of the different thermostats, CASTEP supports Nose-Hoover, Nose-Hoover chains, Langevin and Hoover-Langevin.

Of the different barostats, CASTEP supports the isotropic Andersen-Hoover barostat, and the anisotropic Parrinello-Rahman barostat.

CASTEP also supports the Berendsen thermostat and barostat, as a route to faster equilibration before switching to one of the above thermostats/barostats for production data.

CASTEP can also go beyond the Born-Oppenheimer approximation to do quantum dynamics, using Path Integral Molecular Dynamics (PIMD), in either NVT or NPT ensembles.

In all MD schemes, CASTEP can support both linear and non-linear constraints on the ionic positions and/or on the cell vectors. The detailed trajectory information is written to either  `<seed>.geom` or  `<seed>.md` files, which are structured text files, for ease of manipulation and post-calculation analysis.
