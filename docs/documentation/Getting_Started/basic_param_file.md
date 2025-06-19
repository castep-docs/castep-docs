This is a basic overview of the param file. See the [full param file page](../Input_Files/param_file.md) for more details.

The param file is one of CASTEP's two main input files. It contains all of the information about the kind of simulation your wish CASTEP to perform, as well as details of how CASTEP should perform them and additional simulations and analyses.

The file itself is a free-format keyword-driven text file, consisting largely of single-line keywords, although there are a small number of blocks of information. These may be given in any order, with blocks indicated by the special `%block` and `%endblock` markers. All of the keywords and blocks are optional, but you will almost always want to change at least some.

## Task ##

This keyword controls what CASTEP's simulation task is. The default is

```
task : energy
```
which tells CASTEP to compute the ground state electronic energy and density for the input set of atoms from [the cell file](basic_cell_file.md).

## Cut-off energy ##

The plane-wave cut-off energy controls how large CASTEP's basis set is for representing the wavefunction. Higher values mean more plane-waves and a better representation of the wavefunction, but this consumes more computer RAM and the calculation will take more time. CASTEP calculations are always a compromise between the accuracy you require, and the computational resources the simulations will use. The cut-off energy you need will also depend on the [pseudopotentials](../Pseudopotentials/overview.md) you're using in the [cell file](basic_cell_file.md). You can choose from some preset values using the `basis_precision` keyword:

```
basis_precision : coarse|medium|fine|precise
```
i.e. you can choose to set `basis_precision` to `coarse`, `medium`, `fine` or `precise`.

The settings `coarse` and `medium` are usually only suitable for quick preliminary investigations, and for research simulations you will usually want to set it to `fine` or better.

For more control over the cut-off energy, the `cut_off_energy` keyword may be used instead:

```
cut_off_energy : 500 eV
```
Typical cut-off energies are in the range 300 to 1500 eV.

## XC functional ##

Density functional theory is exact in principle, except for the exchange-correlation (XC) functional which must be approximated. There are many different functional forms to approximate this, and in CASTEP you select it with the `xc_functional` keyword, for example:

```
xc_functional : pbe
```
which selects the PBE functional of Perdew, Burke and Ernzerhof.
