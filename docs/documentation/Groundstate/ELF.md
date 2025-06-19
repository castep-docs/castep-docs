# ELF - Electron Localization Function

The ground state electron density, e.g. from a single point calculation or an MD run, etc. contains much useful information. It can be analysed in different ways, and the Electron Localization Function (ELF) is one such. This idea was originally created by Becke and Edgecombe[@Becke1990] for the analysis of molecules. The idea was later extended to spin and then to solid state systems by Silvi and Savin[@Silvi1994]. It was later discovered that the theoretical expressions were not strictly positive definite, and so a correlation correction was added by Jarvis and Carter[@Jarvis2001], and it is this final form that has been implemented in CASTEP.

## ELF theory

The ELF is given by

\begin{equation}
ELF = \frac{1}{1+\left( D/D0 \right)^2}
\end{equation}

and for Hartree-Fock approaches we have
\begin{equation}
 D = \frac{\sum{\left| \nabla \psi \right|^2}}{2} -\frac{\left(\nabla n\right)^2}{8*n}
\end{equation}

with $\psi$ being the wavefunction and $n$ the electron number density, and

\begin{equation}
D0 = 0.3*\left(3*\pi^2\right)^{2/3}*n^{5/3}
\end{equation}

with $D0$ is the probability. Hence ELF measures the excess kinetic energy due to Pauli repulsion, and this definition is bounded $0<ELF<1$. The excess KE is the difference in energy between a Fermionic and a Bosonic system at the same density. Where electrons make pairs of opposite spin, or are isolated, then Pauli expulsion is small and the excess KE is negligible. Hence the definition of ELF has large values where the system is more 'bosonic' and localized, whereas a HEG will have an ELF=0.5 exactly. In a non-pseudopotential calculation, the absolute values of ELF have meaning, otherwise it is used for trends. The ELF can be used to classify chemical bonds and defects.


### The CASTEP implementation

In CASTEP, we use the corrected DFT form:
\begin{equation}
D = -2*A*\sum{\psi^* \nabla^2\psi} + \frac{A}{2}\nabla^2 n  -  \frac{A}{4*n}\left(\nabla n\right)^2
\end{equation}

and $\psi$ is the Kohn-Sham wavefunction. The first term is the KE of the non-interacting K-S system, the second term is the "correlation correction" and the third term is the KE of the ideal Bose gas at the same density, and
\begin{equation}
A=\frac{\hbar^2}{2*m}.
\end{equation}

In the presence of spin, there is a seperate $ELF_{\alpha}$ and $ELF_{\beta}$ for the different spin channels, and each expression just uses $n_{\alpha}$ and $\psi_{\alpha}$ and

\begin{equation}
D0_{\alpha} = 0.3*\left(6*\pi^2\right)^{2/3}*n_{\alpha}^{5/3}.
\end{equation}

CASTEP uses pseudopotentials, and so the absolute values of ELF are not transferable to other calculations, but it can still give useful insights into the electronic properties of bonds and defects etc.

### CASTEP keywords

The default behaviour is to not compute ELF. It can be turned on by adding
```
CALCULATE_ELF : TRUE
```
to the `.param` file. The ELF will be written out to a binary file, unless the
```
WRITE_FORMATTED_ELF ; TRUE
```
is enabled. The ELF files (both formatted and unformatted) have the same internal layout as POT and DEN. It is conventional to visualize them as 3D isosurfaces using programs such as JMol.
