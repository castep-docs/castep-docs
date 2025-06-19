
The cell and param file keywords used specifically for phonon and
related calculations are listed here alphabetically with brief
descriptions.

### CELL file keywords {#sec:cellkw}

PHONON_FINE_KPOINT_LIST

:   *List of phonon wavevectors on the fine grid* (Block)  
    Phonon frequencies are calculated on a coarse set of wavevectors
    using DFPT and interpolated onto this finer list of points.

PHONON_FINE_KPOINT_MP_GRID

:   *Fine MP-grid of phonon wavevectors* (Integer Vector)  
    Phonon frequencies are calculated on a coarse set of wavevectors
    using DFPT and interpolated onto this finer grid of wavevectors.

PHONON_FINE_KPOINT_MP_OFFSET

:   *Origin offset of the fine phonon MP grid* (Real Vector)  
    The offset of the fine MP grid at which the phonons calculated using
    DFPT are interpolated.

PHONON_FINE_KPOINT_MP_SPACING

:   *The spacing of points on the fine MP set for phonons* (Physical)  
    This specifies the minimum spacing between points on a
    Monkhorst-Pack grid that phonons will be interpolated onto from the
    coarser phonon grid.

PHONON_FINE_KPOINT_PATH

:   *Path of phonon wavevectors on a fine scale* (Block)  
    Phonon frequencies are calculated on a coarse set of wavevectors
    using DFPT and interpolated onto this finer path.

PHONON_FINE_KPOINT_PATH_SPACING

:   *The fine spacing of points on a path at which phonons are
    calculated* (Physical)  
    The spacing of k-points along a path (specified by
    `PHONON_FINE_KPOINT_PATH`) at which phonons will be interpolated
    from a coarser grid

PHONON_GAMMA_DIRECTIONS

:   *Phonon gamma-point LO/TO splitting* (Block)  
    This is a list of directions along which ${\mathbf{q}}\rightarrow 0$
    will be calculated for the non-analytic LO/TO term in a phonon
    calculation at ${\mathbf{q}}=0$. Fractional coordinates must be
    used. Default value: The k-point before gamma in the k-point list,
    or the one after or (0.1, 0, 0)

PHONON_KPOINTS_LIST

:   *Alias for* `PHONON_KPOINT_LIST` (Block)  
    Default value: Determined from `PHONON_KPOINT_LIST`

PHONON_KPOINTS_PATH

:   *Alias for* `PHONON_KPOINT_PATH` (Block)  
    Default value: Determined from `PHONON_KPOINT_PATH`

PHONON_KPOINTS_PATH_SPACING

:   *Alias for* `PHONON_KPOINT_PATH_SPACING` (Physical)  
    Default value: Determined from `PHONON_KPOINT_PATH_SPACING`

PHONON_KPOINT_LIST

:   *List of phonon k-points* (Block)  
    A list of discrete k-points at which phonon frequencies and
    eigenvectors will be calculated. Default value: SCF k-points are
    used if an alternative `PHONON_KPOINT_*` specifier is not given.

PHONON_KPOINT_MP_GRID

:   *Phonon wavevector Monkhorst-Pack grid* (Integer Vector)  
    The phonon wavevectors defined by a Monkhorst-Pack grid. Symmetry
    (if specified) will be used to generate the wavevector list and
    weights.

PHONON_KPOINT_MP_OFFSET

:   *Phonon wavevector Monkhorst Pack grid offset* (Real Vector)  
    The offset of the origin of the Monkhorst-Pack set for phonons in
    fractional coordinates, or the keyword `INCLUDE_GAMMA`. Default
    value: `INCLUDE_GAMMA`

PHONON_KPOINT_MP_SPACING

:   *Phonon wavevector Monkhorst-Pack grid density* (Physical)  
    The density of wavevectors on a a Monkhorst-Pack grid for phonon
    calculations. Units of inverse length should be specified. Default
    value: 0.1 A$^{-1}$.

PHONON_KPOINT_PATH

:   *Phonon dispersion k-point path* (Block)  
    The path continuous through the BZ on which phonon dispersion is
    calculated. This is specified in fractional coordinates. Default
    value: None.

PHONON_KPOINT_PATH_SPACING

:   *Phonon dispersion path spacing* (Physical)  
    The maximum spacing between kpoints along the path specified by
    `PHONON_KPOINT_PATH`. Units of inverse length must be specified.
    Default value: 0.1 A$^{-1}$.

PHONON_SUPERCELL_MATRIX

:   *Supercell matrix for finite difference phonon calculations*
    (Block)  
    The supercelling matrix for force constant matrix calculations. The
    supercell matrix is specified by a 3x3 integer matrix which gives
    the supercell used in finite-difference phonon calculations.

SUPERCELL_KPOINTS_LIST

:   *SCF k-points for FD phonon supercell* (Block)  
    A list of k-points in the Brillouin zone (with associated weights)
    used for BZ integration during a supercell FD phonon calculation.
    The k-point weights must sum to 1. Default value: Generated from
    `SUPERCELL_KPOINTS_MP_SPACING` and the crystal symmetry.

SUPERCELL_KPOINTS_MP_GRID

:   *SCF Monkhorst-Pack grid for FD phonon supercell calculation*
    (Integer Vector)  
    The k-points defined by a Monkhorst-Pack grid when doing a finite
    displacement phonon calculation. Symmetry (if specified) will be
    used to generate the k-point list and weights. Default value:
    Generated from `SUPERCELL_KPOINTS_MP_SPACING`.

SUPERCELL_KPOINTS_MP_OFFSET

:   *SCF Monkhorst Pack grid offset for a FD phonon supercell
    calculation* (Real Vector)  
    The offset of the origin of the Monkhorst-Pack set in fractional
    coordinates when performing a finite displacement phonon
    calculation. Default value: (0, 0, 0).

SUPERCELL_KPOINTS_MP_SPACING

:   *SCF Monkhorst-Pack grid density for FD phonon supercell
    calculation* (Physical)  
    The k-point density of a Monkhorst-Pack grid for a supercell FD
    phonon calculation. Units of inverse length should be specified.
    Default value: 0.1 A$^{-1}$.

    ### PARAM file keywords {#sec:paramkw}

NUM_BACKUP_ITER

:   *md/geom iterations between backups* (Integer)  
    Specifies the number of iterations between backups of all data for
    restarts, for a geometry optimization or molecular dynamics run.
    Allowed values: (any integer) $>$ 0 Default value : 5

BACKUP_INTERVAL

:   *seconds between backups* (Integer)  
    Specifies the interval, in seconds, between backups of all data for
    restarts, for a geometry optimization/molecular dynamics/phonon
    run - if less than or equal to zero then no timed backups. Allowed
    values: (any) Default value : 0

BORN_CHARGE_SUM_RULE

:   *enforce Born charge sum rule* (Logical)  
    Selects whether to explicitly correct the Born effective charge
    tensor to enforce the sum rule that effective charges sum to zero.

CALCULATE_BORN_CHARGES

:   *calculate Born effective charges* (Logical)  
    Selects whether to compute Born effective charge tensors as part of
    a phonon or E-field linear-response calculation. Allowed values:
    TRUE or FALSE Default value : TRUE

CALCULATE_RAMAN

:   *calculate Raman intensities* (Logical)  
    Selects whether to compute Raman intensities as part of a phonon or
    E-field linear-response calculation. Allowed values: TRUE or FALSE
    Default value : FALSE

EFIELD_CALC_ION_PERMITTIVITY

:   *calculate zero-frequency permittivity* (Logical)  
    Specifies whether or not to compute the zero-frequency dielectric
    permittivity based on the ionic response to electric fields. This
    requires a gamma-point phonon calculation in addition to the EFIELD
    linear response one. Allowed values: TRUE or FALSE Default value :
    TRUE

EFIELD_CALCULATE_NONLINEAR

:   *calculate non-linear optical susceptibility* (String)  
    Select which non-linear optical property to calculate during
    TASK=EFIELD calculation. Allowed values: NONE, CHI2 Default value :
    NONE

EFIELD_CONVERGENCE_WIN

:   *convergence tolerance window in EFIELD* (Integer)  
    The LR convergence criteria must be met for `EFIELD_CONVERGENCE_WIN`
    iterations before acceptance. Allowed values: (any integer) $\ge$ 2
    Default value : 2

EFIELD_DFPT_METHOD

:   *E-field DFPT solver method* (String)  
    Selects the solver for E-field density functional perturbation
    theory.. Allowed values: ALLBANDS(=VARIATIONAL) or DM(=GREEN) to
    select Gonze variational or Baroni Green function with DM solver.
    Default value : ALLBANDS

EFIELD_ENERGY_TOL

:   *E(2) convergence tolerance in EFIELD* (Physical)  
    Tolerance for accepting convergence of the field constants during
    PHONON calculation. The difference between max and min E(2) values
    over `EFIELD_CONVERGENCE_WIN` iterations must be less than this. NB
    This is an INTENSIVE parameter and has units of volume. Allowed
    values: (any) $>$ 0.0 Default value : $10^{-5}$ A$^3$

EFIELD_FREQ_SPACING

:   *Spacing of frequencies in permittivity calculation* (Physical)  
    Spacing of frequencies in calculation of frequency-dependent
    permittivity. Allowed values: (any) $>$ 0.0 Default value : 1.0
    cm$^{-1}$

EFIELD_IGNORE_MOLEC_MODES

:   *Ignore lowest modes in permittivity calculation* (String)  
    Ignore the lowest lying (3,5,6) modes when computing the ionic
    contribution to the permittivity and polarizability. Allowed values:
    `CRYSTAL`, `MOLECULE`, `LINEAR_MOLECULE` Default value : `CRYSTAL`

EFIELD_MAX_CG_STEPS

:   *max. number of cg steps in EFIELD* (Integer)  
    The maximum number of conjugate gradient steps in EFIELD calculation
    before performing a SD reset. Allowed values: (any integer) $\ge$ 0
    Default value : 0

EFIELD_MAX_CYCLES

:   *maximum cycles in EFIELD* (Integer)  
    The maximum number of SCF cycles in EFIELD calculation regardless of
    convergence. Allowed values: (any integer) $>$ 0 Default value : 50

EFIELD_OSCILLATOR_Q

:   *Q-factor for line-shape broadening* (Real)  
    Oscillator Q-factor for line-shape broadening in calculation of
    frequency- dependent permittivity. Allowed values: (any) $>$ 0.0
    Default value : 50.0

EFIELD_UNIT

:   *unit of electric field in output* (String)  
    Controls the units used for all electric field in output - many
    different units are supported. Default value : eV/A/E

ELEC_METHOD

:   *treatment of metals or finite temperature insulator* (String)  
    The treatment of metals or finite temperature insulator to be used.
    An alias for `METALS_METHOD`. Allowed values: NONE (=ALLBANDS), DM,
    EDFT Default value : DM

EXCITED_STATE_SCISSORS

:   *“scissors” operator band-gap correction* (Physical)  
    Effectively adds an offset to conduction-band eigenvalues as
    empirical correction for LDA/GGA underestimation of band-gaps.
    Allowed values: (any) Default value : 0.0

FIX_OCCUPANCY

:   *treat system as an insulator* (Logical)  
    Determines if the system is treated as an insulator or a metal.
    Allowed values: TRUE or FALSE Default value : FALSE

GEOM_FORCE_TOL

:   *geometry optimization force convergence tolerance* (Physical)  
    Tolerance for accepting convergence of the maximum \|ionic force\|
    during geometry optimization. Allowed values: (any) $>$ 0.0 Default
    value : 0.05 eV/A

PHONON_CALCULATE_DOS

:   *density of states calculation* (Logical)  
    Determines whether or not the phonon density of states will be
    calculated. Allowed values: TRUE or FALSE Default value : FALSE

PHONON_DOS_SPACING

:   *density of states calculation* (Physical)  
    The resolution at which a phonon density-of-states will be
    calculated. Allowed values: (any) $> 0.0$ Default value : 10.0
    cm$^{-1}$.

PHONON_DOS_LIMIT

:   *density of states calculation* (Logical)  
    The largest phonon to be included in a phonon density-of-states
    calculation. Allowed values: (any) $>$ `PHONON_DOS_SPACING` Default
    value : 5000.0 cm$^{-1}$.

PHONON_CALC_LO_TO_SPLITTING

:   *gamma-point phonon LO/TO correction* (Logical)  
    Selects whether to compute non-analytic contribution to dynamical
    matrix from long-ranged electric field effects responsible for LO/TO
    splitting. This requires calculation of the dielectric permittivity
    by E-field linear-response and the Born effective charges. Allowed
    values: TRUE or FALSE Default value : TRUE

PHONON_CONVERGENCE_WIN

:   *convergence tolerance window in LR* (Integer)  
    The LR convergence criteria must be met for `PHONON_CONVERGENCE_WIN`
    iterations before acceptance. Allowed values: (any integer) $\ge$ 2
    Default value : 2

PHONON_ENERGY_TOL

:   *E(2) convergence tolerance in LR* (Physical)  
    Tolerance for accepting convergence of the force constants during
    PHONON calculation. The difference between max and min E(2) values
    over `PHONON_CONVERGENCE_WIN` iterations must be less than this.
    Allowed values: (any) $>$ 0.0 Default value : $10^{-5}$ eV/A$^2$

PHONON_FINE_METHOD

:   *fine phonon calculation method* (String)  
    Selects which calculation method to use for phonon calculation on a
    fine grid. Allowed values: NONE, SUPERCELL, INTERPOLATE Default
    value : SUPERCELL if TASK=THERMODYNAMICS else NONE

PHONON_FINITE_DISP

:   *finite displacement amplitude* (Physical)  
    The amplitude of the ionic perturbation to be used in a finite
    displacement phonon calculation. Allowed values: (any) $>$ 0.0
    Default value : 0.01 $a_0$

PHONON_FORCE_CONSTANT_CUTOFF

:   *Cutoff for force constant matrix* (Physical)  
    The cutoff for the force constant matrix in a phonon calculation on
    a fine grid with supercell method. Allowed values: (any) $\ge$ 0.0
    Default value : 0.0

PHONON_FINE_CUTOFF_METHOD

:   *Selects which method to use to extract non-periodic force constant
    matrix from periodic supercell.* (String)  
    With the `CUMULANT` method, all contributions from the periodic
    supercell are summed with a suitable weighting factor to avoid
    double counting of image contributions.  
    The `SPHERICAL` method, uses a minimum image convention with a
    spherical cutoff given by `PHONON_FORCE_CONSTANT_CUTOFF`.  
    Allowed values: `CUMULANT` and `SPHERICAL`. Default value :
    `CUMULANT`.

PHONON_FORCE_CONSTANT_CUT_SCALE

:   *Scaling factor for aspherical force constant matrix cutoff*
    (Real)  
    The range of force constant terms included is up to s times halfway
    to the Wigner Seitz cell boundary. This parameter supplies the value
    of s. Allowed values: 0.0 $\le$ (any) $\ge$ 1.0 Default value : 0.0

PHONON_FORCE_CONSTANT_ELLIPSOID

:   *Ellipsoid size for force constant matrix* (Real)  
    Alias for `PHONON_FORCE_CONSTANT_CUT_SCALE` (deprecated).

PHONON_MAX_CG_STEPS

:   *max. number of cg steps in LR* (Integer)  
    The maximum number of conjugate gradient steps in PHONON calculation
    before performing a SD reset. Allowed values: (any integer) $\ge$ 0
    Default value : 0

PHONON_MAX_CYCLES

:   *maximum cycles in LR* (Integer)  
    The maximum number of SCF cycles in PHONON calculation regardless of
    convergence. Allowed values: (any integer) $\ge$ 0 or if TASK=PHONON
    etc $\ge$ `PHONON_CONVERGENCE_WIN` Default value : 50

PHONON_METHOD

:   *phonon calculation method* (String)  
    Selects which calculation method to use for phonons. Allowed values:
    DFPT, LINEARRESPONSE, FINITEDISPLACEMENT Default value : set by
    `PHONON_FINE_METHOD`

PHONON_DFPT_METHOD

:   *phonon DFPT solver method* (String)  
    Selects the solver for phonon density functional perturbation
    theory.. Allowed values: ALLBANDS(=VARIATIONAL) or DM(=GREEN) to
    select Gonze variational or Baroni Green function with DM solver.
    Default value : DM if `FIX_OCCUPANCY : FALSE`, otherwise ALLBANDS

PHONON_PRECONDITIONER

:   *scheme to use in LR* (String)  
    The preconditioning scheme used by the CG minimiser in LR. Allowed
    values: RTPA, TPA, PS, NONE Default value : TPA

PHONON_SUM_RULE

:   *enforce phonon sum rule* (Logical)  
    Selects whether to explicitly correct the dynamical matrix to
    enforce the acoustic q=0 phonon sum rule, i.e. that 3 modes have
    zero frequency at q=0. Allowed values: TRUE or FALSE Default value :
    FALSE

PHONON_SUM_RULE_METHOD

:   *select method to enforce phonon sum rule* (String)  
    Selects a method to use when enforcing acoustic phonon sum rule.
    Allowed values: NONE : No sum-rule correction will be applied.
    RECIPROCAL : Correct dynamical matrix D(q) at each q using D(q=0).
    REALSPACE : Correct the real-space force constant matrix C(R).
    REAL-RECIP : Correct C(R) in realspace followed by D(q) in
    reciprocal space. MOLECULAR : Correct D(0) using rotational as well
    as translational sum-rule. MOLECULAR-1D : Correct D(0) for a linear
    molecule using rotational as well as translational sum-rule. Default
    value : RECIPROCAL

PHONON_USE_KPOINT_SYMMETRY

:   *reduced or full kpoint set in LR* (Logical)  
    Selects which k-point set to use For each phonon q-vector in LR: T
    =\> use the irreducible k-point set of the (reduced) symmetry, F =\>
    use the complete fully symmetric k-point set. Allowed values: TRUE
    or FALSE Default value : TRUE

PHONON_WRITE_FORCE_CONSTANTS

:   *Write out real-space force constant matrix* (Logical)  
    Selects whether to write out the real-space force constant matrix
    from a phonon supercell or interpolation calculation (to the
    `<seedname>.castep` file) for the case of `PHONON_FINE_METHOD` /=
    NONE. Allowed values: TRUE or FALSE Default value : FALSE

PHONON_WRITE_DYNAMICAL

:   *Write out reciprocal space dynamical matrix* (Logical)  
    Selects whether to write out the reciprocal space dynamical matrices
    from a phonon calculation (to the `<seedname>.castep` file). /=
    NONE. Allowed values: TRUE or FALSE Default value : FALSE

THERMO_T_NPOINTS

:   *Number of points in temperature interval* (Integer)  
    The number of points in the temperature interval for the
    thermodynamics calculation. Allowed values: (any integer) $\ge$ 1
    Default value : 2 if `THERMO_T_STOP` /= `THERMO_T_START` or 1
    otherwise

THERMO_T_SPACING

:   *Temperature spacing* (Physical)  
    The spacing between temperature values for the thermodynamics
    calculation. Allowed values: (any) $>$ (-epsilon) Default value :
    `THERMO_T_STOP` - `THERMO_T_START`

THERMO_T_START

:   *Starting temperature* (Physical)  
    The desired starting temperature for the thermodynamics calculation.
    Allowed values: (any) $>$ 0.0 Default value : 298 K

THERMO_T_STOP

:   *Final temperature* (Physical)  
    The desired final temperature for the thermodynamics calculation.
    Allowed values: (any) $\ge$ `THERMO_T_START` Default value : 298

