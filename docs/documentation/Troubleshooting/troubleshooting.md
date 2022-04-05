## CASTEP fails to start ##

### Command not found ###

If you see a message like this on the command-line when you run CASTEP:
```
castep mytest
castep: command not found
```
then your computer has not located the CASTEP program. Check that:

- you've used the correct CASTEP name (`castep.serial` or `castep.mpi`)
- the CASTEP program is somewhere your computer expects programs to be

[See here](linux_path.md) for details of where Linux looks for programs, and how to change it.

## CASTEP aborts a calculation ##

If CASTEP detects a serious problem, it will stop and write an error message to a `.err` file. If you are using the parallel version of CASTEP on many cores, you may see error messages from each of these cores. They are named using the same seedname, but with the process ID added, e.g. if CASTEP is run on 2 cores and a serious problem occurs, you might see the files
```
mytest.0001.err
mytest.0002.err
```
These files contain useful information about what went wrong, so it is always worth looking at them.

### Failed to converge ###

