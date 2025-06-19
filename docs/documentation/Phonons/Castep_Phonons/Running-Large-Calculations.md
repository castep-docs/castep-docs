
Phonon calculations even on small crystalline systems typically require
many times the CPU resources of a ground state calculation. DFPT
calculations of phonon dispersion compute dynamical matrices at a number
of phonon wavevectors, each of which contains calculations of several
perturbations. Each perturbation will typically require a large k-point
set due to symmetry breaking by the perturbation. If the supercell
method is used, converged calculations require a system of a typical
size of a few hundred atoms, and many perturbations, although the
k-point set used is smaller. Consequently, calculations on systems of
scientific interest frequently require departmental, university or
national-level supercomputing facilities, usually parallel cluster class
machines.

Much of the advice for effective use of cluster or supercomputer class
resources is the same as for ground-state or other types of CASTEP
calculations, but there are a few special considerations for phonon
calculations, set out below. Among the particularly relevant general
items are the choice of memory/speed tradeoff; usually the best approach
is to select the highest speed option `opt_strategy_bias : 3`[^20] which
retains wavefunction coefficients in memory rather than paging to disk.
For large calculations it is very frequently the case that that the
memory requirement (in particular of the wavefunctions) is the most
important consideration in choosing a parallel distribution. If a run
fails due to exceeding the available memory per node, the processor
count requested should be increased to distribute the wavefunction
arrays across a larger set of processors, reducing the memory/processor
requirement.

If increasing the degree of parallel distribution is not possible,
`opt_strategy_bias` can be reduced to 0[^21], which will page
wavefunctions to disk. In that case it is vital to ensure that the
temporary scratch files are written to high-speed disk (either local or
a high-performance filesystem). This is usually controlled by setting
the environment variable `CASTEP_PAGE_TMPDIR` to point to a directory on
an appropriate filesystem[^22].

[^20]: equivalent to `opt_strategy : SPEED`

[^21]: equivalent to `opt_strategy : MEMORY`

[^22]: If `CASTEP_PAGE_TMPDIR` is not set, the code falls back to the
    value of `CASTEP_TMPDIR`.

### Parallel execution {#sec:parallelism}

CASTEP implements a parallel strategy based on a hierarchical
distribution of wavefunction data by k-points, plane-waves, bands and
OpenMP across processors[^23]. In a phonon calculation this is used to
speed up the execution within each perturbation and q-point which are
still executed serially in sequence. Normally an efficient distribution
is chosen automatically providing that the `data_distribution` parameter
is not changed from the default value `MIXED`.

K-points, plane-wave, band and task farm parallelism are all implemented
using the [Message-Passing
Interface](https://hpc-tutorials.llnl.gov/mpi) (MPI) system, and CASTEP
must usually be launched by starting the executable using the `mpiexec`
or similar commands, viz

> `mpiexec -n 1024 castep.mpi <seedname>`

which will start 1024 MPI processes and distribute the calculation
across them.

By contrast [OpenMP](https://www.openmp.org/) parallelism is is
activated by setting the environment variable
`CASTEP_NUM_THREADS : <n>`, which may be done before the `mpiexec`
command to activate hybrid MPI+OpenMP mode.

[^23]: k-points, plane-waves, bands correspond to indices of the
    wavefunction data, so parallelism in any of these will distribute
    the wavefunctions across MPI processes and reduce the memory/process
    requirement.

#### k-point and g-vector parallelism

To best exploit the k-point component of the parallel distribution, the
total number of the processors requested should be a multiple of the
number of electronic k-points or have a large common divisor. The
parallel distribution is printed to the `.castep` file, where in this
example four k-points are used:

> ```
> Calculation parallelised over   32 nodes.
> K-points are distributed over    4 groups, each containing    8 nodes.
> ```

For non-phonon CASTEP calculations it is sufficient to choose a
processor count which is a multiple of $N_{\text{k}}$, and that the
degree of plane-wave-parallelism is not so large that efficiency is
lost. However the choice of processor number in a phonon calculation is
severely complicated by the fact that the number of electronic k-points
in the irreducible Brillouin Zone changes during the run as the
perturbations and phonon q-points have different symmetries. It is not
convenient to compute the number for any perturbation individually
without a detailed analysis, and some compromise between all of the
perturbations should be chosen. To assist in this choice a utility
program, `phonon_kpoints` is provided. This reads the configuration of
the proposed calculation from the `.cell` file and is simply invoked by

> `phonon_kpoints` *seedname*

It then determines and prints the k-point counts, and provides a “figure
of merit” for a range of possible processor counts. On most parallel
architectures the efficiency of the plane-wave parallelism becomes
unacceptable if there are fewer than around 200 plane-waves per node. It
is usually possible to choose a processor count which allows a highly
parallel run while keeping the number of plane-waves per node
considerably higher than this.

#### band parallelism

From CASTEP version 24.1 band parallelism is implemented for FD
calculations, but not yet DFPT. This may be enabled using a “devel-code”
string in the `.param` file[^24]

> ```
> %block DEVEL_CODE
> PARALLEL:NBANDS=8:ENDPARALLEL
> %endblock DEVEL_CODE
> ```

will attempt to set up 8-way band parallelism in addition to k-point and
g-vector.

[^24]: This activation mechanism will be replaced by a “first-class”
    parameter to set parallelism in future releases of CASTEP. N.B.
    `DEVEL_CODE` is the only `%block` allowed in the `.param` file.

#### perturbation parallelism

From CASTEP release 24.1, a further level of parallelism called
task-farming may be used to distribute perturbations across processors.
This is set up and run in the same manner as for PIMD or NEB
calculations by setting parameters file keyword `num_farms : <n>`. The
value of $n$ should not be too large, as the performance will be limited
by load-balance issues, and in any case never greater than the number of
perturbations. This will produce $n$ output files named

> `<seedname>_farm00<n>.castep`

instead of the usual, single `.castep` file. Of these,
`<seedname>_farm001.castep` will contain the calculated final
frequencies, Born effective charges etc. but a single instance of the
`.phonon`, `.efield`, `.phonon_dos` and `.check` files are written as
with other parallel schemes.

#### hybrid OpenMP parallelism

In addition to the above-described parallel distribution strategies -
all based on MPI parallelism, CASTEP also offers a degree of OpenMP
parallelism[^25]. This can speed up some operations such as matrix
diagonalisations and is activated by setting the environment variable
`CASTEP_NUM_THREADS : <n>` where $n$ in the range 2-16 is most effective
(only a modest speed-up is accessible using OpenMP). However this can
give a useful gain in addition to MPI parallelism especially in the case
where compute nodes must be underpopulated because of memory
requirements.

[^25]: See [eCSE
    report](http://www.archer.ac.uk/community/eCSE/eCSE01-017/eCSE01-017_Final_Report_technical.pdf)
    for a description of the implementation and benchmark results

### Checkpointing and Restarting {#sec:checkpointing}

Even with a parallel computer, it is frequently the case that a
calculation can not be completed in a single run. Many machines have a
maximum time limit on a batch queue which may be too short. On desktop
machines, run time may be limited by reliability and uptime limitations.
CASTEP is capable of periodically writing “checkpoint” files containing
a complete record of the state of the calculation and of restarting and
completing a calculation from such a checkpoint file. In particular
dynamical matrices from complete q-points, and partial dynamical
matrices from each perturbation are saved and can be used in a restart
calculation. To enable the writing of periodic checkpoint files, set the
parameter

> `backup_interval 3600`

which will write a checkpoint file named *seedname*`.check` every hour
(the time is specified in seconds) or on completion of the next
perturbation thereafter. To restart a calculation, set the parameter

> `continuation : default`

in the `.param` file before resubmitting the job. This will attempt to
read *seedname*`.check` and restart the calculation from there.
Alternatively the full filename of a checkpoint file may be given as
argument to the `continuation` keyword to read an explicitly named file.

At the end of the calculation a checkpoint file *seedname*`.check` is
always written. As with the intermediate checkpoint files this contains
a (now complete) record of the dynamical matrices or force constant
matrix resulting from phonon calculation. This may be analysed in a
post-processing phase using the `phonons` utility.

