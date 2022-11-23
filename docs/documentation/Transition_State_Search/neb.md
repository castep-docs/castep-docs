## Background and theory

The nudged elastic band method is a widely-used method for finding a minimum energy pathway between two structures. 
You can use the method to estimate the barrier for the system to transition between the two structures. 

TODO: more about the theory? 

In our NEB implementation the update rule for atomic position is given by:

$$
x^{k+1}_{n} = x^{k}_n + \alpha^k [-\nabla^\perp V(x^{k}_n) + \mathbf{\eta}^{k}_n]
$$

where $x^{k}_n$ are the positions of image $n$ at iteration $k$. $\alpha^k$ is the step size, which can either be fixed or chosen in an adaptive manner, $\nabla^\perp V(x^{k}_n)$ is the gradient of the total energy, projected to remove the component along the reaction path, and $\mathbf{\eta}^{k}_n = \mathbf{\eta}((x^{k}_n)',(x^{k}_n)'')$ is the NEB spring force.


As a consequence of the projection step, the NEB forces do not have a corresponding energy functional and hence linesearch is not possible, making quasi-Newton searches such as (L)BFGS inapplicable. Standard approaches are either to use simple gradient-only based methods or to add a maximum step size constraint in place of the linesearch. Both of these can exhibit slow convergence; a solution is instead to choose the step size adaptively using a custom time-stepping algorithm. A promising solution to this problem is the ODE12r adaptive scheme introduced in Ref. [3][3], which combines two distinct step selection criteria:
one based on minimising the change in the residual force from one step to the next as is typically done to control error in adaptive ODE solvers, and a second based on minimising the residual itself. The key idea is that adaptive ODE step selection should be used in the pre-asymptotic regime, while minimising the residual is suitable in the asymptotic regime. 


We therefore implemented three optimisation schemes for NEB paths, with the approach to be used controlled by the `TSSEARCH_NEB_METHOD` parameter: (i) the two point steepest descent scheme of [Barzilai and Borwein][1]; (ii) the fast inertial relaxation engine ([`FIRE`][2]) and (iii) the [`ODE12R`][3] scheme discussed above. In all three cases convergence is controlled by the previously existing `TSSEARCH_FORCE_TOL` parameter; a minor modification was made to set the default value of this parameter equal to the force tolerance used during geometry optimisation, `GEOM_FORCE_TOL`, to better fit user intuition. 


We also provide three alternative algorithms to compute the tangents $(x^{k}_n)'$ and curvatures $(x^{k}_n)''$ at each image along the path, controlled by the `TSSEARCH_NEB_TANGENT_MODE` parameter. The three approaches are based on bisection, the improved tangent scheme of Ref [2][2], and cubic spline interpolation as used in Ref [3][3]. The latter was found to be the most robust so has been made the default.


## Keywords

!!! note
        The NEB functionality in CASTEP was overhauled in version 22, with more efficient algorithms available. In order to use this new functionality, make sure you're **using CASTEP 22 or later**. 


As with other functionality in CASTEP, you can use the built-in help tool to find information on NEB-related keywords. For example, you could run:

`castep -s tssearch`


The relevant `.param` keywords are summarised in the table below:


| Parameter                      | Default                                                         | Level        | Notes                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------ | --------------------------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TASK`                         | `SINGLEPOINT`                                                   | Basic        | Task should be set to `TRANSITIONSTATESEARCH` to perform a transition state calculation.                                                                                                                                                                                                                                                  |
| `TSSEARCH_METHOD`              | `LSTQST`                                                        | Basic        | The search method used to locate transition states. Must be set to `NEB` to perform a NEB calculation. Previous default retained for backwards compatibility. Modifiable: restart only Allowed values: `LSTQST`, `NEB` Default value : `LSTQST`                                                                                           |
| `TSSEARCH_FORCE_TOL`           | Same as `GEOM_FORCE_TOL`                                        | Basic        | Tolerance for accepting convergence of the maximum \|ionic force\| during QST search. Modifiable: restart and on the fly                                                                                                                                                                                                                  |
| `TSSEARCH_MAX_PATH_POINTS`     | 20                                                              | Intermediate | The maximum number of path points for NEB search. Modifiable: restart and on the fly Allowed values: (any integer) > 0                                                                                                                                                                                                                    |
| `TSSEARCH_NEB_METHOD`          | [ODE12R][3]                     | Intermediate | Method used to optimize the NEB shape. Modifiable: restart and on the fly. Allowed values: [`GRAD_BB`][1], [`FIRE`][2], [`ODE12R`][3]                                                                                                                     |
| `TSSEARCH_NEB_TANGENT_MODE`    | `SPLINE`                                                        | Basic        | Method used to calculate the tangents of the NEB. Modifiable: restart and on the fly. Allowed values: `NONE`, `BISECT`, `HIGH_E`, `SPLINE`                                                                                                                                                                                                |
| `TSSEARCH_NEB_SPRING_CONSTANT` | 0.1 eV/ang2                                                     | Basic        | Spring constant used between the images in NEB search. Modifiable: restart and on the fly. Allowed values: (any) > 0.0                                                                                                                                                                                                                    |
| `TSSEARCH_NEB_CLIMBING`        | FALSE                                                           | Basic        | If TRUE then the central bead in NEB search climbs up the potential and `TSSEARCH_MAX_PATH_POINTS` must be odd (may be increased by +1). If FALSE then the central bead in NEB search slides down the potential. Modifiable: restart only. Allowed values: TRUE or FALSE Default value: FALSE                                             |
| `TSSEARCH_NEB_MAX_ITER`        | 20                                                              | Intermediate | The maximum number of steps during NEB search. Modifiable: restart and on the fly. Allowed values: (any integer) > 0                                                                                                                                                                                                                      |
| `TSSEARCH_NEB_NORMED`          | FALSE if `TSSEARCH_NEB_TANGENT_MODE` = `SPLINE`, TRUE otherwise | Expert       | If TRUE then the spring forces applied along the tangents in the NEB are normed to the displacement between beads. If FALSE then the spring forces are projected along the tangents in the NEB and may result in null forces if displacements are orthogonal to the NEB tangents. Modifiable: restart only. Allowed values: TRUE or FALSE |



As a bare minimum, you need to specify `TASK: TRANSITIONSTATESEARCH` and `TSSEARCH_METHOD: NEB` in the .param file 
and specify the product (final) ionic positions (using e.g. the `POSITIONS_ABS_PRODUCT` block) in the .cell file, in addition to the regular `POSITIONS_ABS` block.

CASTEP will then linearly interpolate between the initial and product configuration and begin the NEB calculation. 

However, it's advisable to also:

- change the number of images used (`TSSEARCH_MAX_PATH_POINTS`), 
- decide on whether you want the climbing image method (`TSSEARCH_NEB_CLIMBING`), and 
- think about the relevant force criterion to be used (`TSSEARCH_FORCE_TOL`).

For a more practical guide on how to use the NEB method in CASTEP, see the [tutorial](../../tutorials/NEB/neb_tutorial.md).


[1]: https://doi.org/10.1093/imanum/8.1.141 "GRAD_BB reference"
[2]: https://link.aps.org/doi/10.1103/PhysRevLett.97.170201 "FIRE reference"
[3]: https://doi.org/10.1063/1.5064465 "ODE12R reference"