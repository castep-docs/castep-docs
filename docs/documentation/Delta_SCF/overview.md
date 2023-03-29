# Overview

## Functionality

*    Calculate $\Delta$SCF-DFT excitation energies by changing band
    occupation
*   Constrain and occupy an orbital of a subsystem or reference system
     to resemble an electronic excitation - le $\Delta$DSCF-DFT
*   Put penalties onto orbitals of a subsystem in a DFT+U fashion
     (DFT+U(MO)). This can be done by enforcing idempotency (integer
     occupation) or by constrained DFT
*   Generate a projection of the orbital of a subsystem on the
     Density-of-States (DOS)
*   A post-processing tool (MolPDOS) generates the corresponding DOS
     out of the projection information

## Prerequisites

*   The following applies to all modes, except the $\Delta$SCF-DFT
     mode. Nonetheless, this runmode requires a good understanding of
     its limitations.

*   The two systems should not be strongly geometrically or
     electronically mixed and a separation into general system and
     subsystem has to still be chemically reasonable. Otherwise this
     Ansatz breaks down. Ideally the difference can be seen as a weak
     perturbation. This applies for example for

     *     A molecule adsorbed at a metal surface with weak to medium hybridization
           , *e.g.* C~6~H~6~\@Au(111).
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
     ``metals_method=DM`` and without non-local exchange, as well as
     ``spin_treatment=scalar`` or ``none``.

## General Use

The general use of this module always involves the following steps:

1.   Define the subsystem and calculate the self consistent density and wave functions.
     This has to be supplied to the actual calculation as checkfile.
     (not for class. $\Delta$SCF-DFT)

2.  in ``<seed>.param`` issue one of the following, depending on what
    :   you want to do

```
    %BLOCK DEVEL_CODE
      DeltaSCF           # starts a DeltaSCF or DFT+U(MO) calculation
      MolPDOS            # outputs MO projected DOS data
      DeltaSCF MolPDOS   # starts a DeltaSCF calculation and outputs MOPDOS
    %ENDBLOCK DEVEL_CODE
```

3.    Supply a ``<seed>.deltascf`` file that contains the necessary information for the DeltaSCF and/or MolPDOS run.

4.  Start a singlepoint calculation. Put task: singlepoint in the ``<seed>.param`` file and issue

    castep <seed>

5.  Only for MolPDOS calculations: Run the MolPDOS post-processing tool. This needs a ``<seed>.molpdos`` input file. Herefore you issue    ``MolPDOS <seed>``
