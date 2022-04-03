
By default castep will calculate the Mulliken Population analysis at the end of every calculation (the keyword `popn_calculate` is set to `true` by default).

## Silicon

Here is a cell file. You can use the icon in the top right of the box to copy and paste the text. Save it in a file `silicon.cell`

```
%block lattice_abc
3.8 3.8 3.8
60 60 60
%endblock lattice_abc
!
! Atomic co-ordinates for each species.
! These are in fractional co-ordinates wrt to the cell.
!
%block positions_frac
Si 0.00 0.00 0.00
Si 0.25 0.25 0.25
%endblock positions_frac
!
! Analyse structure to determine symmetry
!
symmetry_generate
!
! Specify M-P grid dimensions for electron wavevectors (K-points)
!
kpoint_mp_grid 4 4 4

```

Here is a param file. You can use the icon in the top right of the box to copy and paste the text. Save it in a file `silicon.param`

```
xc_functional : LDA
cutoff_energy : 500 eV
spin_polarised : false
```

Run castep. Toward the end of the file `silicon.castep` you will find


```
Atomic Populations (Mulliken)
-----------------------------
Species          Ion     s       p       d       f      Total   Charge (e)
==========================================================================
Si              1     1.356   2.644   0.000   0.000   4.000     0.000
Si              2     1.356   2.644   0.000   0.000   4.000     0.000
==========================================================================

            Bond                   Population      Length (A)
======================================================================
         Si 1 -- Si 2                   2.99        2.32702
======================================================================
```
The atoms are not charged overall, and there is a large bond population. This is all indicative of a strong covalent bond.

##To finish
