
To perform a molecular dynamics calculation set the task parameter
```
task : md
```

To control the length of the dynamics simulation

* `md_num_iter` :    number of MD steps (default 100)
* `md_delta_t` :     MD timestep (default 1fs)

To control the conditions for the dynamics

* `md_ensemble` :    Ensemble (NVE, NVT, NPH, NPT, HUG)
* `md_thermostat` :  Thermostat to use if not a constant energy ensemble. values: NOSE-HOOVER (default), LANGEVIN, HOOVER-LANGEVIN
* `md_barostat` :    Barostat to use if not a constant volume ensemble. Values: ANDERSEN-HOOVER (default), PARRINELLO-RAHMAN
* `md_temperature` : Temperature to use if not a constant energy ensemble

For the Huginot Thermostat

* `md_hug_method` :                    Hugoniostat method. Values: NONE (default), NVHUG, NPHUG
* `md_hug_dir` :                       Hugoniostat compression direction. Values: XDIR, YDIR, ZDIR, ISO (default)
* `md_hug_t` :                         Hugoniostat coupling constant.
* `md_hug_compression` :               Hugoniostat compression ratio. Values from 0.0 to 1.0 (default)

### Path Integral MD (PIMD)


* MD_USE_PATHINT                   PIMD on/off
* MD_NUM_BEADS                     PIMD number of beads
* MD_PATHINT_INIT                  PIMD initialisation method
* MD_PATHINT_STAGING               PIMD staging modes on/off
* MD_PATHINT_NUM_STAGES            PIMD number of stages


ionic_velocities ??


### Advanced settings

It is possible to change the tolerances for accepting the SCF groundstate during the molecular dynamics run. The default value are those for a single point energy e.g. the default for `md_elec_energy_tol` is the value of `elec_energy_tol`

* `md_elec_energy_tol` :  MD total energy per atom convergence tolerance
* `md_elec_eigenvalue_tol` : MD eigenvalue convergence tolerance
* `md_elec_force_tol` : max force per atom convergence tolerance
* `md_elec_convergence_win` :      MD convergence tolerance window

* MD_EQM_METHOD                    MD enhanced equilibration method
* MD_EQM_ION_T                     MD equilibration time for ions
* MD_EQM_CELL_T                    MD equilibration time for cell
* MD_EQM_T                         MD equilibration time
* MD_ION_T                         MD characteristic ionic time
* MD_CELL_T                        MD characteristic cell time


* MD_CELL_DAMP_RINGING             Damp cell ringing mode
* MD_USE_PLUMED                    Use PLUMED metadynamics
