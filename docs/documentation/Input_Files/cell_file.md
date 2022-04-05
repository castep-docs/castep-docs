This is a detailed description of options for CASTEP's cell file. See the [basic cell file page](/documentation/Groundstate/basic_cell_file) for an overview. This page has the most frequently-used cell file options, but for a full set use [CASTEP's built-in help](/documentation/Getting_Started/built_in_help). There is also a [concise table of cell keywords](cell_keywords.md).

The cell file is one of CASTEP's two main input files. It contains all of the information about the crystal lattice and the atomic positions, as well as additional information such as Brillouin zone sampling ('k-points'), pseudopotentials, cell symmetry, external pressure, constraints on motion of the atoms or cell, and atomic properties such as the mass of each species.

The file itself is a free-format keyword-driven text file, consisting of keywords and blocks of information. These may be given in any order, with blocks indicated by the special `%block` and `%endblock` markers. Most of the keywords and blocks are optional, but CASTEP *requires* two block entries: a block to specify the lattice, and another to specify the atomic elements and positions within the cell.

At the very least, the cell lattice vectors and ionic positions must
be specified. Reasonable defaults are chosen for anything else not
specified.

For the purposes of the following definitions, all
variables represented by $R$ are defined to be real numbers, those
represented by $I$ are defined to be integers and those represented by
$C$ are characters.

### Cell Lattice Vectors ###

The cell lattice vectors may be specified in Cartesian coordinates
or in terms of the lattice vector magnitudes and the angles between 
them ($a, b, c, \alpha, \beta, \gamma$). Only one of `LATTICE_CART`
and `LATTICE_ABC` may occur in a cell definition file.

The definitions of these keywords are as follows:

```
%BLOCK LATTICE_CART
[units]
a_x  a_y  a_z  
b_x  b_y  b_z 
c_x  c_y  c_z
%ENDBLOCK LATTICE_CART
```

Here `a_x` is the x-component of the first lattice vector, $\mathbf{a}$, 
$b_y$ is the y-component of the second lattice vector, $\mathbf{b}$, etc.

`[units]` specifies the units in which the lattice vectors are
defined. If not present, the default is Å.

```
%BLOCK LATTICE_ABC
[units]
a b c
alpha beta gamma
%ENDBLOCK LATTICE_ABC
```

Here `a` is the value of the lattice constant $\vert\mathbf{a}\vert$, `gamma` is the value of the cell angle $\gamma$ (in degrees) etc. If the lattice is specified in this manner, the absolute orientation is arbitrary. In this case the orientation is defined by applying the following constraints:

- $\mathbf{a}$ lies along the x-axis
- $\mathbf{b}$ lies in the xy plane
- $\mathbf{c}$ forms a right-handed set with $\mathbf{a}$ and $\mathbf{b}$

`[units]` specifies the units in which the lattice vector magnitudes are defined. If not present, the default is Å. Angles should be specified in degrees.


### Ionic Positions ###

The ionic positions may be specified in fractional coordinates relative
to the lattice vectors of the unit cell, or in absolute coordinates.
Only one of `POSITIONS_FRAC` and `POSITIONS_ABS` may occur in a cell definition 
file.

```
%BLOCK POSITIONS_FRAC
CCC_1  R_{1i}  R_{1j}  R_{1k}  [SPIN=s_1]  
CCC_2  R_{2i}  R_{2j}  R_{2k}  [SPIN=s_2]
...
%ENDBLOCK END POSITIONS_FRAC
```

The first entry on a line is the symbol of the species (chemical element). Alternatively, the atomic number may be given instead, in which case CASTEP will be look up for chemical symbol. A symbol can have a maximum of three
characters. The first alphabetical characters identify the element,
from which default values for atomic mass etc. 

The next three entries on a line in POSITIONS_FRAC are real numbers
representing the position of the ion in fractions of the unit cell
lattice vectors.

If the optional flag `SPIN` is present on a line, this sets the
spin polarisation ( $N^\uparrow-N^\downarrow$) of the
atom for initialisation of the spin density; for non-collinear spin calculations, the vector spin is specified as three numbers. If this flag is not
present a non-spin polarised state will be assumed.

```
%BLOCK POSITIONS_ABS
[units]
CCC_1  R_{1i}  R_{1j}  R_{1k}  [SPIN=s_1]  
CCC_2  R_{2i}  R_{2j}  R_{2k}  [SPIN=s_2]
...
%ENDBLOCK POSITIONS_ABS
```

The first entry on a line is the symbol or atomic number of the ionic
species, as for `POSITIONS_FRAC`. The next three entries are real
numbers representing the position of the ion in Cartesian coordinates.

`[units]` specifies the units in which the positions are defined. If not present, the default is Å.

The optional flag `SPIN` is defined above under `POSITIONS_FRAC`.

### Brillouin Zone Sampling (k-points) ###

(N.B. in the following section the keywords with the prefixes
`KPOINT_` and `KPOINTS_` are synonymous. `KPOINT_` is
the preferred usage.)

The k-points at which the Brillouin zone is to be sampled during a
self consistent calculation to find the electronic ground state may be
defined either by specifying a list of k-points or a Monkhorst-Pack
grid in terms of the dimensions of the k-point mesh or a minimum
k-point density. The origin of the Monkhorst-Pack grid may be
offset by a vector from the origin of the Brillouin zone.

If no k-points are specified, the default will be a Monkhorst-Pack
grid with a maximum spacing of 0.1Å$^{-1}$ and no offset of the 
origin.

The `KPOINT_LIST`, `KPOINT_MP_GRID` and `KPOINT_MP_SPACING`
keywords are mutually exclusive. `KPOINT_MP_OFFSET` may be specified
in combination with either `KPOINT_MP_GRID` or `KPOINT_MP_SPACING`.

```
%BLOCK KPOINT_LIST
\begin{array}{cccc}
R_{1i}  R_{1j}  R_{1k}  R_{1w}
R_{2i}  R_{2j}  R_{2k}  R_{2w}
...
%ENDBLOCK KPOINT_LIST
```

The first three entries on a line are the fractional positions of the
k-point relative to the reciprocal space lattice vectors. The final entry
on a line is the weight of the k-point relative to the others specified.
The sum of the weights must be equal to 1.

```
KPOINT_MP_GRID I_i I_j I_k
```

This specifies the dimensions of the Monkhorst-Pack grid requested in
the directions of the reciprocal space lattice vectors. The generated
grid will be $I_i\times I_j\times I_k$; any symmetries generated (or
supplied) will be used to reduce this number, when computing the
irreducible wedge.

```
KPOINT_MP_SPACING R [units]
```

The single entry is the maximum distance between k-points on the
Monkhorst-Pack grid. The dimensions of the grid will be chosen such
that the maximum separation of k-points is less than this.

`[units]` specifies the units in which the k-point spacing is
defined, although *note that the actual units used are $2\pi$ units*. If not present, the default is `ang-1`, such that the spacing is in $2\pi Å^{-1}$.

```
KPOINT_MP_OFFSET R_i R_j R_k
```

This specifies the offset of the Monkhorst-Pack grid with respect to
the origin of the Brillouin zone. The three entries are the offset in 
fractional coordinates relative to the reciprocal lattice vectors.

The k-point set for performing spectral calculations
can be specified in the same manner, using version of the keywords
above with `SPECTRAL_` prepended. The same restrictions regarding
mutually exclusive keywords apply.

For a non-self-consistent spectral calculation, the k-points may
be defined along a path through reciprocal space or a list of k-points. 

```
%BLOCK SPECTRAL_KPOINT_PATH
R_{1i} R_{1j} R_{1k} 
R_{2i} R_{2j} R_{2k} 
...
%ENDBLOCK SPECTRAL_KPOINT_PATH
```

The three numbers on each line are the fractional positions of the
k-point relative to the reciprocal space lattice vectors. The k-points
define a continuous sequence of straight line segments, unless the
keyword `BREAK` appears on a separate line within the sequence of
k-points. In this case the continuous path will end at the k-point
immediately preceding the `BREAK` keyword and resume at the k-point
immediately following. The path will be open *unless the first and
last point in the list are identical*.

The maximum spacing of the points sampled along each line segment is defined by the keyword
`SPECTRAL_KPOINT_PATH_SPACING` (default value $0.1 \times 2\pi$Å$^{-1}$). If necessary,
the actual spacing used may be smaller than this in order to ensure
that the length of the line segment is an integer multiple of the
spacing between points on that segment.

Alternatively, the k-point set for performing a band structure
calculation can be specified in the same manner as the main k-point
set, using version of the keywords above with BS_ prepended. The same
restrictions regarding mutually exclusive keywords apply. In this
case, the k-point weight in `SPECTRAL_KPOINT_LIST` is optional. If
omitted, the weights for each k-point are assumed to be equal.

For a phonon spectrum calculation, the k-points may be defined along a
path through reciprocal space or a list of k-points, in the same
manner as for a spectral calculation. The corresponding keywords
are identical to those for the band structure specification with the
initial `SPECTRAL_` replaced by `PHONON_`, e.g. `PHONON_KPOINT_PATH`,
`PHONON_KPOINT_PATH_SPACING` and `PHONON_KPOINT_LIST`. The same
restrictions regarding mutually exclusive keywords apply.

The block keyword `PHONON_GAMMA_DIRECTIONS` specifies the directions
in which the gamma point will be approached when calculating the
non-analytic terms of the LO/TO splitting. Each line in this block
will consist of a 3-vector specifying a direction in the basis of
reciprocal lattice vectors. If this keyword is not present, the
default will be a single vector determined as follows:

1. If the gamma point is $q_i = 0$ and there is a successor kpoint
$q_{i+1}$ in the list, then it is $q_{i+1}$.
2. Otherwise if the gamma point is $q_i =0$ and there is a
predecessor kpoint $q_{i-1}$ in the list then it is $q_{i-1}$.
3. Otherwise (i.e. a Gamma point only calculation) the a-axis of
the reciprocal cell.

For backwards compatibility the keywords beginning `BS_` and `OPTICS_` are
synonyms for SPECTRAL_KPOINT_ and similarly those beginning.

### Cell Symmetry ###

If no symmetry is specified in the cell definition file,
the default is for no symmetry to be applied.

```
SYMMETRY_GENERATE
```

If this keyword is present in the cell, the highest symmetry group
that applies to the structure of the cell will be found and the
corresponding symmetry operations generated.

```
SYMMETRY_TOL R [units]
```

This parameter is the tolerance within which symmetry will be
considered to be satisfied.  If an ion is found within this distance
of its symmetric position, the symmetry will be considered to be
satisfied.

`[units]` specifies the units in which the tolerance is
defined. If not present, the default is Å.

Alternatively, the symmetry operations may be provided directly in a
`SYMMETRY_OPS` block. The symmetry of the cell is represented as a
series of symmetry operations under which the unit cell is
invariant. Each operation is represented as a $3\times 3$ array.

```
%BLOCK SYMMETRY_OPS
R_{11}   R_{21}   R_{31} 
R_{12}   R_{22}   R_{32} 
R_{13}   R_{23}   R_{33} 
T_1      T_2      T_3

R_{11}   R_{21}   R_{31} 
R_{12}   R_{22}   R_{32} 
R_{13}   R_{23}   R_{33} 
T_1      T_2      T_3
...
%ENDBLOCK SYMMETRY_OPS
```

Each of the first three lines contains 3 entries representing a row of 
a $3\times3$ array. These represent one symmetry rotation. The three 
entries on the following line contain the translation associated with 
this rotation.


### Constraints ###

The movement of ions or the unit cell during a relaxation or molecular
dynamics run may be constrained.

The constraints on the ionic motion may by specified as a set of
linear constraints. Each constraint is specified as a series of
coefficients $a_{ijk}$ such that:
$$
\sum_{k=1}^{\tt N_\mathrm{species}} \quad \sum_{j=1}^{\mathrm{N_\mathrm{ions}}(k)}
\quad \sum_{i=1}^{3} a_{ijk}\ \verb#ionic_positions(i,j,k)# = constant
$$
where $\mathrm{N_\mathrm{ions}}(k)$ is the number of ions in species $k$.

The change in the shape of the unit cell may also be constrained
using the keyword `CELL_CONSTRAINTS`.

The special case of constraining the centre of mass of the ions to
remain fixed is supported by a logical keyword `FIX_COM`.  Also all
ionic positions or cell parameters may be fixed by specifying the
keywords `FIX_ALL_IONS` or `FIX_ALL_CELL` to be `TRUE` respectively.

If no ionic or cell constraints are specified in the cell definition file, 
the default is to fix the centre of mass.

```
%BLOCK IONIC_CONSTRAINTS
I_1  CCC_{1s}   I_{1s}   I_{n1}   R_{1i}   R_{1j}   R_{1k} 
I_2  CCC_{2s}   I_{2s}   I_{n2}   R_{2i}   R_{2j}   R_{2k} 
...
%ENDBLOCK IONIC_CONSTRAINTS
```

The first element on each line is an integer specifying the number of the
constraint being specified. The second entry is either the symbol or
atomic number of the species of the ion to which this constraint applies.
The third element is the number of the ion within the species. The ordering
of the ions in a species is the order in which they appear in the
`POSITIONS_FRAC` or `POSITIONS_ABS` block in the cell definition file.
The final three numbers are real numbers representing the coefficients
of the Cartesian coordinates of the ionic position in the constraint
sum. All coefficients in the sum not explicitly specified will be zero.

On reading this data, the matrix of ionic constraints will be 
orthogonalised.

```
%BLOCK CELL_CONSTRAINTS
I_a      I_b      I_c
I_alpha  I_beta   I_gamma
%ENDBLOCK CELL_CONSTRAINTS
```

The first three entries relate to the magnitude of the three
lattice vectors $a,b,c$ and the second set of three entries
to the angles $\alpha, \beta, \gamma$.

If the value of the entry corresponding to a magnitude or angle is
zero, this quantity will remain fixed. If two or three entries
contain the same integer, the corresponding quantities will be
constrained to have the same value. If a positive integer greater than 
0 occurs in entries 1 through 3 the same integer cannot occur in 
entries 4 through 6 as this would imply that a vector length
and angle must have the same value.

### Species Characteristics ###

The mass of a species, the pseudopotential which represents the ion
and the size of the LCAO basis set used for population anslsyis may be
specified in the cell definition file.

```
%BLOCK SPECIES_MASS
[units]
CCC_1   I_1   R_1 
CCC_2   I_2   R_2 
...
%ENDBLOCK SPECIES_MASS
```

`[units]` specifies the units in which the masses are
defined. If not present, the default is atomic mass units.

The first entry on a line is the symbol or atomic number of the
species.  This must correspond with the species symbol or atomic
number of the species in the `POSITIONS_FRAC` or `POSITIONS_ABS`
block. The second entry on each line is the mass of that species. Not
all species need appear in the `SPECIES_MASS` block, any not present
will assume the default mass for that species. If the initial
alphabetical symbol specified for a species is not a standard element
symbol in the periodic table, the mass of the species must be
specified.

```
%BLOCK SPECIES_POT
CCC_1   I_1   <filename> 
CCC_2   I_2   <filename> 
...
%ENDBLOCK SPECIES_POT
```

The first entry on a line is the symbol or atomic number of the
species.  This must correspond with the species symbol or atomic
number of the species in the `POSITIONS_FRAC` or `POSITIONS_ABS`
block. The second entry on each line is the filename of the file
containing the definition of the pseudopotential representing the
ionic species. The file to which this refers may be a definition of
the parameters of the pseudopotential which is to be generated at
runtime, or an old-style pseudopotential definition containing the
data for the pseudopotential. 

Not all species need appear in the `SPECIES_POT` block. If a
pseudopotential is not specified, the default pseudopotential
parameters will be used to generate a pseudopotential for the element
specified. If the initial alphabetical characters of a species label
is not a standard element symbol in the periodic table, the potential
for the species must be specified.

The charge on the ion for each species will be derived from
the pseudopotential corresponding to that ion.

```
%BLOCK SPECIES_LCAO_STATES
CCC_1   I_1   I_{B1} 
CCC_2   I_2   I_{B2} 
...
%ENDBLOCK SPECIES_LCAO_STATES
```

The first entry on a line is the symbol or atomic number of the
species.  This must correspond with the species symbol or atomic
number of the species in the `POSITIONS_FRAC` or `POSITIONS_ABS`
block. The second number is the number of angular momentum channels to
use in the LCAO basis set for the species when performing population
analysis. For example, to use the 2s and 2p states for C (The 1s state
is a core state) this should be 2. By default, the number of states
will be the appropriate number to complete the valence shell to the
next noble gas. If shallow core states are excluded from a
pseudopotential, the value of `SPECIES_LCAO_STATES` for that species
should be included in the cell file to ensure a meaningful basis set
is used.

### External Pressure ###

An external pressure may be applied to the unit cell by specifying
a pressure tensor.

```
%BLOCK EXTERNAL_PRESSURE
[units]
R_{xx}   R_{xy}  R_{xz} 
         R_{yy}  R_{yz} 
                 R_{zz} 
%ENDBLOCK EXTERNAL_PRESSURE
```

`[units]` specifies the units in which the pressure is
defined. If not present, the default is GPa.

Entry $R_{xx}$ is the $xx$-component of the pressure, $R_{xy}$ the
$xy$-component etc.

The default is to apply no external pressure.

### Ionic Velocities ###

The initial ionic velocities may be specified in Cartesian coordinates
in a cell definition file.

```
%BLOCK IONIC_VELOCITIES
[units]
CCC_1 V_{1x}  V_{1y}  V_{1z} 
CCC_2 V_{2x}  V_{2y}  V_{2z} 
...
%ENDBLOCK IONIC_VELOCITIES
```

The first entry on a line is the chemical symbol (or atomic number) of the ionic
species. The correct symbol will be looked up for the atomic species
if the atomic number is specified. A symbol can have a maximum of three
characters. The next three entries are real numbers representing the
velocity of the ion in Cartesian coordinates.

`[units]` specifies the units in which the positions are
defined. If not present, the default is Å/ps.

If this keyword is not present and a molecular dynamics calculation is
performed, the ionic velocities will be randomly initialised with the
appropriate temperature.

