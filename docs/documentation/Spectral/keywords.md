
`SPECTRAL_TASK` - determines what will be calculated. All tasks will compute the eigenenergies (aka bands). The list of tasks, and the extra  properties calculated are as follows:

* `bandstructure`   
*  `dos`         band gradients
*   `optics`     optical matrix elements
* `pdos`  atomic projections
* `coreloss` dipole matrix elements with core states    


Most spectral calculations will involve the calculation of unoccupied states. One of the following parameters should be set to determine the number of states calculated.

```
SPECTRAL_NEXTRA_BANDS            number of extra spectral bands
SPECTRAL_PERC_EXTRA_BANDS        percentage of extra spectral bands
SPECTRAL_NBANDS                  number of bands/k-point in spectral calc
```

It is possible to use a different exchange-correlation functional to the one used for the groundstate. An example might be when a semi-local functional (such as PBE) is used for the groundstate, and a more expensive non-local functional (e.g. PBE0) is used for the spectral calculation. This is an approximation and should be done with cuation. To set the xc functional use one of the two keywords.

```
SPECTRAL_XC_FUNCTIONAL           spectral exchange-correlation functional
SPECTRAL_XC_DEFINITION           spectral exchange-correlation functional
```

To change the convergence tolerance for the eigenvalues set
```
SPECTRAL_EIGENVALUE_TOL          ! default: 10E-6 eV
```


SPECTRAL_MAX_ITER                maximum iterations in spectral calculation
SPECTRAL_MAX_STEPS_PER_ITER      maximum steps per iter in spectral calculation
