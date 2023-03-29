# Molecular Orbital (MO) projected Density-of-States - MolPDOS

## Basics

This mode allows to generate projections and pDOS plots with respect to
any molecular orbital (MO). To run it one has to add following keyword
to ``<seed>.param``

    %BLOCK DEVEL_CODE
      MolPDOS
    %ENDBLOCK DEVEL_CODE

The projection data is produced by CASTEP after the SCF task and is
written to files called ``<seed>.[molpdos_state]()<#>_<#>``, where
the two numbers correspond to the number and the spin of the specified
reference orbital from the reference checkfile.

At the end of the ``<seed>.castep`` file the projection is commented in
the following way:

    Successfully read .deltascf file!
                  Calculating MolPDOS weights
    +-------------------INPUT PARAMETERS-------------------+
    Taking band from model    gasphase
    MolPDOS state               1
    MolPDOS band  nr.           4
    MolPDOS band has spin      1
    MolPDOS state               2
    MolPDOS band  nr.           5
    MolPDOS band has spin      1
    MolPDOS state               3
    MolPDOS band  nr.           6
    MolPDOS band has spin      1
    MolPDOS state               4
    MolPDOS band  nr.           4
    MolPDOS band has spin      2
    MolPDOS state               5
    MolPDOS band  nr.           5
    MolPDOS band has spin      2
    MolPDOS state               6
    MolPDOS band  nr.           6
    MolPDOS band has spin      2
    |DeltaSCF| Reading projection data from model file gs.check
    Writing file   no.molpdos_state_4_1
    Writing file   no.molpdos_state_5_1
    Writing file   no.molpdos_state_6_1
    Writing file   no.molpdos_state_4_2
    Writing file   no.molpdos_state_5_2
    Writing file   no.molpdos_state_6_2

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
``<#>_spin<#>_<output_filename)``. The keywords for the .deltascf and
.molpdos files can be found below.

### Keywords allowed in <seed>.deltascf

In the .deltascf and .molpdos files, the keyword title plus colon takes
exactly 23 columns (A20,3X). The keyword content starts after that.
Lines with ``#`` are ignored.



| keyword           | multiple appearance | arguments and FORTRAN format    |
| ------------------ | ---------- | --------------------------------------- |
| deltascf_iprint  | > No     | <integer I\>                         |
| molpdos_state    | > Yes    | <# of ref. state I6\>1X<spin of ref. state I6\>     |
| deltascf_file    | > No     | <string len=40 filename without  .check\>     |

Example .deltascf file:

    deltascf_iprint      :  2
    deltascf_file        :  gasphase.check
    molpdos_state        :  31     1
    molpdos_state        :  33     1
    molpdos_state        :  35     1
    molpdos_state        :  36     2

In this example, 4 different MOs with the indices 31, 33, 35, and 36
contained in the wavefunction file gasphase.check are projected from the
wavefunction of the current system.

### Keywords allowed in <seed\>.molpdos

| keyword           | multiple appearance | arguments and FORTRAN format          |
| ------------------ | ---------- | --------------------------------------- |
| molpdos_state    | > Yes    | <# of ref. state I6\>1X<spin of ef. state I6\>    |
| molpdos_bin_with | > No     | real number, default=0.01             |
| molpdos_smearing | > No     | real number, default=0.05             |
| molpdos_scaling  | > No     | real number, default=1.0, scales  MolPDOSes     |
| no_fermi_shift   | > No     | no argument, logical, removes  fermishift       |
| ax is_energy_margin         | > No     | real in eV default=0.0eV              |
| output_filename  | > No     | <string len=40 filename\>            |

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
