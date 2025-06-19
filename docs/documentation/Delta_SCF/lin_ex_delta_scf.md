# Linear expansion DeltaSCF DFT calculations - Constraining projected reference orbitals

## Basics

For molecules adsorbed at surfaces, $\Delta$SCF calculations become
challenging, simply because of the large number of states. Not only is
it difficult to identify the correct state, often hybridization spreads
adsorbate molecular orbitals across a large number of substrate bands. A
more realistic excitation constraint would be to project on a gasphase
molecular orbital and subsequently enforce occupation of this state.

This idea is referred to as linear expansion $\Delta$SCF and has first
been proposed by Gavnholt *et al*[@DeltaSCF2].

The CASTEP implementation is described in Maurer and Reuer (2013)[@DeltaSCF3].
Herein, we constrain the occupation of a so-called
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

For a le $\Delta$SCF calculation, we have to set `deltascf_method = linear expansion` in the
`<seed>.param` file. The constraint must also be specifed, as discussed in the
[overview](overview.md) section.

The only additional relevant $\Delta$SCF keywords is `deltascf_overlap_cutoff`

Example `.param` file:


```
reuse               : <base>.check
calculate_deltascf  : true
deltascf_checkpoint : <base>.check
deltascf_method     : linear expansion
deltascf_overlap_cutoff : 0.01

#band  occ  spin
%block deltascf_constraints
35    1.0000  1
%endblock deltascf_constraints
```

In this example, we take state 35 from wavefunction file `<base>.check` and
enforce an occupation of 1.00 electrons. In this runmode we do not have
to pick constraints that yield a net change in charge equal to 0. Charge
neutrality will be satisfied by modifying the Fermi level accordingly.
However, this is only strictly sensible for metallic systems.
