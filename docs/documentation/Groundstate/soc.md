




##keywords

For a calculation of a non-spin polarised system with spin orbit coupling (e.g. GaAs) the following keywords should be set in the param file

```
spin_treatment          : vector
spin_orbit_coupling     : true
spin_polarised          : false
relativistic_treatment  : dirac
```

If the system has a spin density (e.g. a ferromagnet or antiferromagnet) then the following keywords should be set in the para file

```
spin_treatment          : vector
spin_orbit_coupling     : true
spin_polarised          : true
relativistic_treatment  : dirac
```

As the spin-orbit coupling is transmitted via the pseudopotential is is necessary to use j-dependent pseudopotentials. These can be read from file (UPF or uspso) or generated on the fly. At the moment the SOC19 set of OTFG norm-conserving potentials are suitable. These can be specified with the following block in the cell file
```
%block species_pot
SOC19
%endblock species_pot

## Limitations
