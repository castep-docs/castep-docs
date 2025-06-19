
### Molecular vibrational calculations {#sec:molecules}

CASTEP is primarily a solid state code with periodic boundary
conditions, and is not necessarily the first choice for performing
vibrational spectroscopy calculations on molecules. Nevertheless it can
sometimes be convenient to use it in this mode (for example, if it is
desired to compare a molecular crystal with an isolated molecule at
exactly the same level of theory).

With certain limitations this can be done in CASTEP using the “molecule
in large box” method. The idea is to place the molecule in a vacuum by
constructing a large supercell. If the supercell is sufficiently large
that the periodic images of the molecule do not interact then the
frequencies and eigenvectors in the molecular limit can be recovered.
Because the zero charge density in a large volume must still be
represented using a plane-wave basis sat, such calculations can become
expensive, but it is nevertheless essential to perform careful cell size
convergence tests.

A molecule in free space possesses rotational as well as translational
symmetry, which results in three (or two for a linear molecule) free
librational modes of zero frequency. A periodic CASTEP calculation does
not possess this symmetry and the librational mode frequencies will have
nonzero values, either real and positive or imaginary. If a molecular
electric field calculation is desired the parameter

> `efield_ignore_molec_modes`

may be specified with the keyword value of `MOLECULE` or
`LINEAR_MOLECULE`. This omits the 6 (or 5) lowest modes from the
infra-red polarizability calculation, assuming them to be the
librations.

As with crystalline systems it is desirable to maximise the use of
symmetry by optimally orienting the molecule. In this case an additional
criterion applies - the simulation cell vectors should be organised for
maximal compatibility with the molecular symmetry. Any incompatible
symmetry operations will not be found if using the `SYMMETRY_GENERATE`
keyword. For example a tetrahedral molecule is best modelled in a cubic
cell with the 3-fold axes oriented along the cube diagonals. By contrast
a hexagonal molecule such as benzene is better modelled using a
hexagonal simulation cell with the molecule commensurately oriented.

A limitation of this method is that CASTEP implements only the
crystallographic point group symmetry operations, and does not include
all of the molecular point groups. It is not always possible to take
full advantage of molecular symmetry, and 5-fold rotation axes and
icosahedral groups can not be represented. In such cases some
degeneracies will be lifted and only approximately satisfied, and the
group theoretical analysis of the eigenvectors will not be correct for
the molecular point group.

Finally, it is sometimes desirable to compute the vibrational spectrum
of an ion rather than a neutral molecule. This adds a number of
complications of different degrees of severity. First is the well-known
result that semi-local DFT (LDA and GGA) severely underbinds anions, and
the description of the molecular states in some systems may be
substantially incorrect. Second, the introduction of a non-zero
molecular charge in a periodic cell necessitates the addition of a
compensating charge to avoid a divergent Coulomb energy. CASTEP
implicitly adds a uniform charge distribution which integrates over the
cell to the negative of the sum of ionic and electronic charge in the
system. This model while effective, gives rise to additional
electrostatic terms which decrease only as $1/L^{3}$. Consequently it is
impossible to completely converge such a calculation with respect to
cell size. It is beyond the scope of this document to describe the
techniques which may be used to recover the “infinite” volume limit. The
reader is referred to ref ([Leslie and Gillan 1985](Bibliography.md#ref-leslie:85)) and
the extensive literature which cites this paper for further reading. An
example of a successful approach involving an extrapolation of
frequencies of a molecular anion to the infinite cell limit is given in
Parker *et al.* ([Parker et al. 2006](Bibliography.md#ref-ParkerRWBHY06)).

### Isotopic substitution calculations {#sec:isotopes}

A powerful technique in experimental spectroscopy is *isotopic
substitution* where the sample is modified by the substitution of a
common isotope of some element by a heavier or lighter one. This can
provide valuable site-specific spectroscopic information, particularly
if the substitution can be performed in a site-specific manner. Force
constants and dynamical matrices do not depend on nuclear mass, and are
therefore one set of computations will suffice irrespective of isotopic
substitution. The `phonons` tool
(section [[phonons-tool]](Plotting-and-analysis-tools.md#sec:phonons-tool)) allows recomputation
of the frequencies for different isotopic substitutions without
recomputing dynamical matrices.

The simplest case is complete substitution. The new `.cell` file should
contain a block specifying the new mass, *e.g.*

> ```
>  %block SPECIES_MASS
>    H     2.014101778
>  %endblock SPECIES_MASS
> ```

Running the `phonon` code will compute the vibrational frequencies and
eigenvectors for a completely deuterated sample.

Slightly more complicated is the case where only one or a few of a
number of sites is to be substituted. In that case the above
prescription is inadequate as it would change all of the sites
containing the species in question. It is therefore necessary to use
CASTEP’s sub-species labelling capabilities. For example the original
cell containing a methane molecule might contain

```
%block SPECIES_POT
C C_00.recpot
H H_04.recpot
%endblock SPECIES_POT

%block POSITIONS_ABS
C    0.0         0.0          0.0
H    0.0         0.0          1.09
H    0.9316592   0.0         -0.36333333
H   -0.4658296   0.8068405   -0.36333333
H   -0.4658296  -0.8068405   -0.36333333
%endblock POSITIONS_ABS
```

The continuation cell for input to `phonons` should contain

```
%block SPECIES_POT
C C_00.recpot
H H_04.recpot
H:D H_04.recpot
%endblock SPECIES_POT

%block POSITIONS_ABS
C    0.0         0.0          0.0
H:D  0.0         0.0          1.09
H    0.9316592   0.0         -0.36333333
H   -0.4658296   0.8068405   -0.36333333
H   -0.4658296  -0.8068405   -0.36333333
%endblock POSITIONS_ABS

%block SPECIES_MASS
   H:D     2.014101778
   H       1.007825032 
   C       12.0107 
%endblock SPECIES_MASS
```

The new atom label may contain any alphanumeric extension following the
colon up to a maximum of 8 characters.

This defines a new system with one hydrogen atom of a methane molecule
replaced by deuterium. Notice that this has broken the initial symmetry
of the cell. The `phonons` program generates a new system of reduced
symmetry with three distinct atom types, and copies the dynamical matrix
data from the original methane system from the `.check` file over to the
corresponding atoms in the new system. It then diagonalises the
dynamical matrix, applies whatever post-processing is specified and
writes the frequencies and eigenvectors as usual.

This straightforward approach fails to take into account isotopic shifts
in bond lengths and geometry, and is therefore an approximate one. Since
isotopic shifts in bond lengths depend in turn on the vibrational
frequency, within the quasiharmionic approximation a self-consistent
approach under which bond lengths and frequencies are simultaneously
adjusted to self-consistency would be required. This would also require
new DFPT electronic calculations at each stage and is beyond the scope
of this utility.

### Constrained lattice dynamics

It is sometimes desirable to compute the vibrational frequencies of a
restricted region of an *ab initio* model. Consider the case of a
molecule adsorbed on a surface. If only the frequencies of the molecular
vibrations are needed it would be desirable to compute a subset of the
modes were this possible. While it is not practical (as it would require
prior knowledge of the eigenvectors of the full calculation), an
alternative approach is to apply constraints to certain atoms.

CASTEP implements a technique known as *constrained lattice dynamics*,
also known as the *partial hessian* method. Nominated atoms are assumed
to be “frozen”, and the corresponding entries of the dynamical matrix
are set to zero. The model is effectively one whereby the atoms in the
region of the system deemed “irrelevant” are assigned a mass of
infinity. It is not necessary to perform any computations for
perturbation of these atoms, and a considerable saving of computational
effort may be achieved.

Frozen atoms are specified a CASTEP `.cell` file using the same syntax
as applies to geometry operations. The block

```
%block IONIC_CONSTRAINTS
1 Si  1   1   1   1
2 Si  2   1   1   1
3 C   4   1   1   1
%endblock IONIC_CONSTRAINTS 
```

constrains silicon atoms numbered 1-2 and C atom number 4 to be fixed.
These do not move during geometry optimisation, and their perturbations
are not considered during a lattice dynamics calculation. In fact the
constrained lattice dynamics method does not make full use of the
generality of CASTEP’s linear constraints block (see for example the
tutorial on MD at <http://www.castep.org>) but only identifies atoms
which are fully constrained not to move. As in the example above, there
should be a single line for each atom which creates a uniquely numbered
constraint. This should contain a “1” in all of the x, y, z positions.

Except in rather specialised geometries the presence of fixed atom
constraints is incompatible with most symmetry operations, and therefore
symmetry should usually be turned off during a constrained lattice
dynamics calculation. There is also an incompatibility with the acoustic
sum rule (section [[asr]](Running-phonon-calculations.md#sec:asr)) as constraining the atoms
breaks the translational invariance of the Hamiltonian. Acoustic sum
rule correction is therefore disabled automatically if constraints are
present.

