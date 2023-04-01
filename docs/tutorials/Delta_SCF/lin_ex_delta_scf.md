
## Electronic excitations of NO on Ni(001)

ATTENTION: These calculations are done using standard on-the-fly
pseudopotentials from CASTEP-6.0.1

For this example we calculate a charge neutral HOMO-\>LUMO excitation
and a charge transfer excitation between a nickel substrate and a NO
molecule

In the following, the required input files are:

no-on-ni001.param, no-on-ni001.cell, 
gasphase.cell, gasphase.param, gasphase.check

*no-on-ni001.param*

```
    #reuse: default
    calculate_deltascf  : true
    deltascf_method     : linear expansion
    deltascf_checkpoint : gasphase.check
    
#band  occ spin
%block deltascf_constraints
5    0.0000  1
6    1.0000  2
%endblock deltascf_constraints
 
    task: SinglePoint

    spin_polarized : True
    cut_off_energy : 400.0
    elec_energy_tol : 1e-07
    fix_occupancy : False
    iprint : 1
    max_scf_cycles : 200
    metals_method : dm
    mixing_scheme : Pulay
    mix_history_length : 7
    nextra_bands : 50
    num_dump_cycles : 0
    opt_strategy_bias : 3
    smearing_scheme : Gaussian
    smearing_width : 0.15
    xc_functional : RPBE
```

*no-on-ni001.cell*

```
    %BLOCK LATTICE_CART
        3.5240000000 0.0000000000 0.0000000000
        0.0000000000 3.5240000000 0.0000000000
        0.0000000000 0.0000000000 23.0000000000
    %ENDBLOCK LATTICE_CART

    %BLOCK POSITIONS_ABS
        Ni 1.762000 0.000000 1.762000
        Ni 0.000000 1.762000 1.762000
        Ni 0.000000 0.000000 3.524000
        Ni 1.762000 1.762000 3.524000
        Ni 1.762000 0.000000 5.286000
        Ni 0.000000 1.762000 5.286000
        N  1.7620  0.0000  7.0196
        O  1.7620 -0.0000  8.1902
    %ENDBLOCK POSITIONS_ABS

    %BLOCK IONIC_CONSTRAINTS
         1  Ni   1   1 0 0
         2  Ni   1   0 1 0
         3  Ni   1   0 0 1
         4  Ni   2   1 0 0
         5  Ni   2   0 1 0
         6  Ni   2   0 0 1
         7  Ni   3   1 0 0
         8  Ni   3   0 1 0
         9  Ni   3   0 0 1
        10  Ni   4   1 0 0
        11  Ni   4   0 1 0
        12  Ni   4   0 0 1
        13  Ni   5   1 0 0
        14  Ni   5   0 1 0
        15  Ni   5   0 0 1
        16  Ni   6   1 0 0
        17  Ni   6   0 1 0
        18  Ni   6   0 0 1
    %ENDBLOCK IONIC_CONSTRAINTS

    FIX_ALL_CELL : True
    KPOINTS_MP_GRID : 2 2 1
    KPOINTS_MP_OFFSET : 0.25 0.25 0.25
```

*gasphase.cell*

```
    %BLOCK LATTICE_CART
        3.5240000000 0.0000000000 0.0000000000
        0.0000000000 3.5240000000 0.0000000000
        0.0000000000 0.0000000000 23.0000000000
    %ENDBLOCK LATTICE_CART

    %BLOCK POSITIONS_ABS
        N  1.7620  0.0000  7.0196
        O  1.7620 -0.0000  8.1902
    %ENDBLOCK POSITIONS_ABS

    FIX_ALL_CELL : True
    KPOINTS_MP_GRID : 2 2 1
    KPOINTS_MP_OFFSET : 0.25 0.25 0.25
```

*gasphase.param*

```
    task: SinglePoint

    spin_polarized : True
    cut_off_energy : 400.0
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
    xc_functional : RPBE
```

The workflow is as follows:

-   Calculate reference states (gasphase.check). These can be ground
    state Kohn-Sham states or themselves excited KS states
-   Calculate the ground state of NO on Ni(001)


```
    Final energy, E             =  -7867.950085034     eV
```

-   Calculate the leDeltaSCF excitation

We calculate a charge transfer from the molecule to the surface by
removing an electron from the HOMO in the majority spin channel

```
#band  occ spin
%block deltascf_constraints
5    0.0000  1
%endblock deltascf_constraints
 
```

------------------------------------------------------------------------

**WARNING**

:   A sufficient number of virtual states in the calculation, controlled
    by the keyword nextra_states, is very important. The more virtual
    states are used explicitly, the more complete is the projection onto
    the space of KS states. Sometimes states are almost degenerate and
    we also need to constrain the occupation of the other state to
    ensure that the population doesn\'t just switch between the two. In
    some cases, convergence can be very slow and a large number of SCF
    steps is necessary.

------------------------------------------------------------------------

The resulting excitation energy is 0.46 eV.

```
    Final energy, E             =  -7867.487338823     eV
```

We can calculate an intramolecular triplet excitation from HOMO to LUMO
with the following constraint sequence in \<seed\>.deltascf. This
excites 1 electron from the HOMO in the majority spin channel to the
LUMO in the minority spin channel.

```
#band  occ spin
%block deltascf_constraints
5     0.0000  1
6     1.0000  2
%endblock deltascf_constraints
```

The resulting excitation energy is 9.17 eV.

```
    Final energy, E             =  -7858.779610351     eV
```
