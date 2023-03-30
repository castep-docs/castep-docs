For some systems, with light atoms and/or at low temperatures, the zero-point motion of the atom (rather than the electrons) 
can become significant. This requires a level of theory beyond the Born-Oppenheimer approximation, which assuming that the 
nuclei can be treated as classical point charges. One way of doing this, is the Feynman Path Integral approach to quantum 
mechanics, and using the isomorphism of a ring of classical "beads and springs" to represent a quantum particle. This 
approach is combined with MD to generate an ensemble of configurations, and so the approach is known as Path Integral 
Molecular Dynamics (PIMD). With this approach, quantum expectation values can be calculated by trajectory averages. Hence 
classical MD analysis techniques can be used to generate quantum values.

####Keywords

PIMD is a form of MD, and so all the usual MD keywords apply. NB the only supported `md_thermostat` is Langevin but this works with all values of `md_barostat`.

To activate PIMD, the key variables are:

```
md_use_pathint : true
md_num_beads   : 2
```

which turns on PIMD and 2 beads. It is important to note that the number of beads is an extra convergence parameter - the 
discretized ring becomes a continuous path integral in the limit that the number of beads tends to infinity. In practice, 
this is usually 2 -- 128 for light atoms (e.g. hydrogen) at temperatures > 10K. For lower temperatures, the number of beads 
goes up significantly.

```
num_farms      : 2
```

This is an important way to parallelize a PIMD calculation. With task farming, each bead can be assigned to a farm, so the 
number of farms should be either 1 (no farming) or `md_num_beads`. Then the PIMD calculation can be run in parallel on 
`num_farms` blocks of processors, where the number of processors in each block is determined by the usual CASTEP+DFT 
parallelization strategies (k-points, g-vectors, bands etc).


More advanced keywords are:

```
md_pathint_init : point / Gaussian
md_pathint_staging : true
```

This determines how the initial beads positions for a given atom are assigned. 'point' puts all the beads at the same point, 
whilst 'Gaussian' uses a Gaussian spreading function, which is analyticaly correct for a free particle to estimate the 
delocalization at the given temperature.

The staging mode transformation is a key way to eliminate the natural harmonics in the dynamics of the ring of beads, which 
would otherwise significantly reduce the time step required, particularly at low temperatures.

####Output files

When doing a PIMD calculation, there is `md_num_beads` times more information generated! Hence if using farming, then only 
the centroid position of and velocity etc of each ring of beads (corresponding to the classical position of each atom) is output to the `.castep` 
file. The coordinate data for each value of imaginary time (the cyclic index labelling the beads for each atom) is written 
to individual `farmXXX.castep` where XXX is the farm number. If not farming, then all this data is written to the 
single `.castep` file. The size of each ring for each atom at each real timestep is analysed in terms of the 'radius of gyration' 
tensor, and the 3 RGY eigenvalues and corresponding eigenvectors are also output to the master .castep file.

In addition, there are `beadXXX.md` files produced, one per imaginary time value (number of beads). These can 
be used for different MD analysis techniques, and can also be merged using scripts such as `pimerge.pl` to put all the bead 
data for each value of real time into the same file, which can be useful for visualization of the bead dynamics.

####Working with i-pi

`i-pi` is a 3rd-party python package for doing PIMD. This needs other codes, such as CASTEP, to generate the forces for a 
given configuration, and can then do different forms of PIMD, including centroid PIMD, which is not natively supported by 
CASTEP. i-pi communicates to CASTEP via internet sockets. The support for this is built into CASTEP from v22 or later.

There is an example of running i-pi with CASTEP in the examples/castep directory, along with a 'run_me' script that 
launches the i-pi server, creates a set of sub-directories (one per bead), and then launches the separate CASTEP clients. 
If doing PIMD in this mode, then you do not set PIMD variables in the `.param` file but rather in an i-pi `input.xml` file. 

The CASTEP `.param` file keywords needed are:

```
task       : socketdriver
socket_port: 31415
socket_host: localhost
```

where the `task` tells CASTEP to communicate with i-pi on `socket_port` (in this case, it is sent the bead 
coordinates and returns the energy and forces). The `socket_host` can be localhost, or an internet host, if running on a remote server.

For more information, see the [i-pi website](http://ipi-code.org).


