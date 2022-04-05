This is a basic overview of the cell file. See the [full cell file page](/documentation/Input_Files/cell_file) for more details.

The cell file is one of CASTEP's two main input files. It contains all of the information about the crystal lattice and the atomic positions, as well as additional information such as Brillouin zone sampling ('k-points'), pseudopotentials, and atomic properties. 

The file itself is a free-format keyword-driven text file, consisting of keywords and blocks of information. These may be given in any order, with blocks indicated by the special `%block` and `%endblock` markers. Most of the keywords and blocks are optional, but CASTEP *requires* two block entries: a block to specify the lattice, and another to specify the atomic elements and positions within the cell.

## Lattice ##

There are two main ways to set the crystal lattice in the cell file. The `lattice_abc` block specifies the lattice constants in terms of the lengths of the lattice vectors ($\mathbf{a}$, $\mathbf{b}$ and $\mathbf{c}$) and angles (alpha, beta and gamma):
```
%block lattice_abc
a b c
alpha beta gamma
%endblock lattice_abc
```
This doesn't specify how the cell is to be oriented in the Cartesian coordinate system, so CASTEP uses the convention that $\mathbf{a}$ is along the x-axis, and $\mathbf{b}$ is in the x-y plane.

Alternatively, you can specify the lattice vectors $\mathbf{a}$, $\mathbf{b}$ and $\mathbf{c}$ directly in terms of their Cartesian components, using the lattice_cart block. Note that these are specified as *row* vectors:
```
%block lattice_cart
[unit]
a_x  a_y  a_z 
b_x  b_y  b_z 
c_x  c_y  c_z 
%endblock lattice_cart
```
The first line is optional, and specifies a length unit; the default is `ang`, meaning Angstroms.


## Atomic positions ##

The positions of the atoms within a cell may be specified in either fractional coordinates (i.e. the coordinates in the basis of the lattice vectors) or Cartesian coordinates:
```
%block positions_frac
symbol  u v w
%endblock positions_frac
```
where `symbol` is the chemical symbol for the atomic element, and `u`, `v` and `w` are the fractional components of the lattice vectors $\mathbf{a}$, $\mathbf{b}$ and $\mathbf{c}$, respectively, such that the Cartesian positions vector of the atom, $\mathbf{r}$, is

$$
\mathbf{r} = u\mathbf{a} + v\mathbf{b} + w\mathbf{c}
$$

To add a second atom, simply add a second line with the new information, and similarly for additional atoms.

An alternative is to specify the atomic coordinates with reference to their absolute Cartesian coordinates:

```
%block positions_abs
[unit]
symbol  x y z
%endblock positions_abs
```
where `[unit]` is an optional length unit (default: `ang`, meaning Angstroms), `symbol` is the chemical symbol for the atomic element, and `x`, `y` and `z` are the Cartesian coordinates of the atom, such that the position vector, $\mathbf{r}=(x,y,z)$.

## Comments ##

It can be convenient to add comments to a cell file, not only to explain why certain choices were made, but also as a way of disabling input lines without removing them from the file. Both `!` and `#` are accepted as comment characters, and anything to the right of these will be ignored by CASTEP. For example, the cell section
```
# Place a single atom at the origin
%block positions_abs
bohr
C   0.00000000 0.00000000  0.00000000
!Si   0.00000000 0.00000000  0.00000000
%endblock positions_abs
```
has a comment explaining the atomic coordinates, and a single carbon atom at the origin. The second atomic position is commented out, so CASTEP will ignore it.
