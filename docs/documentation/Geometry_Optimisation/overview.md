

The essence of the calculation is for the ions and electrons in the supercell to be moved around stepwise until the forces on the atoms and the change in total energy between steps fall below some predefined convergence tolerance. The ionic positions are optimised using quasi-Newton methods. For each configuration of the ionic positions the electronic configuration is optimised using the method of conjugate gradients. The flow of the calculation is thus;

1. Move ions into new positions using geometry optimisation algorithm
2. Find electronic energy and forces for this ionic configuration
3. Compare total energy with previous configurations and check if forces within tolerance limits
4. If structure not optimised start at (1) and generate new set of ionic positions
This cycle is performed until the forces fall within the tolerance limit and the energy should then be a local minimum.

With periodic boundary conditions (as used by CASTEP) it is also possible to change the size and shape of the cell, in addition to (or instead of) moving the ions. In this case, the stress is calculated in addition to the forces, and this is used to change the cell, until the stress falls within a given tolerance.

Finally, when considering the change in the cell, it is also possible to apply an external pressure. Hence it is the enthalpy, which is the appropriate free energy in this scenario, which is minimised instead of the energy.


### Finite-basis set corrections

It should be noted, that with a plane-wave basis set (as used by CASTEP) there is an important side-effect of changing the size and/or shape of the cell - it changes the basis set used for the electronic states. Many DFT programs ignore this effect, which means that if the cell vectors change by more than a few %, the final structure is evaluated with a non-self-consistent basis, with a different cut-off energy to that intended. In CASTEP, there are two choices here: to either keep the cut-off energy constant (which results in the number and meaning of the plane-waves used in the basis changing from step-to-step) or to keep the number of plane-waves constant  (which results in a change in the cut-off energy and in the meaning of the plane-waves used from step-to-step). The constant-cutoff/variable-number of plane-waves approach is the CASTEP default as it is the most physically reasonable. The constant number of plane-waves approach means that the quality of the calculation is changing from step-to-step.

The effect of changing lattice vectors on the basis set can also be corrected to first-order using the 'finite basis set correction'. This can be calculated by the change in total energy for a small change in the cut-off energy at the start of a calculation, and then used as a correction to the energy and the stress. This is especially important in variable-cell calculations, for which it is activated by default.

#### Advanced settings
For geometry optimisation, there are a variety of different algorithms available which can be selected by the `geom_method` parameter in the param file. The choices are:

* LBFGS - the low-memory version of BFGS - the default option
* BFGS - widely-used quasi-Newton minimization
* TPSD - two-point steepest descent
* DELOCALIZED - a BFGS-based minimizer using delocalized internal coordinates
* DMD - optimally damped MD
* FIRE - fast inertial relaxation engine - a modified MD approach

NB These are all 'local optimisations', i.e. the final structure depends upon the initial configuration and is not the global minimum. For those interested in finding the global minimum, then there are associated projects using Genetic Algorithms and AIRSS.

The first 3 methods can do variable-cell or fixed-cell optimization, whereas the last 3 are only fixed-cell (for now). LBFGS/BFGS is generally the fastest method, and since v19, LBFGS has supported new preconditioners which should make it generally faster still. TPSD (unlike LBFGS/BFGS) has no built-in history, so should be much slower - however, the CASTEP implementation has a very efficient preconditioner which makes up for this, and the lack of history means that variable-cell optimisation with additional cell constraints is much more efficient than the equivalent calculation in LBFGS/BFGS.

The DELOCALIZED minimizer is the only supported method to use delocalized internal coordinates, as opposed to absolute or fractional coordinates, and as such, should be best for optimizing large structures such as molecule-in-a-box with many low-energy soft modes. The two MD-based methods are generally less efficient, but can handle arbitrary constraints well, and have sometimes out-performed other methods for very anisotropic systems, such as molecule-on-a-surface etc.
