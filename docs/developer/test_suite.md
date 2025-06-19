# CASTEP's test suite

## Overview

The CASTEP source distribution includes a test suite to aid developers and users or HPC admins alike by

- Ensuring that new development and refactored code does not cause a crash or significantly change any results;
- Testing a new compiler, or new version of an existing compiler for failures due to language standard support, 
  non-portable code or bugs in the compiler itself;
- Ensuring that serial and parallel execution yield the same results;
- Automating the tests so they may be run as a routine part of
  development, either my the developer or routinely by the "Jenkins"
  Continuous Integration (CI) system.

We adopt the testing method known as *regression testing* whereby
CASTEP is run on a large set of input decks for small calculations,
and the result compared to a previously generated and known good
outputs, known as the *benchmark* for each test. The automation and
testing are performed using the
[`testcode`](https://testcode.readthedocs.io/en/latest/) testing
platform. This handles all of the definition of test categories, the
selection, sequencing and running of tests, and comparison of the run
output with a benchmark. To run CASTEP, postprocess the output and
extract the comparison data, it invokes two scripts supplied in
the CASTEP distribution `bin` directory named [`run_castep_test.py`](#creation-and-format-of-test-outputs-and-benchmarks) and
[`extract_results.pl`](#extraction-of-properties).

The directory structure of the suite consists of a top-level `Test` directory containing testcode's configuration files, a GNU Makefile which contains targets to drive the tests, and a set of subdirectories dividing the tests into categories; in outline

```
Test
 |-- CMakeLists.txt
 |-- Makefile
 |-- jobconfig
 |-- userconfig
 |-- Electronic
         |-- Cr-AFM
			 |-- Cr_00PBE.uspcc
			 |-- Cr_AFM.cell
			 |-- Cr_AFM.param
			 |-- benchmark.out.castep-23.1.castep-python-1.0.python-3.6.9.inp=Cr_AFM.param
         |-- <Electronic test 2> 
|-- <Category 2>
         |-- <Category 2 test 1>
         |-- <Category 2 test 2>
 ...
```

## Testing your code

### A complete test run

A run of the test suite is started by running the testcode script `<CASTEP_ROOT>/bin/testcode.py` from within the Test directory, but as some options are usually required, this is most conveniently invoked via the build system by either

```Shell
    cd Test
    make check
```

or

```Shell
    cmake -t check
```

following a compile with either the GNU make or cmake build systems. This will produce a brief summary output along the lines of

```Shell
make check COMMS_ARCH=mpi
Found mpirun, using PARALLEL_CMD=mpirun -np tc.nprocs
rm -f */*/*.castep */*/*.dfpt_wvfn */*/*.fd_wvfn */*/*.wvfn.* */*/*.*.err
../bin/testcode.py -q  --processors=4 --total-processors=36 --user-option castep run_cmd_template "../../../bin/run_castep_test.pl tc.program tc.args tc.input tc.output mpirun -np tc.nprocs" -e /home/user/CASTEP-23.1/bin/castep.mpi -c simple -c d3-simple -c d4-simple -c md-parallel
....................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................... [487/487]
```

if everything passes. If one or more tests fails the corresponding `.` is replaced with a `F` symbol, or an `S` to flag that the test was skipped (possibly because a prerequisite test failed). 

In case of a failed test, more detailed information on which tests failed and why, the commands 
`make compare`, `make diff`, `cmake -t compare`, or `cmake -t diff`
will print a summary or detailed analysis of the failed tests to stdout.  A deeper analysis may require a direct look at the corresponding `<test.out-...>` file, in the `Test/<category>` subdirectory which will contain the `.castep` output as well as the `.0001.err` error/traceback report file in case of an `io_abort`.

### Partial and incremental testing

During a code development process, running the entire test suite to
check every change will be too time consuming and functionally
unnecessary.  The tests are divided into categories, named `spe`
,`bs` ,`geom` ,`md` ,`magres` ,`misc`
,`pair-pot` ,`phonon` ,`otf` ,`pseudo`
,`tddft` ,`ts` ,`xc` ,`nlxc` ,`libxc`
,`solvation` ,`d3` ,`d4` ,`python`
and `parallel` corresponding roughly to the subdirectories

```
Test/
  |-Electronic
  |-Excitations
  |-Geometry
  |-MD
  |-Magres
  |-Misc
  |-Pair-Pot
  |-Phonon
  |-Pseudo
  |-TDDFT
  |-XC
  |-Solvation
  |-Dispersion
  |-Pseudopotentials
  |-Python
  |-Utilities
  |-LibXC
  |-Parallel
```

and may be run individually using

```
    make check-<category>
    make compare-<category>
    make diff-<category>
```

or the targets of the same name in cmake.

??? keyword "Running individual tests"
    In fact the tests may be run at even finer granularity, down to the subdirectory. This is not implemented via the Makefile or cmake, and can only be accessed by invoking `testcode` directly as described [below](#direct-invocation-of-testcode). However the most straightforward means of doing this is to copy and paste the testcode invocation command printed by `make check-spe` including all of the run and argument setup and change the argument of the `-c` option to `<directory>/<subdirectory>`.

### Adding or changing tests

Code sustainability requires that when developing any new functionality or extending existing capabilities, the test suite is also enhanced to test any new outputs.

The changes required are

  * (Optionally) a new test subdirectory. This will be automatically scanned by `testcode` and included if a subdirectory of one of the existing major categories. If the new output is an enhancement or option to an existing functionality, it may be appropriate to simply add the new test to an existing second-level subdirectory.
  * When adding is a major new capability, it may be appropriate to add a new top-level category and subdirectory tree. In that case the [`Makefile`](#adding-to-make) and [`CMakeLists.txt`](#adding-to-cmake) will need to be extended to add the new `check`, `compare`, `diff` and `recheck` targets.
  * CASTEP input files: `.cell` and `.param`
  * If any external pseudopotential files are required, these should be placed in the `Test/Pseudopotentials` subdirectory and a symbolic link made from the test subdirectory. Both the fle and the link should be added to the `git` repository. 
  * to modify [`bin/run_castep_test.py`](#test-outputs-and-benchmarks) if you need to test the contents of a new output file.
  * if testing a new quantity, either in the `.castep` file or any other output file, you must extend the [`bin/extract_results.pl`](#extraction-of-properties) script to scan for and report the new value to be tested.
  * A new stanza in [`jobconfig`](#jobconfig-file) will be required to specify tolerances for the comparison if the defaults in [`userconfig`](#userconfig-file) are not suitable.
  * a new benchmark file containing CASTEP output from a known good
run. Unfortunately creating benchmark files still requires some manual
intervention.  Regrettably `testcode`s option to create a new
benchmark is unsuitable as it is too inflexible to create a single
test without requiring updates to the entire test suite.  The easiest
way to do this is

    a. Run testcode, either from Make or by hand.  The new test will
fail because no benchmark is present for comparison.

    b. Copy or rename the just created test file
`test.out.<date>?inp=<seedname>.param`    to
`benchmark.out.castep-<old-castep-version>castep-python-1.0.python-<old-python-version>.inp=<seedname>.param`.
where `<old-castep-version>` and `<old-python-version>` should be chosen to match the existing `benchmark.out` files from other tests.

### Considerations for choice of new tests.

Tests in CASTEP are generally defined via a short CASTEP run (complete
with `.cell` and `.param` files) which is:

- Sufficient to demonstrate the functionality in question
- Short enough that it does not take significant time to run
- Stable enough that the results do not change significantly from run to
  run.

!!! note

    These calculations do not necessarily need to be physically meaningful
    and in general should not, due to the time requirements.  Under-convergence is usually fine, and often required.

There are two or three common ways to achieve stability of a run with a test which may be underconverged:

1. Set an explicit `random_seed` in the `.param` file
2. Specify k-points using `%BLOCK KPOINT_LIST` rather than use a grid
   or spacing.  This avoids the propensity of the k-point symmetry
   reduction to generate different but equivalent sets depending on
   hardware, compiler options and the like. Usually a very coarse set will suffice.
3. It is frequently counterproductive to use too loose a value for 
   `ELEC_ENERGY_TOL` as the addition or removal of a single SCF iteration between
   benchmark and test can result in a change of, for example, forces sufficient
   to cause a test failure.
   
### Profiling the test suite

A timing profile of the test suite may be generated following a successful run by the GNU make command

```Shell
make profile > profile.log
```

which writes a list of the tests executed sorted by execution time to
the named file. If using `cmake`, the profile is generated
unconditionally and written to a file with extension
`test-profile-all.log` or `test-profile-<category>.log` in the `Test/`
subdirectory.

## Components of test suite

### Direct Invocation of `testcode`

For a serial run, the test suite may be invoked directly from the
command line (with `Test/` as the current directory) by

```Shell
    ../bin/testcode.py -q --total-processors=6 -e <castep-executable> -c simple -c d3-simple -c d4-simple -c solvation-simple
```

where `-q` sets the verbosity to minimal, ` --total-processors=<n>` restricts the maximum number of test to run concurrently, `-c simple` specifies the common core set of tests.  The other `-c` options specify optional components of the CASTEP build, and should be selected to match the libraries linked in to the test executable.  For testing in MPI parallel, the invocation is more complex:

```Shell
    ../bin/testcode.py -q  --processors=4 --total-processors=6 --user-option castep run_cmd_template "../../../bin/run_castep_test.py tc.program tc.args tc.input tc.output -- mpirun -np tc.nprocs" -e <castep-executable> -c simple -c d3-simple -c d4-simple -c solvation-simple -c parallel-simple
```

Here, the testcode option `run_cmd_template` is being explicitly specified, overriding the value in `userconfig` in order to add the `mpirun` option to the `run_castep_test.py` script's options.  Note the quoting of the strings and the use of testcodes's variables `tc.program`, `tc.args`, `tc.input`, `tc.output` and `tc.nprocs` which testcode replaces before invoking the `run_cmd_template` command.  The additional testcode options `--processors=<n>` specifies the maximum number of MPI processes to pass to mpirun, and we add the additional test category `parallel-simple` which contains the MPI tests.

When invoking testcode in this way, the "category" argument of `-c` may be replaced by the name of a subdirectory of `Test`, for example

```Shell
    -c Phonon/Si2-raman
```

which will run only the tests in that subdirectory.

### Test Outputs and Benchmarks

During execution of a test suite run, individual tests are run via a
wrapper script `run_castep_test.py`. This controls the execution of
CASTEP, and gathers up and appends any additional output files generated 
for this particular task.  This concatenated format is used for both the 
test outputs (`test.out-...`) and benchmark files (`benchmark.out-...`). 

The invocation is

```Shell
    run_castep_test.py [-d|--dryrun] -[h|--helpme] <castep-executable> <param-file> <output-file> -- [<mpirun-cmd>]
```

 * `<castep-executable>` is the path to the serial or parallel CASTEP executable.
 * `<param-file>` is `<seed>.param` for the test to run.
 * `<output-file>` is the test output file name; Testcode's  format is of the form `test.out.<date>-<count>.inp=<param-file>`
 * `<mpirun-cmd>` is optional followng the end of other arguments marked by `--`. This is the command that `run_castep_test` will invoke to execute `<castep-executable>` in parallel - usually `mpirun -np <nprocs>`.

### Extraction of Properties

The `extract_results.pl` script is invoked by `testcode.py` to process both 
the test (`test.out-...`) and benchmark  (`benchmark.out-...`) files and extract 
the specific output data for comparison.
It can extract the following properties

??? Known-Properties

    Those in `code-style` are the names for the properties,
    those without are just divisions used here

    - `Energy`
    - `PS_Energy`
    - `FreeEnergy`
    - `SolvationEnergy`
    - `dEtot/dlogE`
    - `Spin`
    - `AbsSpin`
    - `Force`
    - `Stress`

    - Phonons

        * `Phonon-q`
        * `Phonon`
        * `Grad_q(f)`
        * `Freq`
        * `g(f)`
        * `ir`
        * `Raman`

    - Born

        * `Species`
        * `Ion`
        * `Born`

    - Permittivity

        * `Polarisability`
        * `Permittivity`
        * `epsilon(f)`

    - `NLO_Chi2`
    - Raman

        * `Raman_Tr`
        * `Raman_II`
        * `depolarisation`

    - `Electric_constants`
    - `Compliance_mat`
    - Mulliken Populations

        * `Species`
        * `Ion`
        * `s`
        * `p`
        * `d`
        * `f`
        * `Total`
        * `Charge`

    - Hirshfeld populations

        * `Species`
        * `Ion`
        * `Hirshfeld`
        * `Spin`

    - `ELF Data`
    - elf_fmt

        * `gx`
        * `gy`
        * `gz`
        * `ELF(chi)`

    - den_fmt

        * `gx`
        * `gy`
        * `gz`
        * `density`

    - chdiff_fmt

        * `gx`
        * `gy`
        * `gz`
        * `diff-den`

    - pot_fmt

        * `gx`
        * `gy`
        * `gz`
        * `potential`

    - Band Structure

        * `kx`
        * `ky`
        * `kz`
        * `weight`
        * `Eigenvalue`

    - MD Data

        * MD Labels from the block

    - magres

        * `cs_iso`
        * `cs_aniso`
        * `cs_eta`
        * `Cq`
        * `eta_q`
        * `hf_iso`
        * `FC`
        * `SD`
        * `PARA`
        * `DIA`
        * `TOT`

    - `TDDFT_Eigenvalues`
    - Hugoniostat

        * `H-Compression`
        * `H-Temperature`
        * `H-Pressure`
        * `H-Energy`

    - `EFermi`
    - xrd_sf

        * `h`
        * `k`
        * `l`
        * `Re(...)`, `Im(...)` from output file



#### `userconfig` file

This is one of the two configuration files read by testcode ([documentation](https://testcode.readthedocs.io/en/latest/userconfig.html)) and sets up the testcode default options including the run commands to invoke CASTEP via the `run_castep_test.py`  script in serial and parallel.

It also contains the default tolerances for each individual property, which may be overridden on a per-test basis in the `jobconfig` file.

#### `jobconfig` file

The second of testcode's configuration files ([documentation](https://testcode.readthedocs.io/en/latest/jobconfig.html)) specifies the category- and test-specific quantities including overrides for the default property tolerances, and specifications of the parallelism required.

The structure of the `jobconfig` is as follows:

``` INI
# Run all tests on this folder and all subfolders with the given settings.
[Electronic/*]
run_concurrent = true # (1)
tolerance = (0.015,  None, 'Spin') # (2)

# Override the settings of the general folder for a specific case.
[Electronic/Si2-fine-grid]
tolerance = (0.0003, None, 'Energy'), (0.0003, None, 'PS_Energy')

[categories]
spe-simple           = Electronic/*
bs-simple            = Excitations/*
phonon-simple        = Phonon/*
...
simple               = spe-simple bs-simple phonon-simple [...]
...
```
!!! note

    The `<path_to_tests>` can contain wildcards, or absolute paths

!!! note

    All paths are relative to the location of `jobconfig` in CASTEP's
    case that is the `<root>/Test`


At the end of the `jobconfig` file, there is a section called `categories` which
contains the list of categories testcode knows about. The structure is:

``` bnf
<category_name> := <path_to_tests>|<other categories>
```

1. Enable running tests within this folder in parallel.
2. Set the tolerance for a given [property](#valid-properties).

### Adding to the Build System

#### Adding to CMake

To add the tests to be compatible with the [CMake build system](build-system.md#cmake) you need to modify the `CMakeLists.txt` at
`Test/CMakeLists.txt` and add the category to the list on line 157, which looks like:

``` CMake
foreach (CASTEP_TEST_CATEGORY "spe" "bs" "phonon" ...)
  ADD_CATEGORY_TARGETS(${CASTEP_TEST_CATEGORY} TRUE)
endforeach()
```

#### Adding to Make

To add the tests properly to the [GNU make build system](build-system.md#gnu-make) you need to modify the `Makefile` at
`Test/Makefile` and add the category in several places.

Add it to the list of `.PHONY` :

``` Make
.PHONY: check check-simple check-spe-simple ...
```

and create an entry in the appropriate lists for each of the five classes of test jobs:

1. `check`
2. `recheck`
3. `benchmark`
4. `compare`
5. `diff`


to call your tests when the target is called e.g.:

``` Make
check-solvation: exe-exists prepare-clean
    $(TESTCODE) $(QUIET_FLAG)  $(PARALLEL) -e $(CASTEPEXE) -c solvation-simple
```

!!! note

    `exe-exists` and `prepare-clean` are to ensure that CASTEP is compiled and that
    any old test runs are cleared out before starting the tests.
