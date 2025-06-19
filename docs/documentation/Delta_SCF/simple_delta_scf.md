# Conventional Delta-Self-Consistent-Field-DFT Calculations

## Basics

In $\Delta$SCF-DFT we calculate electronic excited states by assuming a
certain non-equilibrium orbital occupation and by self-consistently
solving the Kohn-Sham equations with this excited state population.

The excitation energy is then simply the energy difference between the
ground state KS-DFT calculation and the $\Delta$SCF-DFT calculation:

$$\Delta E = E(\Delta SCF)-E(DFT)$$

We therefore need to perform two calculations, the ground state DFT
calculation and the DeltaSCF calculation. For a more detailed
explanation, see Maurer and Reuter (2011)[@DeltaSCF1].

For this simple $\Delta$SCF calculation, we have to set `deltascf_method = simple` in the
`<seed>.param` file. The constraint must also be specifed, as discussed in the
[overview](overview.md) section.

The only additional relevant $\Delta$SCF keywords is `deltascf_smearing`

Example `.param` file:


```
reuse               : <base>.check
calculate_deltascf  : true
deltascf_checkpoint : <base>.check
deltascf_method     : simple
deltascf_smearing   : 0.01

#band  occ spin from_band to_band
%block deltascf_constraints
34    0.0000  1   34   34
35    1.0000  1   35   35
%endblock deltascf_constraints
```

In this example, we enforce an occupation of 0.00 electrons in the
electronic state 34, spin channel 1 and an occupation of 1.00 electrons
in the electronic state 35, spin channel 1. The last two numbers in each
line specify a window of states in which the corresponding state is
searched if it changes its position between SCF cycles. In that way we
can ensure that we constrain the correct state.

`deltascf_smearing` is a mechanism which relaxes the constraints minimally to facilitate
convergence. Sometimes, especially in the case of degenerate states, `deltascf_smearing` is
necessary.
