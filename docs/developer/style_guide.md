## Introduction

The CASTEP code has been designed from conception to achieve various goals -
including efficiency and maintainability. The following are some simple
guidelines on writing code for inclusion within CASTEP. These are intended to
enable the writing of correct, efficient code, and to ensure a consistent style
for multiple authors throughout the code that is straightforward for others to
maintain in the future. Fortran 2003 has been chosen as the language that all
the code will be written in, as it has many modern features which enable the
writing of clean, modular code without compromising efficiency and portability.

In this document, there is a [template for writing modules](#template), and for
writing subprograms within a module. These templates are designed to enforce
good programming practice and documentation of routine function and
side-effects.  It is important that all routines be written with these
templates. The general guidelines about style addressed here, the use of module
templates, the completeness of the documentation, etc. all help to make writing
new code and maintaining the existing code a simple task.

It is also the programmer's responsibility to ensure that each routine is coded
as efficiently as possible. Whilst it is tempting to use some of the new
built-in features of Fortran 2003, experience has shown that discretion is
required in their usage so as not to compromise efficiency. Therefore,
guidelines on the use of such features has also been included.

## CASTEP linter

The CASTEP linter is a Python tool which checks your CASTEP build for any issues
related to the CASTEP style. It should be used after making any major
modifications.

!!!note

    The linter is also run on the CASTEP CI system and will warn you if any new
    issues arise from your modifications. Should any new issues be in your PR, it
    may not be accepted.

### Using the CASTEP linter

The linter is available on [PyPI](https://pypi.org/project/castep-linter/) and
can be installed on your system using `pip`:

```shell
python -m pip install castep-linter
```

Following the install, it should be possible to run the linter by running:

```shell
castep-lint <file>
```

e.g.

```shell
castep-lint Source/Functional/pair_pot.f90
```

For further information, type

```shell
castep-lint -h
```

It is also possible to use the CASTEP linter in
[emacs](https://www.gnu.org/software/emacs/) through a [`flycheck`
extension](https://github.com/byornski/castep-linter/blob/main/utils/flycheck-castep.el). To
use this you must install the `flycheck` package which can be done through the
[`MELPA`](https://melpa.org/#/getting-started) emacs package repository.


## Writing to the Specification Document


### "It does exactly what it says on the tin"

Obviously, it is of paramount importance to make sure that any routine that you
are responsible for does exactly what the specification says that it should do,
particularly with regard to exit conditions, side-effects, etc.

Routines and variables that are covered by the specification are `public` whilst
other routines and variables are `private`. The specification says nothing about
the rôle or meaning of private routines. Private routines and variables are
only accessible within the module in which they occur.


### Do not assume anything that is not written in the specification document

If the specification does not say that a particular routine will preserve the
input values on exit, then you cannot presume that whoever coded it will do
likewise! Even if that routine was written by you...

Similarly, it may seem obvious that a particular variable has a particular
meaning, but if it is not defined in the specification, then it cannot be
presumed. Future revisions of the code may change non-specified routines
freely. If all code sticks to the specification at all times, then maintaining
the code is much simpler.

Note that the specification does not say anything about private routines or
variables in any module. For this reason, great care must be taken when using
such routines. The [subprogram template](#template) is there to remind you to
document all side-effects of each routine!


### Code robustly for errors

That is, the user should never see a Fortran run-time error message - your code
should check for possible error conditions, and either correct the error or
print a nice, meaningful error message and do a graceful exit via `io_abort`.


### Conditions on execution

Conditions given in the specification must be true for correct execution of each
routine. Obviously, these should be tested for to ensure correctness, but this
may introduce a considerable performance penalty, particularly for `Utility` or
`Fundamental` routines. For this reason, it is recommended to use a single
`#ifdef debug` block at the start of each routine to test these conditions where
appropriate and call `io_abort` as necessary. The code can then be compiled
either with or without full error checking as appropriate.


## Errors and Warnings


### Use `stderr` from any node

Unlike normal messages, any node can write an error or warning message. Any
such message is to be written to `stderr` from the relevant node. The
routine shall then call `io_abort` to terminate the program neatly.


### Use `iprint` consistently

Normal output, including warning messages and debugging information, should
only by written to `stdout` by the root node. The level of detail is
controlled by the `iprint` variable:

- `0` -  Minimal output - just the basic parameters controlling the run and
  the answers!

- `1` - Default output - breakdown of energies and forces into components,
  etc. but no debugging output.

- `2` - Minimal debugging - values of all significant parameters, etc. Not
  printing all the arrays.

- `3` -  Maximal debugging - the works!

## Efficiency Issues


### Libraries

The use of BLAS and LAPACK libraries are recommended, as these are freely
available libraries and often come in vendor-optimised versions for each
platform. For efficiency, it is also recommended that you do not use BLAS "level
0 routines" as there are little efficiency gains to be made, and the equivalent
fortran is often much neater and easier to read.


### Fortran array intrinsics

Beware the use of fortran array intrinsics - they can be inefficient and may cause
memory problems, e.g. `result=matmul(a,matmul(b,c))` requires an implicit
dynamic memory allocation. Wherever practical use BLAS instead. Some intrinsics
may also impede compiler optimisation, particularly on a vector
machine. Similarly, do not use functions such as `transfer` or `mold` - these
can be very inefficient.


### Passing arrays to subprograms

This is a tricky subject, which can easily lead to confusion and inefficient
code. The main problem is that there are multiple ways of passing arrays, and
these are not in general equivalent!

The best practice is to always pass the whole array together with its size, such
as:

```fortran

call foo(int_array, N1, N2)
...

subroutine foo(int_array, N1, N2)
implicit none
integer, intent(in) :: N1, N2
integer, dimension(1:N1, 1:N2) :: int_array
...

```

as this does not cause any copying of the array and allows the compiler to do
bound-checking etc.

The use of **assumed-shape arrays**, such as `int_array(:, :)` is less efficient
as this has an explicit rank, but an implicit shape. This requires the use of
functions such as `size(int_array,1)` and may prevent certain compiler
optimisations. However, it does allow the compiler to do bound-checking.

Care must be taken in passing the array though. If an array section is to be
passed then it is much better to use **assumed-size arrays** (i.e. the old
fashioned way), that is

```fortran

call foo2(int_array(1, N))
...

subroutine foo2(int_array)
implicit none
integer, dimension(*) :: int_array
...

```

than to pass `int_array(:, N)` and receive `int_array(:)` as this will create a
copy of the array on the stack which will rapidly lead to "out of memory"
errors.

The use of assumed-size arrays, such as `int_array(*)` is useful if you want to
write a general purpose routine that will work with any size and/or rank
array. Note however, that it will not in general work with scalars, nor does it
allow bounds-checking. However, it does not cause the creation of any copies of
the array.


## Machine-Specific Code

### Avoid!

Write in standard fortran without vendor extensions and without using any system
routines wherever possible, for maximum portability. The one exception that is
allowed to this is in the `Utility` modules, where all the low-level
input/output and communications are handled.


### Test thoroughly to prevent

Always test your routines on several different platforms and with several
different compilers to be sure that you have not inadvertently relied upon some
default behaviour of one specific compiler. The CI system will handle
compilation for all supported compilers once submitted as a merge request into
the Bitbucket repository, but these should be performed beforehand to minimise
the effort in bugfixing.


### File handling

One obvious area of machine dependency is that of file handling. For this reason,
the `io` module should be used to handle the opening of all files. The programmer
is responsible for reading / writing the data and closing the file. Files are
not to be kept open for any longer than strictly necessary.


### Compiler/preprocessor directives

These should be avoided wherever possible as they hinder portability. They
should only be used in the `Utility` modules for machine specific code. All
module filenames should be given the extension `.f90`, with the exception of
`Utility` modules, where `.F90` is permitted, but generally only if
preproccesing is used.


## Fortran90 Features


### Use of dynamic arrays

Each routine is responsible for allocating/using/deallocating its own workspace.
We recommend that such `allocate`/`deallocate`s only occur once in a routine -
never inside a loop as this will produce a significant performance penalty. You
must ensure that you always `deallocate` local work arrays on termination of the
routine. Obviously, care needs to be taken if there are multiple exit points
from a routine.


### Pointers

Always accept passed arrays in subprograms as arrays and not as pointers. This
will force automatic dereferencing of the array and enable better optimisations
by the compiler.


### Flow of control

Use of constructs such as `select case` and `do ... end do`, with labelling of
"do loops", etc. is recommended for clarity. Use of `cycle` and `exit` is OK -
but only use to move a maximum of one level of nesting where possible. Do NOT
use `goto`.


### Functions

A function subprogram should be "pure", i.e. generate no side-effects through
modification of variables in argument list or module variables through "use
association". Avoid recursion.


### Use of `use`

Use modules with an `only` clause if only a small number of variables
required. Put appropriate `use` statements into each subroutine required, NOT
into the module header, in order to keep track of module variable modification.


### Line numbers

Avoid where possible. Line numbers are only to be used for format statements,
and `end=` or `err=` in file handling. Do not use `continue`.


### General features

Avoid multiple statement lines unless trivially simple.


## Modules


### General

All code is to be contained within modules.


### Usage

Each module described in the specification is to be one source file. All
routines given in the specification for this module are to be in this file.


### Auxiliary modules

CASTEP also encourages the use of the more recent (Fortran 2008)
`submodule`s. Submodules allow the programmatic subdivision of a module enabling
the compiler to precompile interfaces, reduce required compilation if only the
submodule has changed and allowing the developer to more effectively control
scope of module internals.

For clarity, and to keep the module from being excessively long, the module may
also use auxiliary modules, which can be in separate files (again with one file
per module). Any auxiliary modules must be used in only one specified module,
i.e. no auxiliary code reuse in other specified modules as the auxiliary
routines are not specified!

The naming convention of any auxiliary modules is to be inherited from the
specified module to make it clear where the auxiliary routines are to be used,
e.g. if the specified module is called `me.F90` with routines called `me_sub`,
etc. then an auxiliary module would be `me_extra.F90` with routines called
`me_extra_sub`, etc.

!!! note

    Rather than using full auxilliary modules in modern CASTEP, `submodule`s are
    encouraged.


## Style and Layout


### Use the module template

[The module template](#template) gives the recommended layout for a module and
for a subprogram. This is available in the CASTEP source at
`Source/template.f90`. In particular, note the layout and contents of the
comment header, and the order of declarations. Everything is to be private
unless explicitly specified as public! This also makes it simple to check the
code against the specification.


### Layout

All code is to use indentation as generated by GNU-Emacs f90-mode. Use any
editor you like to create the code, but please ensure that whatever goes into
the Bitbucket repository has been passed through Emacs f90-mode indentation at
the finished stage. To assist in Emacs usage, [the module template](#template)
contains Emacs directives to set f90-mode, etc.


### Case

Use lower case for keywords and use capitalisation as given in the specification
for all routines and variables mentioned therein. For private routines and variables
use lower case in general. However, you may use upper case to differentiate
words within a name, e.g. `userInputData` - as long as you are consistent
throughout the module.

Use upper case, with stripped spaces, for the value of string variables that are
passed between routines, e.g. `run_type='MOLECULARDYNAMICS'` not
`'MolecularDynamics`' or `'molecular dynamics'` etc. to simplify string
comparisons.


### Names

For clarity, don't change variable name on passing to a different routine
wherever possible. Avoid short (1 or 2 letter) variable names except for simple
loop counters. Use new form `end subroutine name` etc. not older form
`end subroutine`.


### Types

Do NOT use implicit typing. Similarly, you do not have to stick to the old rules
for implicit typing - you can have integer names beginning with "`c`" etc! Do
not give type as `double precision` - use `real(kind=dp)` instead, as `dp` is a
constant in the Constants module and this will make porting to other
architectures (e.g. Cray) much simpler. Remember that all machine-specific code
stays in the Utility routines. Similarly, when declaring a constant, use
`1.234_dp` NOT `1.234d0`.


### Free format

Use free-format f90, with a maximum line length of 132 characters.


### Spaces

Use spaces between keywords e.g. `end if` not `endif`.


### Code cleanly

Obviously, to ensure correctness and make it easier for others to maintain the
code. If the obvious way to code a routine is inefficient, whilst the efficient
way is obscure, then this is allowed as long as the routine is well documented
internally, with a discussion as to the design decisions made.


### Be aware of vectorisation

When coding, be aware that the code is almost always executed upon vector
architectures.  Therefore code with a style that enables good vectorisation -
e.g. don't put `if` statements inside nested loops wherever possible.


## Documentation


### Internal

Each module, based upon [the module template](#template), is to have a header block
describing its overall purpose and function.

Each routine, written to the template, is to have a header block describing
its function, the variables required and how modified, the necessary conditions
for correct operation, etc. These comments should be clear and easy to understand.

Each routine is also to contain lots of comments within the code. Comments are
to be either on the same line(s) as the feature being comment upon, or in a
block of lines above the feature.

Comment density should be comparable to code density.

All comments are to be in English and obey standard rules of English grammar.


### External

A module (or any modifications) is only considered complete when additional
documentation has been supplied for inclusion. Documentation must be provided in
the appropriate module and function header blocks, explaining the function of
the module and each routine, the physics behind the code, the algorithms used,
the key variables and data structures, and appropriate references to the
literature.

## Testing


### Test Program

Each module shall be tested for correctness before being added to the Bitbucket
repository. To this end a set of tests shall be provided, which must compile and
execute correctly in the CI system. The purpose of these tests is to verify the
correct operation of every specified routine in the module.

CASTEP uses the [`testcode`](https://testcode.readthedocs.io/en/latest/) testing
platform which allows automated generation of benchmark data from a set of valid
CASTEP input files.

Please see [Testing](adding_testing.md) for more information on how to do this.


### Reference data

The module test program shall come with both appropriate input datafiles and
reference output results. Correct operation of the test shall be verified by
comparing the actual output against the reference output results.


## Module Template

### General

Note particularly the order of declaration, use of `implicit none` and
`private`, and the standard comment header, for internal documentation.  All
lines in comment headers are to be 80 characters wide. Not all sections of the
header will be relevant to all subprograms and so can be deleted. It is very
important that the header is kept up-to-date and as complete as possible.


### Use of `public` and `private`

Each module uses an initial `private` statement to force all entities
in the module to be private by default. Then have explicit `public` statements
to expose those datatypes, variables and (overloaded) routine names, as listed
in the specification document. This makes it easy to compare the code to the
specification document.


### Template

```fortran
! -*- mode: F90 ; mode: font-lock ; column-number-mode: true ; vc-back-end: git -*-
!=============================================================================!
!                          D U M M Y                                          !
!=============================================================================!
! Overall explanation of purpose and function of module.                      !
!                                                                             !
!-----------------------------------------------------------------------------!
! Written from  "Module Specification for New Plane Wave Code",  M. Segall,   !
!    P. Lindan, M. Probert, C. Pickard, P. Hasnip, S. Clark and M. Payne      !
!                           Copyright 1999/2000                               !
!-----------------------------------------------------------------------------!
! Written by author, version, date                                            !
!-----------------------------------------------------------------------------!
!                                                                             !
!                                                                             !
!=============================================================================!

module dummy
  use constants, only : dp                      !Minimal useage where practical

  implicit none                                 !Impose strong typing
  private                                       !Everything is private ...

  !---------------------------------------------------------------------------!
  !                       P u b l i c   R o u t i n e s                       !
  !---------------------------------------------------------------------------!
  public :: routine_name ...                    !... unless exposed here.
  interface routine_name                        !Overloaded routines, etc.
     ...                                        !(specific names are private)
  end interface

  !---------------------------------------------------------------------------!
  !                        P u b l i c   V a r i a b l e s                    !
  !---------------------------------------------------------------------------!
  public datatypes ...
  public variables ...

  !---------------------------------------------------------------------------!
  !                      P r i v a t e   R o u t i n e s                      !
  !---------------------------------------------------------------------------!


  !---------------------------------------------------------------------------!
  !                      P r i v a t e   V a r i a b l e s                    !
  !---------------------------------------------------------------------------!

  datatypes ...                                 !Private data for all routines
  variables ..                                  !in this module ...
  ...

contains
  subroutine public1(var1,var2,...)
    !=========================================================================!
    ! Explanation of purpose of routine                                       !
    ! ...                                                                     !
    !-------------------------------------------------------------------------!
    ! Arguments:                                                              !
    !   var1, intent, meaning                                                 !
    ! ...       (in order of call list)                                       !
    !-------------------------------------------------------------------------!
    ! Parent module variables used:                                           !
    !   globalvar1, meaning                                                   !
    ! ...                                                                     !
    !-------------------------------------------------------------------------!
    ! Modules used:                                                           !
    !   other_module used,                                                    !
    !   other_vars, meanings, changes                                         !
    ! ...                                                                     !
    !-------------------------------------------------------------------------!
    ! Key Internal Variables:                                                 !
    !   intvar1, meaning                                                      !
    ! ...                                                                     !
    !-------------------------------------------------------------------------!
    ! Necessary conditions:                                                   !
    ! ...                                                                     !
    !-------------------------------------------------------------------------!
    ! Written by author, version, date                                        !
    !=========================================================================!
    use my_module, only : some_other_function
    use other_module, only : other_var1
    implicit none

    integer, intent(in), dimension(:,:) :: var1        !Variables in call order
    real(kind=dp), intent(in), parameter :: var2
    ... (other variables in call list)

    real(kind=dp) :: my_var1=2.7182818_dp             !base of natural logs
    complex(kind=dp), allocatable, dimension(:) :: my_work1
    ... (other internal variables)

    ... (condition checks)
    ... (actual code)

    return
  end subroutine public1

  ... (other public subroutines)

  subroutine private1(....)
    !=========================================================================!
    ! Explanation of purpose of routine                                       !
    ! ...                                                                     !
    ! (etc, as for public routines)                                           !
    !=========================================================================!
    ....
  end subroutine private1

end module dummy
```
