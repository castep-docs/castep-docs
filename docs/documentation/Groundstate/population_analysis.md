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

