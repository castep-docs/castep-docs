To perform a geometry optimisation set the task parameter
```
task : geomopt
```

The convergence criteria have the following default values, each of which can be set independently.

* `geom_energy_tol` : Tolerance on energy change between iterations   (default: 2.0e-5 eV)
* `geom_force_tol`  : Tolerance on maximum force on each atom  (default: 0.05 eV/ANG)
* `geom_stress_tol` : Tolerance on maximum stress on cell  (default: 0.1 GPa)
* `geom_disp_tol`  :  Tolerance on change in atom positions between iterations  (default: 0.001: Ang)
* `geom_max_iter`   : Maximum number of iterations  (default: 30)


It is possible to change the optimisation method, and to choose a preconditioner.
```
geom_method     : LBFGS (default), BFGS, TPSD, DAMPEDMD, FIRE
geom_preconditioner : EXP / FF / ID  # EXPonential, Force Field, Identity (default)
```

It is useful to set the following two parameters in a geometry optimisation.
These will cause CASTEP to write a new cell/cif file with the final optimised
coordinates
```
write_cell_structure : T
write_cif_structure  : T
```
