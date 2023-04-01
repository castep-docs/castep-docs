
## Electronic excitations of the Azobenzene molecule

In this example we calculate the first two electronic excited states of
E-Azobenzene in a supercell.

The required files are azo.cell and azo.param:

*azo.param*

```
    task: SinglePoint

    reuse: default
    calculate_deltascf  : true
    deltascf_method     : simple
    deltascf_smearing   : 0.01

#band  occ spin from_band to_band
%block deltascf_constraints
34    0.5000  1   34   34       
35    0.5000  1   35   35
%endblock deltascf_constraints

    spin_polarized : False
    cut_off_energy : 350.0
    elec_energy_tol : 1e-07
    fix_occupancy : False
    iprint : 1
    max_scf_cycles : 200
    metals_method : dm
    mixing_scheme : Pulay
    nextra_bands : 10
    num_dump_cycles : 0
    opt_strategy_bias : 3
    smearing_scheme : Gaussian
    smearing_width : 0.1
    xc_functional : PBE
```

*azo.cell*

```
    %BLOCK LATTICE_CART
        10.0000000 0.0000000000 0.0000000000
        0.0000000000 20.0000000 0.0000000000
        0.0000000000 0.0000000000 10.0000000000
    %ENDBLOCK LATTICE_CART

    %BLOCK POSITIONS_ABS
    C         -6.72081       -1.66625        0.00000
    C         -6.64967       -0.26964        0.00000
    C         -5.40647        0.36858       -0.00000
    C         -4.23175       -0.38857       -0.00000
    C         -4.29745       -1.78579       -0.00000
    C         -5.54882       -2.43430       -0.00000
    H         -7.68820       -2.15296        0.00000
    H         -7.55879        0.31772        0.00000
    H         -5.35348        1.44963       -0.00000
    H         -3.26966        0.10734       -0.00000
    H         -3.37789       -2.35693       -0.00000
    N         -5.65342       -3.85046       -0.00000
    N         -4.64259       -4.58194       -0.00000
    C         -4.75058       -5.99808       -0.00000
    C         -6.00434       -6.64214       -0.00000
    C         -6.07567       -8.03881       -0.00000
    C         -4.90409       -8.80053       -0.00000
    C         -3.65828       -8.16721       -0.00000
    C         -3.58139       -6.77065       -0.00000
    H         -2.61200       -6.28795       -0.00000
    H         -6.92178       -6.06761       -0.00000
    H         -7.03986       -8.53061       -0.00000
    H         -4.96168       -9.88134       -0.00000
    H         -2.75170       -8.75849       -0.00000
    %ENDBLOCK POSITIONS_ABS

    FIX_ALL_CELL : True
    KPOINTS_MP_GRID : 1 1 1
```

We start by calculating the total DFT ground state energy as

```
    Final energy, E             =  -2597.665647686     eV
```

Now we reuse the calculated wavefunctions and switch to the DeltaSCF
calculation (param file above)

There are 68 valence electrons. Therefore, for this non-spin-polarized
system the HOMO orbital is orbital no. 34. The LUMO is orbital no. 35.

The first two excited states of azobenzene are known to be S1(n-\>pi\*)
and S2(pi-\>pi\*) transitions between the HOMO and LUMO and the HOMO-1
and the LUMO.

The corresponding constraint sequence in azo.deltascf for the S1
excitation is

```
#band  occ spin from_band to_band
%block deltascf_constraints
  34    0.5000  1   34   34       
  35    0.5000  1   35   35      
%endblock deltascf_constraints
```

------------------------------------------------------------------------

**WARNING**

:   When running non-spin-polarized calculations, orbital occupations
    range from 0 to 1. !!When running a spin-polarized calculation, they
    also range from 0 to 1, although they contain 0 to 2 electrons. In
    this (non-spin-polarized) case, if we want to transfer an electron
    from the HOMO(34) to LUMO(35) we need to enforce the occupation of
    both to be 0.50.

------------------------------------------------------------------------

Feel free to increase the print level with iprint to study the
output in more detail.

The corresponding total energy is

```
    Final energy, E             =  -2595.702720896     eV
```

This corresponds to an S1 excitation energy of 1.96 eV.

The constraint sequence for an S2 excitation is

```
#band  occ spin from_band to_band
%block deltascf_constraints
33    0.5000  1   33   33
35    0.5000  1   35   35      
%endblock deltascf_constraints
```

The resulting final energy is

```
    Final energy, E             =  -2594.762182241     eV
```

The corresponding S2 excitation energy is 2.90 eV.
