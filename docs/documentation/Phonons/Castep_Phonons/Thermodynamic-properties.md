
One of the important motivations for lattice dynamical calculations of
crystalline solids is that the harmonic approximation gives access to
thermodynamic properties including the zero-point energy and the free
energy as a function of temperature. CASTEP lattice dynamics
calculations can be followed by a thermodynamics calculation to
calculate the zero-point energy and temperature dependent free energy,
entropy, and specific heat

$$\begin{aligned}
 F &= E_{\text{elec}} + k_{B} T \sum_{{\mathbf{q}},i} ln \left [ 2 \sinh \left (\frac{\hbar \omega_{{\mathbf{q}},i}}{ k_{B} T} \right ) \right ],\\
 S &= \frac{1}{2T} \sum_{{\mathbf{q}},i} \hbar \omega_{{\mathbf{q}},i}  \coth \left (\frac{\hbar \omega_{{\mathbf{q}},i}}{ k_{B} T} \right )
       - k_{B} \sum_{{\mathbf{q}},i} ln \left [ 2 \sinh \left (\frac{\hbar \omega_{{\mathbf{q}},i}}{ k_{B} T} \right ) \right ],\\
 C_V &=  \sum_{{\mathbf{q}},i} k_{B} \left ( \frac{\hbar \omega_{{\mathbf{q}},i}}{ k_{B} T} \right )^2
         \exp{\left (\frac{\hbar \omega_{{\mathbf{q}},i}}{ k_{B} T}\right
         )}  /%
         \left [\exp{\left (\frac{\hbar \omega_{{\mathbf{q}},i}}{ k_{B}
         T}\right )} -1 \right ]^2 .
\end{aligned}$$

The thermodynamics calculation follows a previous phonon calculation. It
is selected by setting the parameter

> `task : THERMODYNAMICS`

This may be used in a continuation run from a previous phonon
calculation, where the value of the `continuation` parameter is the name
of the previous `.check` file. Alternatively it may be configured as a
new run from scratch by setting the remainder of the parameters exactly
as if this were a phonon task, and the phonon calculation will be
performed first. Only the phonons defined on the “fine” set of phonon
kpoints will be used to compute the free energy as it is normally
expected that a thermodynamics calculation will follow an interpolation
or supercell calculation. However provided that the standard and fine
sets of phonon k-points are identical, it may also be used following a
standard phonon calculation.

This task will compute and print the free energy, entropy and specific
heat plus the vibrational atomic displacement parameters (“ADP”s) in the
range of temperatures specified by the parameters `thermo_t_start` and
`thermo_t_stop`. The number of temperatures is set by one or other of
the parameters `thermo_t_spacing` or `thermo_t_npoints`. All
temperatures are absolute and the default unit is K. The results of the
calculation are written to the `.castep` file.

The harmonic approximation free energy is only defined if all
frequencies are greater than or equal to zero. Any zero or imaginary
frequencies are automatically omitted from the calculation and a warning
message is printed. **It is the responsibility of the end user to check
that the computed free energy is not rendered meaningless by the
presence of an imaginary mode.**

