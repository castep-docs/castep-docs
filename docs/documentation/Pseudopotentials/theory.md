The electrons in an atom can be divided into two types --- core
electrons and valence electrons. The core electrons are tightly bound
to the nucleus, while the valence electrons are more extended. A
working definition for core electrons is that they are the ones which
play no part in the interactions between atoms, while the valence
electrons dictate most of the properties of the material. It is common
to make the frozen core approximation; the core electrons are
constrained not to differ from their free atomic nature when placed in
the solid state environment. This reduces the number of electronic
degrees of freedom in an all-electron calculation. It is a very good
approximation. A different, but physically related, approach is taken
in the pseudopotential approximation. Since, in an all-electron calculation, the valence electron
wavefunctions must be orthogonal to the core wavefunctions they
necessarily have strong oscillations in the region near the nucleus
(see the all-electron wavefunction in Figure~\ref{fig:wvfn}). Given
that a planewave basis set is to be used to describe the
wavefunctions, these strong oscillations are undesirable --- requiring
many plane waves for an accurate description. Further, these
oscillations are of very little consequence for the electronic
structure in the solid, since they occur close to the nucleus.
In the pseudopotential
approach only the valence electrons are explicitly considered, the
effects of the core electrons being integrated within a new ionic
potential. The valence wavefunctions need no longer be orthogonal to
the core states, and so the orthogonality oscillations disappear;
hence far fewer plane waves are required to describe the valence
wavefunctions.
Numerous schemes to produce optimally soft
pseudopotentials have been developed. Common choices are the
norm-conserving potentials due to Troullier and
Martins[@Troullier1991] and Vanderbilt's ultrasoft
scheme[@Vanderbilt1990].
