!!! Note
    The Koopmans' compliance functionality for determining the Hubbard U parameter was introduced in CASTEP version 26 - ensure you are using this version or later!


## .param file
The following keywords are available to allow specification of calculating Koopmans' compliance parameters in the .param file:
```
task : koopmans
koopmans_method : hubbard
koopmans_LR_method : finitedifference
```
The only currently implemented type of Koopmans' compliance technique is Hubbard, which itself only has the method of finite differences implemented. The default for the latter two parameters are thus as shown above and can therfore be omitted in this case.


## .cell file
To define which species are to have their Hubbard $U$ values calculated, use the `hubbard_alpha` block in the .cell file:
```
%BLOCK hubbard_alpha
Fe
%ENDBLOCK hubbard_alpha
```
This will use the default of $0.1$ eV as the `hubbard_alpha` value. To define the values yourself, use:
```
%BLOCK hubbard_alpha
eV
Fe d : 0.2
%ENDBLOCK hubbard_alpha
```
This implicitly defines $\alpha_{I}$ values for all Fe atoms in the system. Once the base $\alpha_{I}=0\;\forall\;I$ calculation has been performed, an additional $6$ non-self consistent (NSC) and $6$ self consistent (SC) calculations will be computed for one of each inequivalent Fe site. These $6$ calculations will have perturbations applied to the respective ion of: $-3\alpha_{I}$, $-2\alpha_{I}$, $-\alpha_{I}$, $\alpha_{I}$, $2\alpha_{I}$ and $3\alpha_{I}$.

!!! Example
    In Fe<sub>3</sub>O<sub>4</sub>, we have $2$ inequivalent Fe sites, with multiplicity of $2$ and $1$. Let's define Fe-1 and Fe-2 as equivalent, and Fe-3 unique. The $6$ NSC and $6$ SC calculations will be performed with $\alpha_{I}\neq0$ on Fe-1 (and $\alpha_{I}=0$ on all other atoms), and the corresponding occupancies obtained for use in the linear fittings. Fe-2 will then be solved via symmetry, and will not require any $\alpha_{I}\neq0$ computations. Finally, Fe-3 will have its $6$ NSC and $6$ SC calculations performed with $\alpha_{I}\neq0$.

If different $\alpha_{I}$ values are required for different sites:
```
%BLOCK hubbard_alpha
eV
Fe 1 d : 0.08
Fe 2 d : 0.08
Fe 3 d : 0.12
%ENDBLOCK hubbard_alpha
```
This is unlikely to be required, but may be used if any linear fitting warnings are spotted in the output. See [U from Linear Response - Warnings/Errors](alpha-warnings-errors.md).


## Farm parallelism
All perturbative ($\alpha_{I}\neq0$) calculations are independent from all others. Therefore, due to the large number required, it is often beneficial to utilise farm parallelism. This can split the $\alpha_{I}$ tasks across nodes to speed up computation time. To indicate that you would like the `CASTEP` calculation to be farm parallelised, indicate this in the .param file:
```
num_farms = 4
```
This will require the number of processes used to be at least $4$, and will proceed to utilise $\mathbf{k}$-point, $\mathbf{G}$-vector or band parallelism within each farm block of processes if possible. Each farm will essentially run its own `CASTEP` calculation (all running in parallel) and have its own output .castep file. The powerful aspect of this is that when each farm has finished its $\alpha_{I}$ computations, the results will be collated on the master farm node and the $U$ values computed as normal. The computation
of the $U$ values after the $\alpha_{I}$ calculations have been performed is very quick, and does not need any level of parallelism.

!!! Example
    Suppose you would like to $\mathbf{k}$-point parallelise a calculation across $4$ $\mathbf{k}$-points and $3$ farms. This would require $12$ processes. The $12$ processes would be split into $3$ blocks of $4$. For each of those $3$ farms, the $4$ processes would be split across the $4$ $\mathbf{k}$-points.

An Mn d states $U$ calculation in MnO, where the $6$ $\alpha_{I}$ calculations are farm parallelised over $3$ farms, will have $3$ .castep files named `MnO_farm001.castep`, `MnO_farm002.castep` and `MnO_farm003.castep`. Each file will indicate the work that each farm will perform, for example in MnO_farm001.castep:
```
  This farm will perform the following calculations:
    1st alpha calc out of  6 for channel    Mn              1  d
    2nd alpha calc out of  6 for channel    Mn              1  d
```

!!! Tip
    Each farm will conduct its own base $\alpha_{I}\neq0\;\forall\;I$ calculation, which makes the method less efficient as this only needs to be computed once. The recommended workflow is to conduct a `singlepoint` calculations as normal (no farm parallelism required). Then, run a `continuation` calculation with the output .check file from the `singlepoint` run for the $\alpha_{I}$ calculations **with** farm parallelism. Each farm will read in the base wavefunction and density from the .check file and conduct its share of $\alpha_{I}$ calculations as normal.

