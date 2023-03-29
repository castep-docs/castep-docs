# Linear expansion DeltaSCF DFT calculations - Constraining projected reference orbitals

## Basics

For molecules adsorbed at surfaces, $\Delta$SCF calculations become
challenging, simply because of the large number of states. Not only is
it difficult to identify the correct state, often hybridization spreads
adsorbate molecular orbitals across a large number of substrate bands. A
more realistic excitation constraint would be to project on a gasphase
molecular orbital and subsequently enforce occupation of this state.

This idea is referred to as linear expansion $\Delta$SCF and has first
been proposed by Gavnholt *et al*. Phys. Rev. B 78, 075441 (2008).

The here presented implementation is described in J. Chem. Phys. 139,
014708 (2013). Herein, we constrain the occupation of a so-called
resonance state built from a linear combination of Kohn-Sham states
instead of a single KS state. We expand an abitrary reference state
$|\phi_c\rangle$ in the space of Kohn-Sham states as follows:

$$|\tilde{\psi}_c^{\mathbf{k}}\rangle = \sum_i^{\mathrm{states}} |\psi_i^{\mathbf{k}}\rangle\langle\psi_i^{\mathbf{k}}|\phi_c^{\mathbf{k}} \rangle$$

At the same time we orthogonalize the remaining KS states

$$|\tilde{\psi_i^{\mathbf{k}}}\rangle = |\psi_i^{\mathbf{k}}\rangle - \sum_c^{\mathrm{constr.}}|\phi_c^{\mathbf{k}}\rangle\langle\phi_c^{\mathbf{k}}|\psi_i^{\mathbf{k}}\rangle$$

After an additional orthonormalization of all states we have constructed
a resonance state $\tilde{\psi_c^{\mathbf{k}}}$ and removed all its
contributions from all other states. We can now constrain the occupation
of this state with the effect of describing an excitation of a specific
molecular orbital. This is done in every SCF step until the calculation
is converged.

For the le $\Delta$SCF calculation, we have to add following keyword to
<seed\>.param

    %BLOCK DEVEL_CODE
     DeltaSCF
    %ENDBLOCK DEVEL_CODE

and add following keyword to <seed\>.deltascf

    deltascf_mode        :  3

### Keywords allowed in <seed\>.deltascf

In the .deltascf file, the keyword title plus colon takes exactly 23
columns (A20,3X). The keyword content starts after that. Lines with
``#`` are ignored.

| keyword           | multiple appearance | arguments and FORTRAN format          |
| ------------------ | ---------- | --------------------------------------- |
| deltascf_iprint              | > No    | <integer I\>                            |
| deltascf_file  | > No    | <string\>                               |
| delta_scf_constraint          | > Yes   | <#state I5\>1X<occ. F8.4\>1X<spinI4\>      |
| overlap_cutoff | > No    | <float F8.4\>, default: 0.01            |
| deltascf_mixing              | > No    | <float F8.4\>, default: mix_charge_amp  |


Example .deltascf file:

    deltascf_mode        :  1                               
    deltascf_file        :  bla.check                               
    deltascf_iprint      :  1                               
    # mode 3 constraints ##                                 
    #                       band  occ  spin
    deltascf_constraint  :  35    1.0000  1
    overlap_cutoff       :  0.01                            

In this example, we take state 35 from wavefunction file bla.check and
enforce an occupation of 1.00 electrons. In this runmode we do not have
to pick constraints that yield a net change in charge equal to 0. Charge
neutrality will be satisfied by modifying the Fermi level accordingly.
However, this is only strictly sensible for metallic systems.
