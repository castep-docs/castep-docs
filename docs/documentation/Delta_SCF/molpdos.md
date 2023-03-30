# Molecular Orbital (MO) projected Density-of-States - MolPDOS

## Basics

This mode allows to generate projections and pDOS plots with respect to
any molecular orbital (MO). To run it one just has to add `calculate_modos=true` keyword
to `<seed>.param` file.

The projection data is produced by CASTEP after the SCF task and is
written to files called ``<seed>.modos_state_<#>_<#>``, where
the two numbers correspond to the number and the spin of the specified
reference orbital from the reference checkfile.

At the end of the ``<seed>.castep`` file the projection is commented in
the following way:

```
             Calculating MODOS weights               
 +-------------------INPUT PARAMETERS-------------------+
Taking band from model   N2-base.check                                                                                                                                                                                                                                                   
  MODOS state               1
  MODOS band  nr.           5
  MODOS band has spin       1
  MODOS state               2
  MODOS band  nr.           6
  MODOS band has spin       1
|DeltaSCF| Population of state:     5     1   1.000000
|DeltaSCF| Population of state:     6     1   0.000000
 Writing file   N2-modos.modos_state_5_1
 Writing file   N2-modos.modos_state_6_1
```

These files, together with the ``<seed>.bands`` file can be post-processed
with the MolPDOS program with the following command

    MolPDOS <seed>

This will write output in the ``<seed>.castep`` with following header.

    #############################################
    #                                           #
    #                                           #
    #    MolPDOS  -CASTEP Post-processor        #
    #                                           #
    #       by   R. J. Maurer                   #
    #                                           #
    #                                           #
    #############################################

In addition it will write files for the total DOS (Total-DOS.dat), for
the two spin channels if the calculation was spin polarized
(Total-DOS_spin1.dat, Total-DOS_spin2.dat), and for the MolPDOS (
``<#>_spin<#>_<output_filename)``. 

The keywords for the `.molpdos` input file can be found below.

### Keywords allowed in <seed>.molpdos

In the .molpdos files, the keyword title plus colon takes
exactly 23 columns (A20,3X). The keyword content starts after that.
Lines with ``#`` are ignored.


| keyword           | multiple appearance | arguments and FORTRAN format          |
| ------------------ | ---------- | --------------------------------------- |
| molpdos_state    |  Yes    | <# of ref. state I6\>1X<spin of ef. state I6\>    |
| molpdos_bin_with |  No     | real number, default=0.01             |
| molpdos_smearing |  No     | real number, default=0.05             |
| molpdos_scaling  |  No     | real number, default=1.0, scales  MolPDOSes     |
| no_fermi_shift   |  No     | no argument, logical, removes  fermishift       |
| ax is_energy_margin        |  No     | real in eV default=0.0eV              |
| output_filename  |  No     | <string len=40 filename\>            |

Example .molpdos file:

    molpdos_state        :  34     1
    molpdos_state        :  35     1
    molpdos_state        :  36     1
    molpdos_state        :  33     1
    molpdos_bin_width    :  0.02
    molpdos_smearing     :  0.05
    molpdos_scaling      :  1.00
    axis_energy_margin   :  2.00
    output_filename      :  MolPDOS.dat
