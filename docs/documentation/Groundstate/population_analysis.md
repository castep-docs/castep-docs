# Population analysis

At the end of a single point calculation, the ground state electron density is obtained. The electrons are distributed such that the total energy functional is minimised, meaning that they do not
belong to individual atoms anymore. However, it is often useful as well as insightful to partition the total electron density to atomic or bond contributions. While such population analyses have no
direct connection to experimental observables, they provide a chemical interpretation of possible charge transfer within the system. There are many flavours of charge partitioning, of which CASTEP can
perform the [Mulliken population analysis](https://doi.org/10.1063/1.1740588) (see also [here](https://doi.org/10.1063/1.1740589), [here](https://doi.org/10.1063/1.1741876) and [here](https://doi.org/10.1063/1.1741877)) and the [Hirshfeld definition](https://doi.org/10.1007/BF00549096).

## Mulliken population analysis

The total number of electrons $N$ of a quantum mechanical system can be found by evaluating the sum
\begin{equation}
N = \sum _ \mu (\mathbf{P} \mathbf{S}) _ {\mu\mu}
\end{equation}
where $\mathbf{P}$ and $\mathbf{S}$ are the density and overlap matrices expressed in a suitable basis set $\boldsymbol{\chi}$, respectively. The overlap matrix elements are obtained as
\begin{equation}
S _ {\mu\nu} = \langle \chi _ \mu | \chi _ \nu \rangle
\textrm{.}
\end{equation}
The density matrix results from evaluating the density operator using the basis set
\begin{equation}
P _ {\mu\nu} = \langle \chi _ \mu | \hat{P} | \chi _ \nu \rangle
\end{equation}
where the single-particle density operator is expressed in terms of the single-particle wavefunctions $\psi _ i$ and the corresponding occupancies $f _ i$ as 
\begin{equation}
\hat{P} = \sum _ i f _ i \; |\psi _ i \rangle \langle \psi _ i |
\textrm{,}
\end{equation}
therefore
\begin{equation}
P _ {\mu\nu} = \sum _ i f _ i \; \langle \chi _ \mu | \psi _ i \rangle \langle \psi _ i | \chi _ \nu \rangle
\textrm{.}
\end{equation}

If the basis set $\boldsymbol{\chi}$ is local (i.e. functions with compact support), individual terms $(\mathbf{P} \mathbf{S}) _ {\mu\mu}$ in the total charge expression may be associated with the
spatial region corresponding to the individual basis function $\chi _ \mu$. If these basis functions are centred on atoms, the contributions belonging to a particular atom $A$ are defined as the
charge of $A$:
\begin{equation}
N _ A = \sum _ {\mu \in A} (\mathbf{P} \mathbf{S}) _ {\mu\mu}
\textrm{.}
\end{equation}
Conveniently, the off-diagonal elements of $\mathbf{P} \mathbf{S}$ are partitioned into bond contributions between atoms $A$ and $B$ as
\begin{equation}
N _ {AB} = \sum _ {\mu \in A} \sum _ {\nu \in B} (\mathbf{P} \mathbf{S}) _ {\mu\nu}
\textrm{.}
\end{equation}

To assign a charge to an atom,
\begin{equation}
q _ A = Z' _ A - N _ A
\end{equation}
is calculated, where $Z'$ is the pseudoatom nuclear charge.


### The CASTEP implementation

In CASTEP, the solution of the electronic problem results in a set of Kohn-Sham orbitals $\psi _ i$, which are expressed in terms of plane-wave functions. Plane-waves are non-local, therefore not
directly suitable for Mulliken population analysis. In order to obtain a suitable local basis, CASTEP solves the electronic problem of the isolated atom for each atomic specie present in the system,
resulting in a set of atomic orbitals $\chi _ \mu$. Note that for this set of calculations, the same calculation settings (e.g. electronic cutoff and pseudopotentials) are used. With the atomic
orbitals determined, the Mulliken population analysis can be performed by calculating the projections $\langle \chi _ \mu | \psi _ i \rangle$.

### CASTEP keywords

The default behaviour is to compute the population analysis on completion of most tasks that determine the ground state electron density. Mulliken population analysis can be turned off by adding
```
POPN_CALCULATE : FALSE
```
to the `.param` file. The bond population analysis is computed between all atoms which are closer than a spatial cutoff (3 &#8491 by default), which may be controlled using the `.param` keyword `POPN_BOND_CUTOFF`, for
example
```
POPN_BOND_CUTOFF : 4.0
```
to set the cutoff to 4 &#8491. To control the verbosity of the population analysis output,
```
POPN_WRITE : ENHANCED
```
which is the default setting, writes individual orbital as well as atomic and bond populations;
```
POPN_WRITE : MINIMAL
```
only writes atomic and bond populations;
```
POPN_WRITE : NONE
```
only writes bond populations.

The `.cell` block `SPECIES_LCAO_STATES` controls the number of atomic orbitals, as specified by their main and angular quantum numbers, used for each atomic specie. By default, all valence states up to the next noble gas configuration are obtained and used
in the population analysis, but these can be overridden, for example:
```
%BLOCK SPECIES_LCAO_STATES
H 3
%ENDBLOCK SPECIES_LCAO_STATES
```
will use the 1s, 2s and 2p orbitals. Shallow core states, if explicitly treated as valance states, are included. For example, for atoms such as Na, where most pseudopotential definitions include shallow core states, 2s, 2p, 3s and 3p are all used in the population analysis.

## The Hirshfeld partitioning scheme

The Hirshfeld population analysis partitions the total ground state electronic density $\rho(\mathbf{r})$ into atomic densities using
\begin{equation}
\rho _ A(\mathbf{r}) = w _ A(\mathbf{r}) \rho(\mathbf{r})
\end{equation}
where $w _ A(\mathbf{r})$ is the sharing function belonging to atom $A$. The sharing function is calculated from the spherically averaged isolated atom densities $\rho^\textrm{isolated}$ as
\begin{equation}
w _ A(\mathbf{r}) = \frac{\rho^\textrm{isolated} _ A (\mathbf{r})}{\sum _ A \rho^\textrm{isolated} _ A (\mathbf{r})}
\textrm{,}
\end{equation}
where each $\rho^\textrm{isolated} _ A$ is centred at the position $\mathbf{R} _ A$ of the nucleus of $A$.

The electronic charge attributed to atom $A$ is the integral 
\begin{equation}
N _ A = \int \mathrm{d} \mathbf{r} \rho _ A(\mathbf{r})
\textrm{,}
\end{equation}
from which the total charge is obtained as
\begin{equation}
q _ A = Z' _ A - N _ A
\textrm{.}
\end{equation}

Other quantities, such as the volume of the bonded atom is calculated from the integral
\begin{equation}
V _ A = \int \mathrm{d} \mathbf{r} \rho _ A(\mathbf{r}) |\mathbf{r} - \mathbf{R} _ A|^3
\textrm{,}
\end{equation}
which are useful in other methods, such as the [many-body and XDM ispersion schemes](../dftd).


### The CASTEP implementation

Similarly to the Mulliken population analysis, the ground state electron density of isolated atoms of every specie are determined in the post-processing step, using the same pseudopotential and
calculation parameters as the main calculation.

### CASTEP keywords

To switch on the Hirshfeld partitioning scheme, add
```
CALCULATE_HIRSHFELD : TRUE
```
to the `.param` file. This provides a basic analysis of the Hirshfeld charges. More information, such as atomic volumes, can be gained when using
```
IPRINT : 2
```
or higher.
