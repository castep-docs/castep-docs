
This guide introduces the concepts, keywords and techniques needed to
set up and run CASTEP calculations of lattice dynamics and vibrational
spectroscopy. The material covers the various lattice-dynamical and
related methods implemented in CASTEP, how to set up a calculation, and
presents simple examples of the major types of calculation. It is
assumed that the reader is familiar with the general CASTEP input and
output files and keywords to the level which may be found at
<https://castep-docs.github.io/castep-docs/>. It describes how to
analyse the results and generate graphical output using the CASTEP
tools, but does not cover the modelling of IR, Raman or inelastic
neutron or X-ray spectra, which are large subjects and beyond the scope
of this document.

It does not describe the compilation and installation of CASTEP and its
tools, nor does it describe the operational details of invoking and
running CASTEP. Computational clusters, HPC computing environments and
batch systems vary to a considerable degree, and the reader is referred
to their cluster or computer centre documentation. It does discuss
general aspects of managing and running large phonon calculations
including restarts and parallelism in
section [[large-calculations]](Running-Large-Calculations.md#sec:large-calculations).

There are many useful textbooks on the theory of vibrations in crystals,
or *lattice dynamics* as the subject is usually known. A good beginner’s
guide is “Introduction to Lattice Dynamics” by Martin Dove ([Dove
1993](Bibliography.md#ref-Dove93)). More advanced texts are available by
Srivistava ([Srivastava 2023](Bibliography.md#ref-Srivastava90)), Maradudin ([Maradudin
and Horton 1980](Bibliography.md#ref-Maradudin80)) and many others. The following
section presents only a brief summary to introduce the notation.

### Theory of Lattice Dynamics {#sec:theory}

Consider a crystal with a unit cell containing $N$ atoms, labelled
$\kappa$, and $a$ labels the primitive cells in the lattice. The crystal
is initially in mechanical equilibrium, with Cartesian co-ordinates
$R_{{\kappa,\alpha}}$, ($\alpha=1..3$ denotes the Cartesian $x$,$y$ or
$z$ direction).
${{\mathbf{u}}_{{\kappa,\alpha},a}}= x_{{\kappa,\alpha,a}} - R_{{\kappa,\alpha,a}}$
denotes the displacement of an atom from its equilibrium position.
Harmonic lattice dynamics is based on a Taylor expansion of total energy
about structural equilibrium co-ordinates.     
{#eq:taylor}

$$E = E_0 + \sum_{{\kappa,\alpha,a}} \frac{\partial E}{\partial{{\mathbf{u}}_{{\kappa,\alpha},a}}}.{{\mathbf{u}}_{{\kappa,\alpha},a}}+ {\frac{1}{2}}
    \sum_{{\kappa,\alpha,a},{\kappa^\prime,\alpha^\prime},a^\prime}  {{\mathbf{u}}_{{\kappa,\alpha},a}}.{\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(a,a^\prime)}. {{\mathbf{u}}_{{\kappa^\prime,\alpha^\prime},a^\prime}}+ ...$$

where ${{\mathbf{u}}_{{\kappa,\alpha},a}}$ is the vector of atomic
displacements from equilibrium and
${\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(a)}$ is the matrix
of *force constants*     
{#eq:fcmat}

$${\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(a)}\equiv {\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(a,0)}= \frac{\partial^2 E}{\partial {{\mathbf{u}}_{{\kappa,\alpha},a}}\partial {{\mathbf{u}}_{{\kappa^\prime,\alpha^\prime},0}}} \;.$$

At equilibrium the forces
$F_{{\kappa,\alpha}} = -\partial E/\partial{{\mathbf{u}}_{{\kappa,\alpha}}}$
are all zero so the first-order term vanishes. In the *Harmonic
Approximation* the 3$^{\text{rd}}$ and higher order terms are neglected
[^1]. Assume *Born von Karman* periodic boundary conditions and
substitute a plane-wave trial solution

$${{\mathbf{u}}_{{\kappa,\alpha}}}= {\mathbf{\varepsilon}_{m{\kappa,\alpha}{\mathbf{q}}}}\exp( i {\mathbf{q}}. {\mathbf{R}}_{{\kappa,\alpha}} - \omega_{m} t)$$

with a phonon wavevector ${\mathbf{q}}$ and a *polarization vector*
${\mathbf{\varepsilon}_{m{\kappa,\alpha}{\mathbf{q}}}}$. This yields an
eigenvalue equation     
{#eq:dmat-eigen}

$${D^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(\mathbf{q})}{\mathbf{\varepsilon}_{m{\kappa,\alpha}{\mathbf{q}}}}= \omega_{m,{\mathbf{q}}}^2 {\mathbf{\varepsilon}_{m{\kappa,\alpha}{\mathbf{q}}}}\; .$$

The **dynamical matrix** is defined as     
{#eq:dmat}

$${D^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(\mathbf{q})}= \frac{1}{\sqrt{M_\kappa M_{\kappa^\prime}}} {C^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(\mathbf{q})}=
\frac{1}{\sqrt{M_\kappa M_{\kappa^\prime}}} \sum_{a} {\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(a)}
    e^{-i \mathbf{q}.{\mathbf{r}}_a}$$

where the index $a$ runs over all lattice images of the primitive cell.
That is, the dynamical matrix is the mass-reduced Fourier transform of
the force constant matrix.

The eigenvalue equation [[dmat-eigen]](Introduction.md#eq:dmat-eigen) can be
solved by standard numerical methods. The eigenvalues,
$\omega_{m,{\mathbf{q}}}^2$, must be real numbers because
${D^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}(\mathbf{q})}$ is a
Hermitian matrix. The vibrational frequencies at each mode
$\omega_{m,{\mathbf{q}}}$ are obtained as the square roots, and
consequently are either real and positive (if
$\omega_{m,{\mathbf{q}}}^2 > 0$) or pure imaginary (if
$\omega_{m,{\mathbf{q}}}^2 < 0$) The corresponding eigenvectors are the
polarization vectors, and describe the pattern of atomic displacements
belonging to each mode.

The central question of *ab-initio* lattice dynamics is therefore how to
determine the force constants
${\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}}$ which are the
*second derivatives* of the total energy with respect to two atomic
displacements. The *first* derivatives are the forces, and may be
determined straightforwardly using the Hellman–Feynmann Theorem as the
derivative of the quantum mechanical energy with respect to an atomic
displacement, $\lambda$     
{#eq:hellman}

$$\begin{aligned}
 E &=  {\left < \psi \right |}{\hat{H}}{\left | \psi \right >}\qquad \text{with}\qquad {\hat{H}}= \nabla^2 + V_{\text{SCF}}\\
F  &=  - \frac{dE}{d\lambda} \\
   &=  - {\left < {\frac{d \psi}{d \lambda}}\right |}{\hat{H}}{\left | \psi \right >}-
    {\left < \psi \right |}{\hat{H}}{\left | {\frac{d \psi}{d \lambda}}\right >}- {\left < \psi \right |}{\frac{d V}{d \lambda}}{\left | \psi \right >} \; .
\end{aligned}$$

If ${\left < \psi \right |}$ represents the ground state of ${\hat{H}}$
then the first two terms vanish because
${\left < \psi \right |}{\hat{H}}{\left | {\frac{d \psi}{d \lambda}}\right >}= \epsilon_n {\left < \psi \right |}{\left | {\frac{d \psi}{d \lambda}}\right >}= 0$.
Differentiating again yields

$$\frac{d^2 E}{d \lambda^2} = {\left < {\frac{d \psi}{d \lambda}}\right |}{\frac{d V}{d \lambda}}{\left | \psi \right >}+
    {\left < \psi \right |}{\frac{d V}{d \lambda}}{\left | {\frac{d \psi}{d \lambda}}\right >}- {\left < \psi \right |}{\frac{d^2 V}{d \lambda^2}}{\left | \psi \right >}\;.$$

Unlike equation [[hellman]](Introduction.md#eq:hellman) the terms involving the
derivatives of the wavefunctions do not vanish. This means that it is
necessary to somehow compute the *electronic response* of the system to
the displacement of an atom to perform *ab-initio* lattice dynamics
calculations. This may be accomplished either by a finite-displacement
method, *i.e.* performing two calculations which differ by a small
displacement of an atomic co-ordinate and evaluating a numerical
derivative, or by using perturbation theory to evaluate the response
wavefunction ${\frac{d \psi}{d \lambda}}$. (In Kohn-Sham DFT, as
implemented in CASTEP we actually evaluate the first-order response
orbitals.)

Some general references on *ab-initio* lattice dynamics methods are
chapter 3 of ref ([Srivastava 2023](Bibliography.md#ref-Srivastava90)) and the review
paper by Baroni *et al.*([Baroni et al. 2001](Bibliography.md#ref-BaroniDDG01)).

[^1]: Thus the harmonic approximation is noticeably in error for very
    asymmetric potentials, which for examplein the worst cases can lead
    to disagreement with experimental frequencies of up to 5% for the
    librational modes of small molecular crystals, or OH bonds. It also
    neglects phonon-phonon interactions and therefore does not predict
    any intrinsic line broadening.

### Prerequisites {#sec:prerequisites}

#### Geometry Optimisation {#sec:geometry}

A successful phonon calculation almost always requires a preceding
geometry optimisation (except for small, high symmetry system where all
atoms lie on crystallographic high-symmetry positions and the forces are
zero by symmetry). It is *not* necessary to perform a variable-cell
optimisation - the lattice dynamics is well defined at any stress or
pressure, and phonons in high-pressure or strained systems are
frequently of scientific interest. The two most convenient ways of
achieving this are to

- Set up the phonon run as a continuation of the geometry optimisation
  by setting the parameters keyword `continuation : <geom-seed.check>`.

- Add the keyword `write_cell_structure : TRUE` to the geometry
  optimization run and modify the resulting `<seedname>-out.cell` to use
  as the input for a new run.

The importance of a high-quality structure optimisation can not be
overemphasized - the energy expansion in
equation [[taylor]](Introduction.md#eq:taylor) makes the explicit assumption that
the system is in mechanical equilibrium and that all atomic forces are
zero.

This is sufficiently important that before performing a phonon
calculation CASTEP will compute the residual forces to determine if the
geometry is converged. If any component of the force exceeds
`geom_force_tol` it will print an error message and abort the run.
Should a run fail with this message, it may be because the geometry
optimisation run did not in fact succeed, or because some parameter
governing the convergence (*e.g.* the cutoff energy) differs in the
phonon run compared to the geometry optimisation. In that case the
correct procedure would be to re-optimise the geometry using the same
parameters as needed for the phonon run. Alternatively if the geometry
error and size of the force residual are tolerable, then the value of
`geom_force_tol` may be increased in the `.param` file of the phonon
calculation which will allow the run to proceed.

How accurate a geometry optimization is needed? Accumulated practical
experience suggests that substantially tighter tolerances are needed to
generate reasonable quality phonons than are needed for structural or
energetics calculations. For many crystalline systems a geometry force
convergence tolerance set using parameter `geom_force_tol` of
0.01 eV/Å is typically needed. For “soft” materials containing weak
bonds such as molecular crystals or in the presence of hydrogen bonds,
an even smaller value is frequently necessary. Only careful convergence
testing of the geometry and resulting frequencies can determine the
value to use. To achieve a high level of force convergence, it is
obviously essential that the forces be evaluated to at least the same
precision. This will in turn govern the choice of electronic k-point
sampling, and probably require a smaller than default SCF convergence
tolerance, `elec_energy_tol`. See
section [[convergence]](Running-phonon-calculations.md#sec:convergence) for further discussion
of geometry optimisation and convergence for phonon calculations.

If a lattice dynamics calculation is performed at the configuration
which minimises the energy the force constant matrix
${\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}}$ is positive
definite, and all of its eigenvalues are positive. Consequently the
vibrational frequencies which are the square roots of the eigenvalues
are real numbers. [^2] If on the other hand the system is not at a
minimum energy equilibrium configuration
${\Phi^{\kappa,\kappa^\prime}_{\alpha,\alpha^\prime}}$ is not
necessarily positive definite, the eigenvalues
$\omega_{m,{\mathbf{q}}}^2$ may be negative. In that case the
frequencies are imaginary and do not correspond to a physical
vibrational mode. For convenience CASTEP prints such values using a a
minus sign “$-$”. These are sometimes loosely referred to as “negative”
frequencies, but bear in mind that this convention really indicates
negative *eigenvalues* and *imaginary* frequencies. [^3]

[^2]: Beware of the tempting but incorrect assumption that a CASTEP
    geometry optimisation is sufficient to find the true minimum-energy
    configuration of the atoms. Any such geometry optimization can only
    yield the minimum subject to the constraints imposed; in most cases
    by crystallographic symmetry and in all cases by the lattice repeat
    symmetry of the unit cell. The true system may be able to lower its
    energy further, but only by breaking the symmetry or lattice
    constraint. In such cases there will be an imaginary frequencies
    corresponding to any such possibility.

[^3]: This apparent problem may be turned to a positive advantage. A
    lattice dynamics calculation can be used as a test whether a
    purported equilibrium crystal structure really is dynamically
    stable. The presence of imaginary frequencies anywhere in the
    Brillouin Zone would indicate that the structure is unstable to a
    distortion along the corresponding eigenvector. Another occasion
    would be to investigate a transition state. By definition a
    transition state geometry is at a stationary saddle point of the
    energy hypersurface and must therefore exhibit precisely one
    imaginary frequency. A final example is the case of a system
    exhibiting a “soft-mode” phase transition where the frequency at the
    Brillouin-zone boundary decreases to zero, indicating that the
    crystal could lower its energy by doubling of the corresponding unit
    cell parameter. It is often useful to explore how the frequency
    approaches zero as some external variable such as pressure or
    lattice constant is varied, in order to precisely locate the phase
    transition. Reference ([Pallikara et al. 2022](Bibliography.md#ref-Pallikara22))
    discusses the physical significance of imaginary phonon modes in
    some details and with examples.

#### Use of Symmetry {#sec:symmetry}

CASTEP lattice dynamics uses symmetry to reduce the number of
perturbation calculations to the irreducible set, and applies the
symmetry transformations to generate the full dynamical matrix. Combined
with the usual reduction in k-points in the IBZ, savings in CPU time by
use of crystallographic symmetry can easily be a factor of 10 or more.
It is therefore important to maximise the symmetry available to the
calculation, and to either specify the symmetry operations in the
`.cell` file using the `%block SYMMETRY_OPS` keyword or generate them
using keyword `symmetry_generate`.

CASTEP generates the dynamical matrix using perturbations along
Cartesian X, Y and Z directions. To maximise the use of symmetry and
minimise the number of perturbations required, the symmetry axes of the
crystal or molecule should be aligned along Cartesian X, Y, and Z. If
the cell axes are specified using `%block LATTICE_ABC`, CASTEP attempts
to optimally orient the cell in many cases, but if using
`%block LATTICE_CART` it is the responsibility of the user. This is one
of the few cases where the absolute orientation makes any difference in
a CASTEP calculation. An optimal orientation will use the fewest
perturbations and lowest CPU time and will also exhibit best convergence
with respect to, for example electronic k-point set.

Phonon calculations should normally be set up using the *primitive* unit
cell. As an example the conventional cell of a face-centred-cubic
crystal contains four primitive unit cells, and thus four times the
number of electrons and four times the volume. It will therefore cost 16
times as much memory and 16 times the compute time to run even the SCF
calculation. CASTEP’s symmetry analysis will print a warning to the
`.castep` file if this is detected. A further reason to work with the
primitive cell is that CASTEP defines its phonon ${\mathbf{q}}$-point
parameters with respect to the actual simulation cell, and so a naive
attempt to specify ${\mathbf{q}}$-point paths would result in output for
a folded Brillouin-Zone, which is unlikely to be what is desired. Most
input structure-preparation tools like `c2x` or `cif2cell` are capable
of conversion between conventional and primitive cells.

There is a further consideration related to symmetry; structure, cell
and atomic co-ordinates must be specified to a reasonably high accuracy
in the input files. CASTEP uses stochastic methods to analyse the effect
of symmetry operations on the dynamical matrix, and this analysis can
fail to detect symmetries or otherwise misbehave unless symmetry
operations, lattice vectors and atomic co-ordinates are consistent to a
reasonable degree of precision. It is recommended that symmetry-related
lattice vectors and internal co-ordinates are consistent to at least
10$^{-6}$Å  which can only be achieved if the values in the `.cell` file
are expressed to this number of decimal places. This is particularly
significant in the case of trigonal or hexagonal systems specified with
`%block LATTICE_CART` where equality of the $a$ and $b$ cell vector
lengths is only as precise as the number of significant figures used to
represent the components.

Two features of CASTEP’s `.cell` file input may be helpful. First is the
ability to input cell vectors and atomic positions using (a limited set
of) mathematical syntax. See
figure [[example-gamma]](Running-phonon-calculations.md#fig:example-gamma) for an example.
Second, if the cell file keyword `snap_to_symmetry` is present, CASTEP
will adjust co-ordinates and vectors to satisfy symmetry to high
precision.

Alternatively there is a utility program in the academic distribution
named `symmetry_snap` which implements the same functionality. This is
invoked simply as

> `symmetry_snap` *seedname*

which reads *seedname*`.cell` and outputs the symmetrised version to
*seedname*`-symm.cell`

