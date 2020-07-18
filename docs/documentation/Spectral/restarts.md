


Spectral calculations do not write a check file - however, they can write backups to enable restarting an unfinished calculation. The limitation is that a parallel calculation must be restarted on the same number of processors.

```
#Sample param file
cut_off_energy   :  550 eV
fix_occupancy    : true
task             : spectral
spectral_task    : coreloss

%block devel_code
SPECTRAL_RESTART
%endblock devel_code

backup_interval 1800  ! time in seconds
```
The devel_code keyword `SPECTRAL_RESTART` triggers both the writing an reading of Spectral backup files.

`backup_interval` determines the time between writing backups. Backup will slow down the calculation as they require disk access (which is always slow). If you expect a job to run for several hours backing up every 30min is a reasonable compromise. After completing each k-point the CASTEP will check to see if time since the last backup is greater than backup_interval - is it is a backup will be written - if not CASTEP carries on with the next k-point. Note that a backup is always written (if backup_interval>0) after the final kpoint. This is useful insurance in case there is any problem when CASTEP writes the final output files.

Here is an example .castep file with backup 

```
  =====================================================================
  +                                                                   +
  +                 Calculation of Spectral Properties                +
  +                                                                   +
  + Calculation re-parallelised over 2 processes.                     +
  + Data distributed by G-vector(1-way), k-point(2-way), band(1-way)  +
  + Data distributed by k-point(2-way)                                +
  +                                                                   +
  =====================================================================
  Starting k-point:        1 of        5 on this process      |<-- SPEC
  Starting k-point:        2 of        5 on this process      |<-- SPEC
  Starting k-point:        3 of        5 on this process      |<-- SPEC
  Check-pointing spectral run                                 |<-- SPEC
  Starting k-point:        4 of        5 on this process      |<-- SPEC
  Starting k-point:        5 of        5 on this process      |<-- SPEC
  Starting k-point:        1 of        5 on this process      |<-- SPEC
  Check-pointing spectral run                                 |<-- SPEC
  Starting k-point:        2 of        5 on this process      |<-- SPEC
  Starting k-point:        3 of        5 on this process      |<-- SPEC
  Starting k-point:        4 of        5 on this process      |<-- SPEC
```
We see that backups were written every three k-points.  The last backup was done after the 1st k-point for spin 2.

As this calculation was run on two processors, we find two backup files have been created 

```
-rw-r--r--  1   317700 18 Jul 10:53 Si2-core.0001.spec
-rw-r--r--  1   317700 18 Jul 10:53 Si2-core.0002.spec
```


To restart, keep everything the same but add to the param file

```
 continuation : xxx.check 
```
 
 Where `xxx.check` is the name of the check file containing the ground-state density etc. This will have been written during the first run - and xxx will be replaced with whatever is the seedname of your run.
 
 We now re-run the calculation. CASTEP will read the ground-state from the check file (so there should be no electronic minimisation)
 
```
    Restarting spectral calculation from restart file         |<-- SPEC
  Starting k-point:        2 of        5 on this process      |<-- SPEC
  Starting k-point:        3 of        5 on this process      |<-- SPEC
  Starting k-point:        4 of        5 on this process      |<-- SPEC
  Check-pointing spectral run                                 |<-- SPEC
  Starting k-point:        5 of        5 on this process      |<-- SPEC
  Check-pointing spectral run                                 |<-- SPEC
  Total time to compute matrix elements           3500.45 sec |<—- SPEC
```
So the calculation did restart from the 2nd k-point on spin 2.

