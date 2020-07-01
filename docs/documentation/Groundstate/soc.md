




##keywords

For a calculation of a non-spin polarised system with spin orbit coupling (e.g. GaAs) the following keywords should be set in the param file

```
spin_treatment          : vector
spin_orbit_coupling     : true
spin_polarised          : false
```

If the system has a spin density (e.g. a ferromagnet or antiferromagnet) then the following keywords should be set in the para file

```
spin_treatment          : vector
spin_orbit_coupling     : true
spin_polarised          : true
```

As the spin-orbit coupling is transmitted via the pseudopotential is is neccessary to use j-dependant pseudopotentials. These are available for the whole periodic table as .uspso files.

## Limitations
