##Check-pointing, Continuation and Parameter Changes

As with any other calculation in CASTEP, checkpoint files
are written at regular intervals. Should the calculation
be interrupted for whatever reason, it is possible to
continue from the point at which a checkpoint file
was written.

Check-pointing is performed by dumping all pertinent
data to a .check file. The interval at which this
check-pointing occurs can be controlled in two ways.

The first option is to specify the number of md steps
between checkpoints.

```
num_backup_iter = 5
```

Alternatively, the wall-clock time (in seconds) between backups
can be specified with:

```
backup_interval = 60
```

Both intervals can be used, i.e. a checkpoint file could be
written every 60 seconds and every 5 MD steps. To disable
either interval, set the corresponding parameter to zero.

The name of the checkpoint file will be the calculation seed-name
followed by ``.check``. This can be overridden with:

```
checkpoint   = my_md_run.check
```

To continue an MD calculation from a checkpoint file, ensure
that the .check file, the .castep file and the .md file
from the previous run are present in the current directory. If the
seed-name of the new run is the same as for the old, the command

```
continuation = default
```

will suffice. To continue the run from a checkpoint file
``my_md_run.check`` use:

```
continuation = my_md_run.check
```

####Changing Parameters on Continuation

Check-pointing is particularly useful for MD calculations where
we often require many thousands of time-steps to extract
useful information. Another important benefit is the ability
to halt a calculation, and continue from a checkpoint with
a revised set of MD parameters. For example one may wish
to alter the target thermostat temperature, or the
cell relaxation time without having to restart the run from the unequilibrated
configuration.

All options described in the above sections can be changed on a restart, i.e.
it is possible to change ensemble, thermostat and barostat schemes, relaxation
times, time-step, constraints e.t.c by specifying new values in the input files for the new
run. It is not possible to change the number
of atoms/electrons in the cell. Care must be taken when changing parameters
on a restart. For example a large discontinuous change in the specified temperature or
pressure will perturb a system away from equilibrium. In such cases the system
should not be sampled until re-equilibrated.

Although it is possible to change electronic minimisation schemes/parameters
on a restart, this is somewhat unwise for obvious reasons.

##On-The-Fly Parameter Changes

In fact, molecular dynamics parameters can be changed without having to halt
the calculation at all! At the end of each MD step, the parameters file
is re-read. Any parameters in this file which differ from those currently in use
will be updated before the next MD step commences.  It is therefore possible
to alter the state of a running calculation by simply making changes
to the parameters file while the calculation is running. The same
considerations/restrictions which apply to changing parameters on a
restart apply to these on the fly changes.
