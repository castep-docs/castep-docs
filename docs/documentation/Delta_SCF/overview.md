# Overview

## Functionality

*    Calculate $\Delta$SCF-DFT excitation energies by changing band
    occupation - the "simple" method.
*   Constrain and occupy an orbital of a subsystem or reference system
     to resemble an electronic excitation via 'linear expansion mode' = le $\Delta$SCF-DFT
*   Put penalties onto orbitals of a subsystem in a DFT+U fashion
     (DFT+U(MO)). This can be done by enforcing idempotency (integer
     occupation) or by constrained DFT
*   Generate a projection of the orbital of a subsystem on the
     Density-of-States (DOS)
*   There is also a separate post-processing tool (MolPDOS) to generate the corresponding DOS
     from the projection information

## Prerequisites

*   The following applies to all modes, except the $\Delta$SCF-DFT
     mode. Nonetheless, this runmode requires a good understanding of
     its limitations.

*   The two systems should not be strongly geometrically or
     electronically mixed and a separation into general system and
     subsystem has to still be chemically reasonable. Otherwise this
     Ansatz breaks down. Ideally the difference can be seen as a weak
     perturbation. This applies for example for

     *   A molecule adsorbed at a metal surface with weak to medium hybridization, *e.g.* C~6~H~6~\@Au(111).
     *   A particle or molecule inserted into a porous nanostructure.
     *   The exact same system in another electronic state, *e.g.*
         groundstate *vs.* first excited state.

*    The wavefunction of the subsystem has to be calculated with
     **exactly** the same settings (K-points, spin-polarisation,
     cutoff, cell size) as the actual system. This introduces some
     artificial dispersion for gas-phase molecules, but if the cell is
     sufficiently large the effects should be small. In addition, this
     might be something desirable, for example when high coverage
     situations are investigated.

*   At the moment, the excitation constraints only work for
     ``metals_method=DM`` and ``spin_treatment=scalar`` or ``none``. 
    Currently, hybrid XC functionals are unsupported.

## General Use

The general use of $\Delta$SCF always involves the following steps:

1.   Define the base system and calculate the self consistent density and wave functions using a 
`task=single point energy`. The checkfile generated is then used as the base for the next steps.

2.  Define the system you want to study and add something similar to the following to 
the``<seed>.param`` file:

```
reuse               : <base>.check
calculate_deltascf  : true
deltascf_checkpoint : <base>.check
deltascf_mode       :  1
```

where `<base>` is the seedname of the base calculation in step 1. 

3. Decide on the type of $\Delta$SCF calculation. The allowed methods are:

```
deltascf_method : SIMPLE		or	deltascf_mode : 1
deltascf_method : DFT+U(MO)		or	deltascf_mode : 2
deltascf_method : LINEAR EXPANSTION	or	deltascf_mode : 3
```

For each method, the constraints need to be specified as follows:

SIMPLE
```
#band  occ spin from_band to_band
%block deltascf_constraints
5    0.5000  1   5   5
6    0.5000  1   6   6
%endblock deltascf_constraints
```

DFT+U(MO)
```
#band  occ spin U(eV) excite_band
%block deltascf_constraints
5    0.5000  1   +0.0   .true.
6    0.5000  1   +0.0   .true.
%endblock deltascf_constraints
```

LINEAR EXPANSION
```
#band  occ spin
%block deltascf_constraints
5    0.5000  1
6    0.5000  1
%endblock deltascf_constraints
```

The "occ" column is the constrained occupation required. In this instance, 1 electron is being 
raised from band 5 to band 6. The occupation is defined such that 0<=occ<=1 so if non-spin polarized 
calculation then occ=0.5 means 1 electron.


4.  You can now run the $\Delta$SCF calculation as any other CASTEP task.

5.  If you wish to, you can analyse the results using the MolPDOS post-processing tool which needs 
an additional ``<seed>.molpdos`` input file. Hence use  ``MolPDOS <seed>``
