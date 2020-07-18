At the start of a calculation CASTEP will generate the require pseudopotentials. A report is written into the start of the <seedname>.castep file. This page explains what information is contained within this header.

## Carbon - Ultrasoft

```
============================================================                
| Pseudopotential Report - Date of generation  8-07-2020   |                
------------------------------------------------------------                
| Element: C Ionic charge:  4.00 Level of theory: PBE      |                
| Atomic Solver: Koelling-Harmon                           |                
|                                                          |                
|               Reference Electronic Structure             |                
|         Orbital         Occupation         Energy        |                
|            2s              2.000           -0.505        |                
|            2p              2.000           -0.194        |                
|                                                          |                
|                 Pseudopotential Definition               |                
|        Beta     l      e      Rc     scheme   norm       |                
|          1      0   -0.505   1.395     qc      0         |                
|          2      0    0.250   1.395     qc      0         |                
|          3      1   -0.194   1.395     qc      0         |                
|          4      1    0.250   1.395     qc      0         |                
|         loc     2    0.000   1.395     pn      0         |                
|                                                          |                
| Augmentation charge Rinner = 0.983                       |                
| Partial core correction Rc = 0.983                       |                
------------------------------------------------------------                
| "2|1.4|10|12|13|20:21(qc=7)"                             |                
------------------------------------------------------------                
|      Author: Chris J. Pickard, Cambridge University      |                
============================================================ 
```
All quantities are given in atomic units - so energies in Hartree (1Ha =26.4eV) and lengths in Bohr (1 bohr = 0.88Ang)

* Element: This is just the symbol for the element 
* Ionic Charge: Sum of nuclear charge and the core electrons (C Z=6 core=1s2 gives ionic charge as +6-2=+4)
* Level of theory: The Exchange-Correlation potential used.
* Atomic-solver: Koelling-Harmon is the default atomic solver. 

### Reference electronic structure.

This section describes the valence states included in the calculation. For Carbon these are the 2s and 2p states. Their occupations and energies are given.

### Pseudopotential Definition (Advanced)
The definitions of each of the non-local projector (aka beta projectors) is given here. 

* Beta - the number of the projector
* l    - angular momentum quantum number
* e    - energy of the corresponding orbital
* Rc   - Cutoff (matching) radius for the orbital 
* scheme - pseudization scheme (qc = qc tuned)
* norm   - 1=norm-conserving 0-ultrasoft (norm not conserved)

This is a standard Ultrasoft pseudopotential with two beta projectors per angular momentum channel. One projector is from an orbital at the boundstate energy (i.e. -0.505Ha for 2s) while the second projector corresponds to a non-bound orbital at an energy of 0.25Ha.

The final line gives the choice of local potential. In this case the local potential is constructed from a l=2 state with the same cutoff radius as for the local projectors.

`Augmentation charge Rinner`. This is specific to the Ultrasoft scheme - and describes the radius outside which the augmentation charge matches the all-electron charge.

`Partial core correction`. As the exchange correlation energy is a non-linear function of charge there is an error introduced if we compute the xc energy of the valence and core electron separately. We therefore include the core charge in the calculation of the xc energy. The core charge is challenging to represent on a grid - and so a pseudized core charge is used. Rc is the cut-off for this pseudized core charge.

## Carbon - Normconserving

```
============================================================                
| Pseudopotential Report - Date of generation  8-07-2020   |                
------------------------------------------------------------                
| Element: C Ionic charge:  4.00 Level of theory: PBE      |                
| Atomic Solver: Koelling-Harmon                           |                
|                                                          |                
|               Reference Electronic Structure             |                
|         Orbital         Occupation         Energy        |                
|            2s              2.000           -0.505        |                
|            2p              2.000           -0.194        |                
|                                                          |                
|                 Pseudopotential Definition               |                
|        Beta     l      e      Rc     scheme   norm       |                
|          1      0   -0.505   1.201     qc      1         |                
|         loc     1   -0.194   1.201     qc      1         |                
|                                                          |                
| No charge augmentation                                   |                
| Partial core correction Rc = 0.839                       |                
------------------------------------------------------------                
| "1|1.2|17|20|23|20N:21L(qc=8)"                           |                
------------------------------------------------------------                
|      Author: Chris J. Pickard, Cambridge University      |                
============================================================  
```

Note that the `Reference Electronic Structure` section is identical to the ultrasoft potential above. This relates to the all-electron atom and is unaffected by the details of the pseudopotential.

From the pseudopotential definition we see there is one beta projector for l=0 (s) and the local potential is set to be l=1 (p). For norm-consering potentials it is common to only need one projector per angular momentum chanel, and for one of the occupied chanels to be represented by the local potential.

There is no charge augmention (this is only needed for ultrasofts) however, a non-linear core correction is used.


## Uranium - J-dependant

```
============================================================                
| Pseudopotential Report - Date of generation  4-07-2020   |                
------------------------------------------------------------                
| Element: U Ionic charge: 14.00 Level of theory: LDA      |                
| Atomic Solver: Dirac (FR)                                |                
|                                                          |                
|               Reference Electronic Structure             |                
|         Orbital         Occupation         Energy        |                
|          6s1/2            2.000           -1.748         |                
|          6p1/2            2.000           -1.101         |                
|          6p3/2            4.000           -0.776         |                
|          7s1/2            2.000           -0.161         |                
|          5f5/2            1.286           -0.147         |                
|          5f7/2            1.714           -0.116         |                
|          6d3/2            0.400           -0.103         |                
|          6d5/2            0.600           -0.085         |                
|                                                          |                
|                 Pseudopotential Definition               |                
|      Beta    l   2j     e      Rc     scheme   norm      |                
|        1     0    1   -1.748   2.106     qc     1        |                
|        2     0    1   -0.161   2.106     qc     1        |                
|        3     1    3   -0.776   2.106     qc     1        |                
|        4     1    1   -1.101   2.106     qc     1        |                
|        5     2    5   -0.085   2.106     qc     1        |                
|        6     2    3   -0.103   2.106     qc     1        |                
|        7     3    7   -0.116   2.106     qc     1        |                
|        8     3    5   -0.147   2.106     qc     1        |                
|       loc    4    0    0.000   2.106     pn     0        |                
|                                                          |                
| No charge augmentation                                   |                
| Partial core correction Rc = 1.472                       |                
------------------------------------------------------------                
| "4|2.1|17|19|22|60N:70N:61N:62N:53N(qc=6,q3=8)"          |                
------------------------------------------------------------                
|      Author: Chris J. Pickard, Cambridge University      |                
============================================================   
```

This pseudopotential is calculated by using a Dirac equation solver including the spin-orbit interaction (FR=fully relativistic).

It is a norm-conserving potential.

There are 14 electrons included in the valence (6s2,7s2,6p6,6d1,5f3). Because of the spin orbit splitting states with different j quantum numbers have different energies. States with l>0 are split into $j=l+1/2$ and $j=l-1/2$ (e.g. the 6p states are split into 6p1/2 and 6p3/2, the 5f into 5f5/2 5f7/2).







