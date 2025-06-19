#  DFT+U(MO) - Applying potentials to arbitrary orbitals

## Basics

We can employ the molecular orbital projections we have introduced
in the [le $\Delta$SCF](lin_ex_delta_scf.md) section to also
introduce penalty potentials that shift specific orbitals up or down. This can be used to specify the
HOMO-LUMO of an adsorbed molecule or to modify the level alignment with the
metal substrate. This constraint potential can be combined with population constraints.

For more details and an example application on Porphine molecules adsorbed at coinage
metal surfaces, see Müller *et al*. (2016)[@Muller2016].

For a le $\Delta$SCF calculation, we have to set `deltascf_method = linear expansion` in the
`<seed>.param` file. The constraint must also be specifed, as discussed in the
[overview](overview.md) section.

The only additional relevant $\Delta$SCF keywords is `deltascf_dftu_checkpoint`

Example `.param` file:


```
reuse               : <base>.check
calculate_deltascf  : true
deltascf_checkpoint : <base>.check
deltascf_dftu_checkpoint : <base2>.check
deltascf_method     : DFT+U(MO)

#band  occ spin    +U in eV  excite?
%block deltascf_constraints
34    0.0000  1   -1.40         Y
35    1.0000  2    0.70         Y
%endblock deltascf_constraints
```
In this mode we add a potential to the Hamiltonian for each defined constraint,
which has the following form:

$$V_c = \frac{U}{2} \cdot|\phi_c\rangle\langle\phi_c| $$

You can find a detailed description of these potentials in Appendix D of
*First-Principles Description of the Isomerization Dynamics of Surface-Adsorbed Molecular Switches* [@Maurer2014]

In this example, two +U constraint potentials act on orbital no. 34 of the majority spin channel
and orbital no. 35 of the minority spin channel, taken from the
`deltascf_dftu_checkpoint=<base2>.check` file. In addition, the occupation of orbital no. 35 taken
from file `deltascf_checkpoint=<base>.check` file is constrained
to the occupation 1.000. Excitation constraints on each state can be activated (or not) by adding
the final 'Y' or 'N' to the relevant line.
