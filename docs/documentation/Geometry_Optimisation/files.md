## .geom

The `.geom` file is the primary output file, and contains the unit cell, positions of the atoms and the forces on the atoms 
for each step of the geometry optimisation. The format of this file is very similar to the `.md` file.

```
BEGIN header

END header

                                     0                                     F   F   F   F            <-- c
                    -1.1089287934762380E+000   -1.1089287934762380E+000                             <-- E
                     1.1338356755021575E+001    0.0000000000000000E+000    0.0000000000000000E+000  <-- h
                     6.9427411538139708E-016    1.1338356755021575E+001    0.0000000000000000E+000  <-- h
                     6.9427411538139708E-016    6.9427411538139708E-016    1.1338356755021575E+001  <-- h
H               1    0.0000000000000000E+000    0.0000000000000000E+000    0.0000000000000000E+000  <-- R
H               2    0.0000000000000000E+000    0.0000000000000000E+000    1.8897261258369291E+000  <-- R
H               1    5.2328399876121735E-008   -1.0421543664521416E-007    7.0009877481903737E-002  <-- F
H               2   -5.2328399876121735E-008    1.0421543664521414E-007   -7.0009877481903737E-002  <-- F

                                     1                                     F   F   F   T            <-- c
                    -1.1238786617585625E+000   -1.1238786617585625E+000                             <-- E
                     1.1338356755021575E+001    0.0000000000000000E+000    0.0000000000000000E+000  <-- h
                     6.9427411538139708E-016    1.1338356755021575E+001    0.0000000000000000E+000  <-- h
                     6.9427411538139708E-016    6.9427411538139708E-016    1.1338356755021575E+001  <-- h
H               1    9.4833861449528325E-008   -1.8886784811136898E-007    1.2687770000486739E-001  <-- R
H               2   -9.4833861449528339E-008    1.8886784811136895E-007    1.7628484258320618E+000  <-- R
H               1   -3.5821658412345467E-009    7.1341230429117867E-009    4.3459352502549203E-002  <-- F
H               2    3.5821658412345467E-009   -7.1341230429117867E-009   -4.3459352502549203E-002  <-- F

                                     5                                     T   T   T   T            <-- c
                    -1.1282766172341445E+000   -1.1282766172341445E+000                             <-- E
                     1.1338356755021575E+001    0.0000000000000000E+000    0.0000000000000000E+000  <-- h
                     6.9427411538139708E-016    1.1338356755021575E+001    0.0000000000000000E+000  <-- h
                     6.9427411538139708E-016    6.9427411538139708E-016    1.1338356755021575E+001  <-- h
H               1   -3.9595146097124387E-007    7.8856409239690845E-007    2.1772199021621047E-001  <-- R
H               2    3.9595146097124376E-007   -7.8856409239690845E-007    1.6720041356207189E+000  <-- R
H               1   -8.2747158669639466E-009    1.6479675454026804E-008    1.5340573808683700E-006  <-- F
H               2    8.2747158669639466E-009   -1.6479675454026804E-008   -1.5340573808683700E-006  <-- F
```

All quantities are reported in atomic units (this cannot be changed by any parameter)

* `<-- c` Reports the iteration number and whether the convergence criteria are satisfied.
* `<-- E` Energy (total energy, enthalpy)
* `<-- h` Unit cell vectors
* `<-- S` Stress on unit cell (only reported if the cell is allowed to change)
* `<-- R` Cartesian positions of atoms
* `<-- F` Force on atoms

The '<-- c' line also reports the status of 4 convergence flags (either F=false or T=true). These are (in order):

* dE - has the energy change/atom been below geom_energy_tol for the last geom_convergence_win steps?
* Fmax - is the largest component of any force below geom_force_tol?
* dRmax - is the largest change in position for any atom below geom_disp_tol?
* Smax - is the largest component of the stress tensor below geom_stress_tol?
