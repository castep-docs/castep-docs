# Adding Tests

Following the addition of a new feature or bugfix it is essential to
add system and unit tests that demonstrate the functionality of said
addition.

This document describes the process of adding new tests to the system
as well as implementing your own testing groups.

!!! warning

    Before any code is accepted into CASTEP it must have tests to
    prove its functionality and robustness.

## `testcode`

CASTEP's test suite is built using the
[`testcode`](https://testcode.readthedocs.io/en/latest/) testing
platform. This handles all of the generation of benchmarks and
comparisons in the test suite.

### Valid Properties

CASTEP's `extract_results.pl` can extract the following properties
from the `.castep` files:

??? note

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


## The Test folder structure

The CASTEP test folder is structured as follows:

```
Test
 |- CMakeLists.txt
 |- jobconfig
 |- userconfig
 |- README
 |- List
 |- Electronic
  |- Cr-AFM
   |- Cr_00PBE.uspcc
   |- Cr_AFM.cell
   |- Cr_AFM.param
   |- benchmark.out.castep-23.1.castep-python-1.0.python-3.6.9.inp=Cr_AFM.param
  |- ELF
  |- Electrostatics
  ...
 |- XC
 ...
```

The key files in the `Test` directory are:

`CMakeLists.txt`

:   CMake source file to build test suite in CMake (see: build_system
    and [Adding tests to be run](#adding-tests-to-be-run))

`jobconfig`

:   Essential file for `testcode` which defines the jobs, tolerances and
    categories of tests.

`userconfig`

:   Essential file for `testcode` which defines the
    commands to run tests and where to look for benchmarks.

`README`

:   Brief documentation detailing the purpose of the test
    suite and how to construct tests.

The tests themselves are generally structured in the folder tree by a
folder representing the general category of the tests and then a
sub-folder for the specific test case. It is, however, possible to
have multiple test cases within these sub-folders.

The structure is used by testcode to determine which properties to
check with which tolerances.

## Adding Tests

### Defining new tests

#### What do tests look like?

Tests in CASTEP are generally defined via a short CASTEP run (complete
with `.cell` and `.param` files) which is:

- Sufficient to demonstrate the functionality in question
- Short enough that it does not take significant time to run
- Stable enough that the results do not change significantly from run to
  run.

!!! note

    These calculations do not necessarily need to be physcially meaningful
    and in general should not, due to the time requirements.

#### Adding tests to be run

`testcode` runs tests according to two files contained in the [`Test`
directory](#the-test-folder-structure).

##### `userconfig`

To add tests you should not need to touch `userconfig`, so we can
ignore that here.

##### `jobconfig`

If we are adding a new test folder we need to modify `jobconfig` to
include the new test folder, as well as define tolerances on the
various properties we might measure within the tests.

The structure of the `jobconfig` is as follows:

``` INI
# Run all tests on this folder and all subfolders with the given settings.
[Electronic/*]
run_concurrent = true # (1)
tolerance = (0.015,  None, 'Spin') # (2)

# Override the settings of the general folder for a specific case.
[Electronic/Si2-fine-grid]
tolerance = (0.0003, None, 'Energy'), (0.0003, None, 'PS_Energy')

```

1. Enable running tests within this folder in parallel.
2. Set the tolerance for a given [property](#valid-properties).

#### How to ensure stability

CASTEP tests generally want to have a fixed seed using:

```
rand_seed: 1234567890
```

!!! note

    The actual value of the `rand_seed` doesn't matter, only that
    it is fixed.

The test should also generally be a short run of a small crystal structure to
avoid any potential noise accumulating in the answer. The run does not need
tight tolerances on $E_{\text{cut}}$ or $\mathbf{k}$-point meshes, only
sufficient to ensure that the answer produced is not noise itself.

### Adding Test Groups

#### Adding to `jobconfig`

At the end of the `jobconfig` file, there is a section called `categories` which
contains the list of categories `testcode` knows about. The structure is:
``` bnf
<category_name> := <path_to_tests>|<other categories>
```

!!! note

    The `<path_to_tests>` can contain wildcards, or absolute paths

!!! note

    All paths are relative to the location of `jobconfig` in CASTEP's
    case that is the `<root>/Test`

Example format of the categories

``` INI
[categories]
spe-simple           = Electronic/*
bs-simple            = Excitations/*
phonon-simple        = Phonon/*
...
simple               = spe-simple bs-simple phonon-simple [...]
...
```

#### Adding to CMake

To add the tests to be compatible with the CMake build system (see: [build
system](developer/build-system.md)) you need to modify the `CMakeLists.txt` at
`Test/CMakeLists.txt` and add the category to the list on line 157, which looks like:

``` CMake
foreach (CASTEP_TEST_CATEGORY "spe" "bs" "phonon" ...)
  ADD_CATEGORY_TARGETS(${CASTEP_TEST_CATEGORY} TRUE)
endforeach()
```

#### Adding to Make

To add the tests properly to the Make build system (see: [build
system](developer/build-system.md)) you need to modify the `Makefile` at
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
