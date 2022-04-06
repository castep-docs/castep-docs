# Checkpointing and Restarting

CASTEP provides a mechanism for saving intermediate and final states of the calculation and for restarting or continuing from a saved state.

At the end of every calculation which completes normally, CASTEP writes two files `<seed>.check` and `<seed>.castep_bin` which are binary-format files containing a complete state of the calculation including input parameters, cell variables, electron densities and any results or intermediate quantities whose calculation has completed. All inputs and results reported in the `.castep` file are saved to the checkpoint: indeed a lost `.castep` file from a completed calculation may be (mostly) regenerated using a minimal continuation run.

??? Info ".check vs .castep_bin"
    The only difference between `.check` and `.castep_bin` is that the `.check` file contains the converged ground-state wavefunctions but `.castep_bin` does not, and therefore requires much less disk space to store. This makes it useful for purposes of archiving a calculation. When continuing from a `.castep_bin` CASTEP will regenerate the ground state wavefunctions non-selfconsistently using the ground-state density from the file.

### Checkpointing during a calculation

An incomplete calculation can be completed in a new run by adding the parameters keyword

   `continuation : default`

in the `.param` file and rerunning CASTEP as before with the same `<seed>` command-line argument. This is the usual way of continuing a run interrupted, for example, by the job time limit on a batch scheduling system. To benefit from continuation, a checkpoint file must have been written in the original run. There are three parameters keywords which may be used to do this:

 - `num_backup_iter <n>` write a checkpoint every `<n>` (default 5) geometry MD or phonon steps
 - `backup_interval <s>` write a checkpoint every `<s>` seconds
 - `run_time <s>` write a checkpoint and exit at the first opportunity after `<s>` seconds have elapsed.

These may be used to periodically checkpoint many lengthy post-SCF tasks including geometry optimization, MD, phonon calculations, but checkpointing of spectral and magres tasks is not supported via this mechanism. Neither is checkpointing possible within an extremely lengthy SCF calculation, but see the next section for an alternative.  

Checkpoint files are portable, and independent of data-distribution, so the continuation run may use a different number of parallel nodes, data distribution, OpenMP etc. They are also portable across computers, so a run may be started on one computer and finished on another, which may be helpful to balance use of computer resources.

??? Info "Advanced keywords"
    One additional related parameters keyword which finds occasional use is a simple one-liner  `stop` which can be added to the `.param` file while a run is in progress. CASTEP rereads the `.param` file at every checkpoint opportunity and if this is present will perform a graceful exit after writing the checkpoint files.

    Which periodic and end-of-run checkpoint files are written may be controlled by the parameters keyword `write_checkpoint` which takes values

    - `none` : to suppress checkpoints completely

    - `minimal` writes only `.castep_bin`

    - `all` : writes both `.check` and `.castep_bin`

### Continuing from completed calculations
The checkpoint/restart mechanism may also be used to "chain" runs or initialise a modified run with the results of a previous one. The `.param` file of the new run should contain

`continuation : <oldseed>.check`

Parameters values stored in and read from `<oldseed>.check` will be used, unless overridden by the new `.param` file, which therefore needs only a minimal number of entries. The `.cell` file is usually just copy of the original, but may also be modified if needed.  Modifying `task` is a good way to "chain" calculations, for example performing a geometry optimisation followed by a spectral calculation.

!!! info
    Not all parameter or cell keywords can be overridden upon continuation. `castep --help <parameter-name>` will report whether a variable is modifiable on continuation


