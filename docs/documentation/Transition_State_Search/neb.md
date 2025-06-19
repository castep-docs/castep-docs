!!! note
        The NEB functionality in CASTEP was overhauled in version 22, with more efficient algorithms available. In order to use this new functionality, make sure you're **using CASTEP 22 or later**.

## Background and theory

The nudged elastic band method is a widely-used method for finding a minimum energy pathway between two structures.
You can use the method to estimate the barrier for the system to transition between the two structures.

<!-- TODO: more about the theory?  -->

In our NEB implementation the update rule for atomic position is given by:

$$
x^{k+1}_{n} = x^{k}_n + \alpha^k [-\nabla^\perp V(x^{k}_n) + \mathbf{\eta}^{k}_n]
$$

where $x^{k}_n$ are the positions of image $n$ at iteration $k$. $\alpha^k$ is the step size, which can either be fixed or chosen in an adaptive manner, $\nabla^\perp V(x^{k}_n)$ is the gradient of the total energy, projected to remove the component along the reaction path, and $\mathbf{\eta}^{k}_n = \mathbf{\eta}((x^{k}_n)',(x^{k}_n)'')$ is the NEB spring force.


As a consequence of the projection step, the NEB forces do not have a corresponding energy functional and hence linesearch is not possible, making quasi-Newton searches such as (L)BFGS inapplicable. Standard approaches are either to use simple gradient-only based methods or to add a maximum step size constraint in place of the linesearch. Both of these can exhibit slow convergence; a solution is instead to choose the step size adaptively using a custom time-stepping algorithm. A promising solution to this problem is the ODE12r adaptive scheme[@ODE12R], which combines two distinct step selection criteria:
one based on minimising the change in the residual force from one step to the next as is typically done to control error in adaptive ODE solvers, and a second based on minimising the residual itself. The key idea is that adaptive ODE step selection should be used in the pre-asymptotic regime, while minimising the residual is suitable in the asymptotic regime.

We have implemented three optimisation schemes for NEB paths, with the approach to be used controlled by the `TSSEARCH_NEB_METHOD` parameter: (i) the two point steepest descent scheme of Barzilai and Borwein[@TPSS]; (ii) the fast inertial relaxation engine (`FIRE`[@FIRE]) and (iii) the `ODE12R`[@ODE12R] scheme discussed above. In all three cases, convergence is controlled by the existing `TSSEARCH_FORCE_TOL` parameter. To better fit user intuition, the default value of this parameter is now equal to the force tolerance used during geometry optimisation, `GEOM_FORCE_TOL`.


We also provide three alternative algorithms to compute the tangents $(x^{k}_n)'$ and curvatures $(x^{k}_n)''$ at each image along the path, controlled by the `TSSEARCH_NEB_TANGENT_MODE` parameter. The three approaches are based on bisection, the improved tangent scheme of FIRE[@FIRE], and cubic spline interpolation as used in ODE12R[@ODE12R]. The latter was found to be the most robust so has been made the default.


## Keywords

As with other functionality in CASTEP, you can use the built-in help tool to find information on NEB-related keywords. For example, you could run:

`castep -s tssearch`


The relevant `.param` keywords are summarised in the table below:


| Parameter                      | Default                                                         | Level        | Notes                                                                                                                                                                                                                                                                                                                                     |
|--------------------------------|-----------------------------------------------------------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `TASK`                         | `SINGLEPOINT`                                                   | Basic        | Set to `TRANSITIONSTATESEARCH` to perform a transition state calculation.                                                                                                                                                                                                                                                                 |
| `TSSEARCH_METHOD`              | `LSTQST`                                                        | Basic        | The search method used to locate transition states. Must be set to `NEB` to perform a NEB calculation. Previous default retained for backwards compatibility. Modifiable: restart only. Allowed values: `LSTQST`, `NEB` Default value : `LSTQST`                                                                                          |
| `TSSEARCH_FORCE_TOL`           | Same as `GEOM_FORCE_TOL`                                        | Basic        | Tolerance for accepting convergence of the maximum \|ionic force\| during QST search. Modifiable: restart and on the fly                                                                                                                                                                                                                  |
| `TSSEARCH_MAX_PATH_POINTS`     | 20                                                              | Intermediate | The maximum number of path points for NEB search. Modifiable: restart and on the fly. Allowed values: (any integer) > 0                                                                                                                                                                                                                   |
| `TSSEARCH_NEB_METHOD`          | ODE12R[@ODE12R]                                                 | Intermediate | Method used to optimize the NEB shape. Modifiable: restart and on the fly. Allowed values: `GRAD_BB`[@TPSS], `FIRE`[@FIRE], `ODE12R`[@ODE12R]                                                                                                                                                                                             |
| `TSSEARCH_NEB_TANGENT_MODE`    | `SPLINE`                                                        | Basic        | Method used to calculate the tangents of the NEB. Modifiable: restart and on the fly. Allowed values: `NONE`, `BISECT`, `HIGH_E`, `SPLINE`                                                                                                                                                                                                |
| `TSSEARCH_NEB_SPRING_CONSTANT` | 0.1 eV/ang2                                                     | Basic        | Spring constant used between the images in NEB search. Modifiable: restart and on the fly. Allowed values: (any) > 0.0                                                                                                                                                                                                                    |
| `TSSEARCH_NEB_CLIMBING`        | FALSE                                                           | Basic        | If TRUE then the central bead in NEB search climbs up the potential and `TSSEARCH_MAX_PATH_POINTS` must be odd (may be increased by +1). If FALSE then the central bead in NEB search slides down the potential. Modifiable: restart only. Allowed values: TRUE or FALSE. Default value: FALSE                                            |
| `TSSEARCH_NEB_MAX_ITER`        | 20                                                              | Intermediate | The maximum number of steps during NEB search. Modifiable: restart and on the fly. Allowed values: (any integer) > 0                                                                                                                                                                                                                      |
| `TSSEARCH_NEB_NORMED`          | FALSE if `TSSEARCH_NEB_TANGENT_MODE` = `SPLINE`, TRUE otherwise | Expert       | If TRUE then the spring forces applied along the tangents in the NEB are normed to the displacement between beads. If FALSE then the spring forces are projected along the tangents in the NEB and may result in null forces if displacements are orthogonal to the NEB tangents. Modifiable: restart only. Allowed values: TRUE or FALSE |



As a minimum, you need to specify `TASK: TRANSITIONSTATESEARCH` and `TSSEARCH_METHOD: NEB` in the .param file
and specify the product (final) ionic positions (using e.g. the `POSITIONS_ABS_PRODUCT` block) and a transition state guess configuration (using e.g. the `POSITIONS_ABS_INTERMEDIATE` block) in the .cell file, in addition to the normal `POSITIONS_ABS` block.
CASTEP will then linearly interpolate from the initial to intermediate and from the intermediate to product configurations to begin the NEB calculation.
<!-- TODO: in future versions of CASTEP, you won't be required to manually specify an intermediate structure. If not present, castep will linearly interpolate between start and end -->

However, it's advisable to also:

- change the number of images used (`TSSEARCH_MAX_PATH_POINTS`),
- decide on whether you want the climbing image method (`TSSEARCH_NEB_CLIMBING`), and
- think about the relevant force criterion to be used (`TSSEARCH_FORCE_TOL`).

For a practical guide on how to use the NEB method in CASTEP, see the [tutorial](../../tutorials/NEB/neb_tutorial.md).



## Output files

In addition to information in the `.castep` file, a `.ts` file will be generated during a transition state search calculation. Below is the start of a typical `.ts` file, with annotations explaing what each line means (you can see these by clicking on the (:heavy_plus_sign:) symbols).



!!! note
        Like `.geom` and `.md` files, `.ts` files use atomic units (Ha for energies, Bohr for distances and Bohr/Ha for forces etc.).

``` yaml
 TSTYPE TSConfirmation # (1)!
 REA     1      0.00000000E+000 # (2)!
              -1.19447739E+001     -1.19447739E+001                       <-- E #(3)!
               1.32280829E+001      0.00000000E+000      0.00000000E+000  <-- h #(4)!
               8.09986468E-016      1.32280829E+001      0.00000000E+000  <-- h
               8.09986468E-016      8.09986468E-016      1.32280829E+001  <-- h
 H           1      6.61419707E+000      8.39780193E+000      5.86117838E+000  <-- R #(5)!
 H           2      8.15635294E+000      5.72185774E+000      5.85777350E+000  <-- R
 H           3      5.06964224E+000      5.72278559E+000      5.86095165E+000  <-- R
 N           1      6.61404144E+000      6.61404144E+000      6.61404144E+000  <-- R
 H           1      8.47021636E-007      3.11793289E-005      2.28609226E-005  <-- F #(6)!
 H           2      1.38512779E-006     -2.45087447E-005     -4.65186359E-005  <-- F
 H           3     -4.12781162E-005     -4.76763241E-006      1.75643331E-005  <-- F
 N           1      3.90459667E-005     -1.90295182E-006      6.09338019E-006  <-- F

 PRO    1      1.00000000E+000 #(7)!
              -1.19447351E+001     -1.19447351E+001                       <-- E
               1.32280829E+001      0.00000000E+000      0.00000000E+000  <-- h
               8.09986468E-016      1.32280829E+001      0.00000000E+000  <-- h
               8.09986468E-016      8.09986468E-016      1.32280829E+001  <-- h
 H           1      6.61608080E+000      8.39796599E+000      7.36585209E+000  <-- R
 H           2      8.15724653E+000      5.72090835E+000      7.36726384E+000  <-- R
 H           3      5.07119891E+000      5.72404366E+000      7.37171850E+000  <-- R
 N           1      6.61404144E+000      6.61404144E+000      6.61404144E+000  <-- R
 H           1      6.09749957E-005      4.97392811E-005     -4.85624696E-005  <-- F
 H           2      6.57602570E-005     -1.92918456E-005     -3.12188543E-005  <-- F
 H           3     -5.16484028E-005      2.80445001E-005      5.83274956E-005  <-- F
 N           1     -7.50868499E-005     -5.84919355E-005      2.14538282E-005  <-- F

 TST    1      1.25000056E-001 #(8)!
              -1.19415297E+001     -1.19415297E+001                       <-- E
               1.32280829E+001      0.00000000E+000      0.00000000E+000  <-- h
               8.09986468E-016      1.32280829E+001      0.00000000E+000  <-- h
               8.09986468E-016      8.09986468E-016      1.32280829E+001  <-- h
 H           1      6.61443264E+000      8.39782206E+000      6.04926187E+000  <-- R
 H           2      8.15646486E+000      5.72173929E+000      6.04646018E+000  <-- R
 H           3      5.06983587E+000      5.72294304E+000      6.04979810E+000  <-- R
 N           1      6.61404144E+000      6.61404144E+000      6.61404144E+000  <-- R
 H           1     -9.19085803E-006      2.32501273E-002     -1.04092397E-002  <-- F
 H           2      2.02903385E-002     -1.17660606E-002     -1.06346944E-002  <-- F
 H           3     -2.03961322E-002     -1.17795791E-002     -1.05604406E-002  <-- F
 N           1      1.14984498E-004      2.95512341E-004      3.16043747E-002  <-- F


```

1. This is a comment line stating what type of calculation was carried out.
2. This is the initial (i.e. the **REA** ctant) configuration. The integer indicates it is the configuration for the first NEB iteration. As the REActant (and PROduct) configurations are the same for every NEB iteration, they are only printed out once. The float at the end of the line is a measure of where the configuration lies between 0 (reactant) and 1 (product).
3. `<-- E` is the total energy and enthalpy of the system, in atomic units.
4. `<-- h` is the unit cell matrix (atomic units).
5. `<-- R` are the atomic coordinates (Cartesian), in atomic units.
6. `<-- F` are the forces (atomic units).
7. This is the end-point (or **PRO** duct) configuration for the first iteration. As this is the same for every NEB iteration, it is only printed out once.
8. This is the first of the transition state configurations (NEB images) for iteration 1 of the NEB. For example, if you have 7 images, then there will be 7 blocks that start with `TST    1 `.

<!-- TODOs:
- be more precise about the meaning of the 'distance' between images
- clarify what forces these are (do they include the spring forces?)
-  -->
