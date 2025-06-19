CASTEP has two main input files, called [the cell file](basic_cell_file.md) and [the param file](basic_param_file.md). The cell file defines the structure of the material (or molecule) you wish to study, and the param file defines the kind of simulation CASTEP should perform.

The cell and param files should be named using the same prefix, which CASTEP calls the "seedname", with the extensions `.cell` and `.param`, respectively. For example, for a calculation called `mytest`, you need the input files
```
mytest.cell
mytest.param
```
and the calculation is run with the command
```
castep mytest
```
The main CASTEP output file will be names using the same seedname and the `.castep` extension, i.e. in the above example it would be called `mytest.castep`. If this file already exists, CASTEP will append its output to it.

When CASTEP completes successfully, it writes additional files such as the `.bib` file, which contains references to key papers for the theory and methods CASTEP used.

If CASTEP encounters a serious problem, it will stop and write an error message to a `.err` file. If you are using the parallel version of CASTEP on many cores, you may see error files from each of these cores. They are named using the same seedname, but with the numeric process ID added, e.g. if CASTEP is run on 2 cores and a serious problem occurs, you might see the files
```
mytest.0001.err
mytest.0002.err
```
These files contain useful information about what went wrong, so it is always worth looking at them. See the [Troubleshooting Guide](../Troubleshooting/troubleshooting.md) for details of how to find and fix common problems.
