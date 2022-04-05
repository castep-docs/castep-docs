CASTEP is a software package to calculate the properties of materials. It is based on quantum mechanics, in a form known as density functional theory, and can simulate a wide range of materials proprieties including energetics, structure at the atomic level, vibrational properties, and many experimental characterisation methods, such as infra-red and Raman spectra, NMR, and core-level spectra.

### This documentation ###

This documentation focuses on using CASTEP at the command-line, as a stand-alone program. You can build two versions of CASTEP: a "serial" version called `castep.serial`, which is primarily designed to run on a single CPU core; or a parallel version called `castep.mpi`, which uses the message passing interface (MPI) to run on more than one core. Most of this documentation applies equally to both versions, but for simplicity we will focus on the serial version in most of the examples.

We will refer to the CASTEP command itself as `castep`, which you will need to change to `castep.serial` or `castep.mpi`, as appropriate.

In this documentation, anything in a fixed width font `like this` is text to type, either on the command-line or in a CASTEP input file. For CASTEP's input files, there is sometimes a choice between different settings, and this will be indicated using the `|` symbol, meaning "or". For example,
```
setting : choice_1|choice_2|choice_3
```
If some of the entries are optional, they will have square brackets around them `[like this]`, for example:
```
setting : choice_1|choice_2|choice_3 [unit of choice]
```
