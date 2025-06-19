##Understanding the Output

In this chapter we shall briefly describe the output produced
during a CASTEP calculation. Only the level of detail printed
at iprint = 1 will be discussed.


##The .castep file

####Header

As well as the usual information printed at the top of the output file,
the molecular dynamics data specified in the parameters file is
presented.

```
 ************************ Molecular Dynamics Parameters ************************

 ensemble                                       : NPT
 variable cell method                           : fixed basis quality
 pressure                                       : see below
 temperature                                    :  293.0       K
 using                                          : Parrinello-Rahman barostat
 with characteristic cell time                  :  26.00       ps
 using                                          : Langevin thermostat
 with characteristic ionic time                 :  16.95       ps
 time step                                      : 0.2000E-02   ps
 number of MD steps                             :     500000
 using best-fit first order extrapolation for wavefunctions
 backup results every                           :          5   steps

 MD SCF energy / atom convergence tol.          : 0.1000E-04   eV
 MD SCF convergence tolerance window            :          3   cycles

 *******************************************************************************
```

This amount of information presented in this section will obviously vary
depending on the type of calculation being performed, but should
be self-explanatory.

####Initial cell

The information specified in the .cell file is then output. This will
include the ionic positions, any user specified velocities if present,
the usual pseudo-potential, k-point information, and details
of any constraints. The total energy of the initial cell is then
minimised, performing a finite basis set correction along the way
if appropriate.

The message

```
Starting MD
```

is then printed, and the MD calculation proper commences. As the
first time-step will require data on forces, stress (for variable cell
calculations) and energies, these are evaluated and printed at this point.

Forces are output in the following format, using the force unit
specified by the user, or the default of eV / Ang.

```
 ******************************** Forces *********************************
 *                                                                       *
 *                      Cartesian components (eV/A)                      *
 * --------------------------------------------------------------------- *
 *              x                    y                    z              *
 *                                                                       *
 * Si   1     -0.02632             -0.02632             -0.02632         *
 * Si   2     -0.02653             -0.02617             -0.02617         *
 * Si   3     -0.02617             -0.02617             -0.02653         *
 * Si   4     -0.02617             -0.02653             -0.02617         *
 * Si   5      0.00075              0.05164              0.00075         *
 * Si   6      0.05204              0.05204              0.05204         *
 * Si   7      0.05164              0.00075              0.00075         *
 * Si   8      0.00075              0.00075              0.05164         *
 *                                                                       *
 *************************************************************************
```

The stress tensor (if calculated) is output in the specified units of pressure,
along with the corresponding scalar $T=0$ pressure, i.e. one third of the trace of
the stress tensor.

```
 ***************** Stress Tensor *****************
 *                                               *
 *          Cartesian components (GPa)           *
 * --------------------------------------------- *
 *             x             y             z     *
 *                                               *
 *  x      0.009981      1.140649      1.140649  *
 *  y      1.140649      0.009981      1.140649  *
 *  z      1.140649      1.140649      0.009981  *
 *                                               *
 *  Pressure:   -0.0100                          *
 *                                               *
 *************************************************
```

The current time and MD energies are then printed in the
user specified energy units. Here potential energy
refers to the total configurational energy of electrons
plus ions obtained from the DFT calculation. Kinetic energy
is the classical kinetic energy of the ions. Total
energy refers to the sum of these two energies.

The enthalpy and the relevant Hamiltonian energy for the ensemble
as quoted in section [ensembles](basics.md#ensembles) is then printed.

The temperature is also output at this point. Note that this
is the ionic temperature only. If performing a calculation
with finite temperature electrons (i.e. EDFT) the electron
temperature may not be the same. Finally total pressure, i.e.
the trace of the stress tensor plus the kinetic (ideal gas) pressure
is printed in the user specified pressure units.

```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
x                                               MD Data:     x
x                                                            x
x              time :      0.000000                   ps     x
x                                                            x
x   Potential Energy:   -865.882944                   eV     x
x   Kinetic   Energy:      0.265113                   eV     x
x   Total     Energy:   -865.617832                   eV     x
x           Enthalpy:   -865.617735                   eV     x
x   Hamilt    Energy:   -865.617735                   eV     x
x                                                            x
x        Temperature:    293.000000                    K     x
x      T/=0 Pressure:      0.172231                  GPa     x
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

##Iteration

The MD simulation proper now begins.

```
=================================================================
 Starting MD iteration    1 ...
=================================================================
```

Following this message the current cell information on the new configuration is printed and
the energy is re-minimised to determine the new forces. The
MD step is then performed and the updated forces, stress and energy
information is printed in the same manner as above.

```
-----------------------------------------------------------------
 ... finished MD iteration    1
-----------------------------------------------------------------
```

The process repeats until the calculation is killed, or the specified number
of MD iterations is completed.

##The .md file

The .md file is provided as a single source for all the dynamical
data produced by a CASTEP calculation. In all cases, data is printed
in Hartree atomic units. Fortran formating data will be given here for
all entries in this file for those who wish to import it into their
own analysis codes.

The CASTEP default behaviour is to record every single configuration in the .md file. This can therefore grow to quite a
large size if doing a long MD run! The only exception to this, is if doing a non-DFT calculation, whereupon a sample of the
configurations are written if `md_sample_iter`>0, otherwise no configurations are written.

Note that unlike the .castep file, the .md file from a previous
calculation with the same seedname will be overwritten, unless
the new calculation is a continuation of the original.

####Header

At the top of every .md file a header is written as below. The total
length is four lines including blanks. The comments written are
taken from the cell/parameter files.

```
 BEGIN header

 This is 8 atom cubic Si cell
 END header
```

This is followed by a blank line. There is a single space at the start
of each non-blank line. This header is written once only.

####Time and Energy Data

The next entry will be the data for the first MD step. This begins with
the current time on the first line, followed by the Total, Hamiltonian, and
Kinetic energy on the second line with the label ``<-- E``.

```
               0.00000000E+000
              -3.18206146E+001     -3.18108683E+001      9.74270683E-003  <-- E
```

Formatting:

```
format(12x,es18.8e3)
format(9x,3(3x,es18.8e3),'  <-- E')
```

####Thermodynamic Data

The current temperature is then printed with the label ``<-- T``. If the output is from a variable cell
calculation, or ``calculate_stress`` has been explicitly set to true, the pressure
is also printed with the label ``<-- P``.

```
                9.27876841E-04                                            <-- T
                5.85402338E-06                                            <-- P
```

Formatting:

```
format(12x,es18.8,T73,   '  <-- T')
format(12x,es18.8,T73,   '  <-- P')
```

####Cell Data

For all calculations, the current matrix of cell vectors is printed with
the label ``<-- h`` Each row
gives the three Cartesian components of one of the cell vectors.

```
               1.01599045E+001      0.00000000E+000      0.00000000E+000  <-- h
               1.29430839E-017      1.01599045E+001      0.00000000E+000  <-- h
               1.29430839E-017      1.29430839E-017      1.01599045E+001  <-- h
```

Formatting:

```
format(9x,3(3x,es18.8e3),'  <-- h')
format(9x,3(3x,es18.8e3),'  <-- h')
format(9x,3(3x,es18.8e3),'  <-- h')
```

The remaining cell data is only printed for variable cell calculations, regardless
of the value of ``calculate_stress``. First the velocity of each cell vector
is printed with the label ``<-- hv``.

```
               2.80052926E-008     -1.42751448E-007     -1.35787248E-007  <-- hv
              -1.42751448E-007      2.76907508E-008     -1.44694219E-007  <-- hv
              -1.35787248E-007     -1.44694219E-007      2.71532850E-008  <-- hv
```

Formatting:

```
format(9x,3(3x,es18.8e3),'  <-- hv')
format(9x,3(3x,es18.8e3),'  <-- hv')
format(9x,3(3x,es18.8e3),'  <-- hv')
```

The full pressure tensor (including kinetic contributions) is then printed
with the label ``<-- S`` in a similar fashion.

```
              -6.21684372E-006      3.03062374E-005      3.23291890E-005  <-- S
               3.03062374E-005     -6.06171719E-006      3.31426773E-005  <-- S
               3.23291890E-005      3.31426773E-005     -5.79666096E-006  <-- S
```

Formatting:

```
format(9x,3(3x,es18.8e3),'  <-- S')
format(9x,3(3x,es18.8e3),'  <-- S')
format(9x,3(3x,es18.8e3),'  <-- S')
```

####Ionic Data

Data on the current ionic configuration is then printed. Atoms
are identified by their chemical symbol in the first column,
and number of the atom within the species in the second.

First the position vectors of all ions are printed with the
label ``<-- R``.

```
 Si     1      1.04834750E-002      1.15560090E-002      7.82230990E-003  <-- R
 Si     2     -3.20400394E-003      5.07172565E+000      5.10986361E+000  <-- R
 Si     3      5.07271954E+000      5.11656710E+000     -2.45225140E-003  <-- R
 Si     4      5.10789066E+000     -2.63240242E-002      5.09753015E+000  <-- R
 Si     5      7.57309188E+000      2.52845762E+000      7.57612741E+000  <-- R
 Si     6      2.55271297E+000      2.54057876E+000      2.53924276E+000  <-- R
 Si     7      2.53422324E+000      7.64091983E+000      7.62428191E+000  <-- R
 Si     8      7.63167143E+000      7.59610368E+000      2.52717191E+000  <-- R
```

Formatting (for each atom):

```
format(1x,a3,1x,i4,3(3x,es18.8e3),'  <-- R')
```

Velocities are then printed in a similar fashion.

```
 Si     1      5.77278549E-005      7.23673746E-005      4.30349159E-005  <-- V
 Si     2     -1.72415752E-005     -5.23270551E-005      1.75385181E-004  <-- V
 Si     3     -4.17085102E-005      2.14539848E-004     -1.78769096E-005  <-- V
 Si     4      1.58756714E-004     -1.60916056E-004      9.49147966E-005  <-- V
 Si     5     -2.70431102E-004     -7.18757382E-005     -2.43440176E-004  <-- V
 Si     6      7.51663795E-005      8.70332331E-008     -8.82271461E-006  <-- V
 Si     7     -4.19898677E-005      1.31687892E-004      3.60873179E-005  <-- V
 Si     8      7.97201068E-005     -1.33563298E-004     -7.92824105E-005  <-- V
```

Formatting (for each atom):

```
format(1x,a3,1x,i4,3(3x,es18.8e3),'  <-- V')
```

Finally forces are printed.

```
Si     1     -4.23569381E-003      2.52214252E-003     -2.46018145E-003  <-- F
Si     2      3.06338418E-003     -2.16206923E-003     -5.29928454E-003  <-- F
Si     3      7.37259995E-004     -4.73479365E-003     -2.20030945E-003  <-- F
Si     4     -6.89050954E-003     -2.25153379E-003     -8.37626756E-003  <-- F
Si     5      4.53551291E-003      3.34757083E-003      1.02791157E-002  <-- F
Si     6      2.06737343E-003      2.05175887E-003      2.70990363E-003  <-- F
Si     7     -1.41457164E-003     -9.15433604E-004      1.54850432E-003  <-- F
Si     8      2.13724448E-003      2.14235805E-003      3.79851935E-003  <-- F
```

Formatting (for each atom):

```
format(1x,a3,1x,i4,3(3x,es18.8e3),'  <-- F')
```

A blank line is then printed, and the process repeats with the data from the next
time-step.

##The .hug file

If you are using the Hugoniostat predictor-corrector method to generate a Hugoniot curve, each different state point
generated has a different compression etc. This is summarized in the `.hug` file as follows:

```
  0.990000000000       36.31531287        0.41888602        0.15771481  <-- cTPE
  0.943272613764       40.07750465        0.63662992        1.62298398  <-- cTPE
  0.865294155381       58.07130958        1.30346964        6.92736406  <-- cTPE
```

The 4 data fields are:

c - the ratio of the compressed to original cell vectors

T - the temperature (in user units) - calculated as a time average of the instantaneous temperature of the configurations
at this compression

P - the pressure (in user units) - calculated as a time average

E - the energy (in user units) - calculated as a time average
