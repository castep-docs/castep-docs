This is a concise list of the common keywords for CASTEP's cell input file. The definitions of the keywords are given in more detail in the [section on the cell file](cell_file.md).

| Keyword in the cell file | Type | Default | Description               |
|---------------|:----:|---------|---------------------------|
`LATTICE_CART`$^1$ | B | -- | The cell lattice vectors in Cartesian coordinates. 
`LATTICE_ABC`$^1$ | B | -- | The cell lattice vectors specified in $ a, b, c, \alpha, \beta, \gamma $ format.   
`POSITIONS_FRAC`$^2$ | B | -- | The positions of the ions in fraction coordinates with respect to the lattice vectors. 
`POSITIONS_ABS`$^2$ | B | -- | The positions of the ions in absolute coordinates. 
`KPOINT_LIST`$^3$ | B | -- | A list of k-points in the Brillouin zone with associated weights. 
`KPOINT_MP_GRID`$^3$ | W | -- | The k-points defined as a Monkhorst-Pack grid by specifying the grid dimensions in each direction. 
`KPOINT_MP_SPACING`$^3$ | P | 0.1 $Å^{-1}$ | The k-points as a Monkhorst-Pack grid by specifying the maximum distance between k-points. 
`KPOINT_MP_OFFSET` | V | 0,0,0 | The offset of the origin of the Monkhorst-Pack grid in fractional coordinates relative to the reciprocal lattice vectors. 
`SPECTRAL_KPOINT_PATH`$^4$ | B | -- | A list of k-points in the Brillouin zone which defines the path along which a band-structure calculation will be performed. 
`SPECTRAL_KPOINT_PATH_SPACING` | P | 0.1 $Å^{-1}$ | Specifies the maximum spacing between k-points along the path for which a band structure calculation will be performed. 
`SPECTRAL_KPOINT_LIST`$^4$ | B | SCF k-points | A list of k-points at which a band-structure calculation will be performed. 
`SPECTRAL_KPOINT_MP_GRID`$^4$ | W | -- | The k-points for optical matrix element calculations defined as a Monkhorst-Pack grid by specifying the grid dimensions in each direction. 
`SPECTRAL_KPOINT_MP_SPACING`$^4$ | P | 0.1 Å$^{-1}$ | The k-points for optical matrix element calculations as a Monkhorst-Pack grid by specifying the maximum distance between k-points. 
`SPECTRAL_KPOINT_MP_OFFSET` | V | 0,0,0 | The offset of the origin of the Monkhorst-Pack grid for optical matrix element calculations in fractional coordinates relative to the reciprocal lattice vectors. 
`PHONON_KPOINT_PATH`$^5$ | B | -- | A list of k-points in the Brillouin zone which defines the path along which a phonon calculation will be performed. 
`PHONON_KPOINT_PATH_SPACING` | P | 0.1 Å$^{-1}$ | Specifies the maximum spacing between k-points along the path for which a phonon calculation will be performed. 
`PHONON_KPOINT_LIST`$^5$ | B | SCF k-points | A list of k-points at which a phonon calculation will be performed. 
`PHONON_GAMMA_DIRECTIONS` | B | See text | The directions in which the gamma point will be approached for calculation of the LO/TO splitting. 
`SYMMETRY_GENERATE`$^6$ | D | no symmetry | If this is present, the highest symmtery group of the cell will found and the corresponding symmetry operations generated. 
`SYMMETRY_OPS`$^6$ | B | no symmetry | The symmetry operations that apply to the cell. 
`SYMMETRY_TOL` | P | 0.01 Å | The tolerance within which symmetry will be enforced.
`IONIC_CONSTRAINTS` | B | no constraints | The constraints on the motion of ions during relaxation or MD. 
`FIX_ALL_IONS` | L | `FALSE` | Constrain all ionic positions to remain fixed.
`FIX_ALL_CELL` | L | `FALSE` | Constrain all cell parameters to remain fixed. 
`FIX_COM` | L | `TRUE` | Constrain the centre of mass of the ions to remain fixed.
`CELL_CONSTRAINTS` | B | no constraints | The constraints on changes in the cell shape during relaxation or MD. 
`SPECIES_MASS` | B | atomic mass | The masses of the ionic species. 
`SPECIES_POT` | B | see text | The names of the pseudopotentials associated with each species. 
`SPECIES_LCAO_STATES` | B | see text | The number of angular momentum states to use in the LCAO basis set for this species when performing population analysis. 
`EXTERNAL_PRESSURE` | B | no pressure | The external pressure tensor. 
`IONIC_VELOCITIES` | B | random | The velocities of the ions in Cartesian coordinates. 

For the argument types, B indicates block data, P means a physical value, L is a
logical value, D is a keyword that may simply be defined (present) or
not, V is a real vector and W is an integer vector.

$^1$ Only one of `LATTICE_CART` and `LATTICE_ABC` maybe present in a cell file.

$^2$ Only one of `POSITIONS_FRAC` and `POSITIONS_ABS` may be present in a cell file.

$^3$ Only one of `KPOINTS_LIST`, `KPOINTS_MP_GRID` and `KPOINTS_MP_SPACING` may be present in a cell file.

$^4$ Only one of `SPECTRAL_KPOINT_PATH`,`SPECTRAL_KPOINTS_MP_GRID`, `SPECTRAL_KPOINTS_MP_SPACING` and `SPECTRAL_KPOINT_LIST` may be present in a cell file.

$^5$ Only one of `PHONON_KPOINT_PATH` and `PHONON_KPOINT_LIST` may be
present in a cell file.

$^6$ Only one of `SYMMETRY_GENERATE` and `SYMMETRY_OPS` may be present in a cell file.


