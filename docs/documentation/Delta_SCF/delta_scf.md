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
explanation, see J. Chem. Phys. 135, 224303 (2011)

For the $\Delta$SCF calculation, we have to add following keyword to
<seed\>.param

    %BLOCK DEVEL_CODE
      DeltaSCF
    %ENDBLOCK DEVEL_CODE

and add following keyword in <seed\>.deltascf

    deltascf_mode        :  1                               

### Keywords allowed in <seed\>.deltascf

In the .deltascf file, the keyword title plus colon takes exactly 23
columns (A20,3X). The keyword content starts after that. Lines with
\'#\' are ignored.

------------------------------------------------------------------------



------------------------------------------------------------------------

| keyword        | multiple appearance | arguments and FORTRAN format |   
| ------------ |  -------------------- | ---------------------------- |
| deltascf_iprint              | > No                | <integer I\>                |
| deltascf_mode  | > No    | <integer I\>, 1, 2, 3, or 4             |
| deltascf_constraint          | > Yes   | <#state I5\>1X<occ. F8.4\>1X<spin I4\><from I4\><to I4\>     |
| overlap_cutoff | > No    | <float F8.4\>, default: 0.01            |
| deltascf_smearing            | > No    | <float F8.4\>, default: 0.01 eV         |
| deltascf_mixing              | > No    | <float F8.4\>, default: mix_charge_amp  |


Example .deltascf file:

    deltascf_mode        :  1                               
    deltascf_iprint      :  1                               
    # mode 1 constraints ##                                 
    #                       band  occ  spin from_band to_band
    deltascf_constraint  :  34    0.0000  1   34   34       
    deltascf_constraint  :  35    1.0000  1   35   35     
    overlap_cutoff       :  0.01                            
    deltascf_smearing    :  0.01   

In this example, we enforce an occupation of 0.00 electrons in the
electronic state 34, spin channel 1 and an occupation of 1.00 electrons
in the electronic state 35, spin channel 1. the last two numbers in each
line specify a window of states in which the corresponding state is
searched if it changes its position between SCF cycles. In that way we
can ensure that we constrain the correct state. ``deltascf_smearing`` is a
mechanism which relaxes the constraints minimally to facilitate
convergence. Sometimes, especially in the case of degenerate states,
``deltascf_smearing`` is necessary.
