One of the most fundamental tasks for CASTEP is to take a crystal lattice and set of atomic positions, and compute the electronic density and total energy.

Once the [lattice and atomic positions](/documentation/Getting_Started/basic_cell_file) have been specified, you can tell CASTEP to compute the energy by setting the task keyword in [the param file](/documentation/Getting_Started/basic_param_file):

```
task : energy
```

Your cell and param files should be named using the same prefix, which CASTEP calls the "seedname", and the extensions `.cell` and `.param`, respectively. For example, for a calculation called `mytest`, you need the input files
```
mytest.cell
mytest.param
```
and the calculation is run with the command
```
castep mytest
```



CASTEP computes the energy by solving the Kohn-Sham equations iteratively, using the 'self-consistent field' (SCF) method.
