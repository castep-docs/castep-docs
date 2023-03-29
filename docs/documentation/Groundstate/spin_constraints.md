# Introduction

Spin constraints allow you to ‘fix’ the spins within DFT by adding an energy penalty to states which do not obey the constraint. These change the minimum energy state from being the normal ground state to only those which have the target spin.

# Theory
## Energy Penalty Function


The easiest constraint is to fix the vector direction of the spin on a target atom. The energy penalty has the form:

$E_\text{con} =  \lambda\left(|\mathbf{M}_I| - \mathbf{e}_I \cdot \mathbf{M}_I\right) \geq 0$                 (eq1),

where  is the penalty constant, $\mathbf{M}_I$ is the magnetic moment of atom $I$, defined by

$\mathbf{M}_I = \int_\Omega \mathbf{m}(\mathbf{r}) F_I(\mathbf{r}) d^3r$

where $m(r)$ is the magnetization of the electrons at $r$, and $F_I(r)$ is a function approximating the electronic density of the atom $I$. This integral sums up the total magnetic moments in a region around the atom.

Eq (1) goes to zero as $\mathbf{M}_I$ goes to $\mathbf{e}_I$ and it is positive otherwise, so this leaves the target state unchanged and increases the energy of other states. 

The potential that arises from this can be found by taking the derivative of (1) with respect to the density:

$V_\text{con}(\mathbf{r}) = \lambda  F_I(\mathbf{r}) \left[\left(\frac{\mathbf{M}_I}{|\mathbf{M}_I|} - \mathbf{e}_I \right) \cdot \sigma\ \right]$

This is a local potential that pushes the density towards the constrained state. The strength of this “push” is changed by the penalty constant . Due to the factor (the spin operator), the potential only has components in the spin space and tries to rotate the direction of spin, but not change the magnitude. 


## Energy Penalty Constant

The energy penalty constant ($\lambda$) must be large enough to overcome any natural features of the energy landscape. That is, it must be big enough to make the target minimum be the actual minimum of the system. 

On the other hand, making this value too big causes the numerics to become difficult to solve. CASTEP is built to solve 
things 
that act like physical systems and various parameters have been tuned to make it fast at this. Values that are too big, push the system away from being like a physical system and make it take a very long time to converge. 

There are a few tricks that we can play to speed this up. The first is to start with a low value of the $\lambda$ and then increase it gradually. We do this by starting with a very low value, waiting until the system is converged, and then checking if the constraints are actually fulfilled (ie $\mathbf{M}_I = \mathbf{e}_I$. If not, we double $\lambda$ and converge again. We repeat this until the constraint is obeyed. 



# Using Magnetic Constraints

To apply a constraint to an atom, you must specify the spin in the cell file and add the extra tag FIX_SPIN for each atom on which you want to apply a constraint to block positions_frac or positions_abs in cell:
```
%block positions_frac
Fe 0.0 0.0 0.0 spin  2 0 0 FIX_SPIN
Ni 0.5 0.5 0.5 spin  1 1 0 
Mn 0.3 0.4 0.0 
%endblock positions_frac
```

This will set the system up with two Fe atoms as follows: 

| Element | Initial Spin | Spin Constraint |
|---------|--------------|-----------------|
| Fe      | 2 0 0        | Along 1 0 0     |
| Ni      | 1 1 0        | None            |
| Mn      | None         | None            |

It will then do the procedure mentioned in the previous section, doubling $\lambda$ to achieve the target constraints. You can only add FIX_SPIN to any atom that you have specified the spin for.

## Convergence

Some of the magnetic states can be difficult to converge, as the penalty potential still does not end up looking like a physical system. This causes the calculation to take a huge number of steps to reach convergence (if it even gets there!)

You almost certainly need to decrease the value of spin_mix_amp which has a default of 0.8 but should be much lower (eg 0.5 or even less) for many of these systems. 

Alternatively, you can use metals_method: EDFT which uses EDFT instead of density mixing and this can improve the convergence.
