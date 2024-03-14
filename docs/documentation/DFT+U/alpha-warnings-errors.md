

## Convergence
As with the base $\alpha_{I}=0$ calculation, convergence of the non-self consistent (NSC) and self consistent (SC) calculations is required. If any of the NSC or SC calculations fail to converge, a note will be made in the .castep file and .err files will be created. If any of the `hubbard_alpha` specification in the .cell file is very large, then the potential may result in difficulties for the solver to find the constrained ground state. In this case, consider using a lower `hubbard_alpha`
setting.

Alternatively, consider:

- Checking that the atomic positions make physical sense in your .cell file.
- Checking `fix_occupancy : true` is **not** set in your .param file if your system is actually metallic.
- Checking `spin = 0` is **not** set in your .param file if your system is actually magnetic. Also consider initialising a non-zero spin.
- If the density mixing scheme is in place, consider the parameters `mixing_scheme`, `mix_cut_off_energy`, `mix_charge_amp` and `mix_spin_amp`.


## Linear regression
An automatic check will take place to investigate the validity of the linear fitting of the occupancies against $\alpha_{I}$ values. If you notice:
```
Warning: non-negligble (> 0.01) quadratic terms for Co               1  d
 Consider applying a smaller Hubbard alpha potential to this ion
```
in your .castep file then consider reducing the supplied `hubbard_alpha` value for that species. This may have happened because the strength of the given $\alpha_{I}$ potential is so strong that the linear fitting scheme is no longer valid, and higher order polynomial coefficients are non-negligble.

If you still obtain this warning after reducing the supplied $\alpha_{I}$ value, then consider increasing the `cut_off_energy` parameter and/or density of the $\mathbf{k}$-point grid. This error may be occuring due to poor convergence with respect to these parameters.

Another consideration is that the achieved ground state wavefunctions, whilst converged, are unphysical. This could be because you have used $U=0$ when a sensible ground state may only be achievable with $U>0$. Consider applying a $U$ value to the culprit species; the computed $U$ value at the end of this calculation should then be consider a **correction** to the originally input $U$ value.


## Matrix inversions
The inversion of each of the $\chi$ matrices requires the rows/columns to all be linearly independent. If the inversion of any of the matrices fails, the user will see the following error in the .castep file:
```
 Error in inversion of occupancy matrices - this could be because U is near 0
```
One can imagine an ion that does not respond to the applied $\alpha_{I}$ perturbations, and as a result, has linearly dependent rows/columns in its $\chi$ matrices. In this case, the $U$ value is likely near $0$. If this occurs for an ion that you suspect should indeed have a non-negligble $U$, then consider increasing the `cut_off_energy`, $\mathbf{k}$-point grid density and/or applying a precursor $U$ value to the ion as discussed in the section above.

