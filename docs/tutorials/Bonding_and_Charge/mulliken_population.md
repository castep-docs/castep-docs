
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

### Comparing to Other Diamond Structures

To understand the results of this further, we will compare them to 2 other diamond structures - GaAs and diamond (as in carbon-diamond).


For both of these cases, we will use an identical `.param` file (just rename them to `diamond.param` and `GaAs.param`). The cell files will be slightly different - for diamond we will change the `lattice_abc` block lattice dimensions with 2.52$\mathring{\text{A}}$ (rather than 3.8$\mathring{\text{A}}$ - the structure is the same but the cell size is different). Naturally the `Si`'s in the `positions_frac` block need to be replaced with `C`'s

Towards the end of `diamond.castep` we find

```
Atomic Populations (Mulliken)
-----------------------------
Species          Ion     s       p       d       f      Total   Charge (e)
==========================================================================
C               1     1.076   2.924   0.000   0.000   4.000     0.000
C               2     1.076   2.924   0.000   0.000   4.000     0.000
==========================================================================

            Bond                   Population      Length (A)
======================================================================
          C 1 -- C 2                    3.00        1.54318
======================================================================
```
The results are rather similar but there are a couple of interesting things to note:

- The ratio of the populations in s and p orbitals is closer to 1:3, which is expected for sp^3^ hybridization - this indicates that the bonds are much more perfectly hybridized, meaning it's more overlapped: this indicates stronger bonding, as well as showing that silicon is a semimetal
- The population of electrons in the bonds is the same (indicating that the same type of bonding is present), but the bond length is smaller - again indicating more overlap and thus stronger bonding.

Now we will compare it with GaAs. The same procedure is used, except the lattice length is now 3.93$\mathring{\text{A}}$ and the atoms in `positions_frac` should be `Ga` and `As` (it doesn't matter which one goes in which position/line).

We get an output looking like this:

```
Atomic Populations (Mulliken)
-----------------------------
Species          Ion     s       p       d       f      Total   Charge (e)
==========================================================================
Ga              1     1.180   1.743   9.994   0.000  12.917     0.083
As              1     1.488   3.595  10.000   0.000  15.083    -0.083
==========================================================================

            Bond                   Population      Length (A)
======================================================================
         Ga 1 -- As 1                   0.34        2.44652
======================================================================
```

Despite having the same structure, the results are very different now:

- Unlike before, the Ga and As ions have charges on them - this is indicative of ionic/polar character
- There is now a much smaller population in the Ga-As bond. This indicates less covalent character
- Especially in the case of Ga, the s:p shell ratio is far off from 1:3 - this again indicates that the bonding is not like in the cases above

## Diatomic molecules

Next we will examine a few diatomic molecules - HF, HCl and HBr.

Here is the `HF.cell` file

```
%block lattice_abc
5 5 5
90 90 90
%endblock lattice_abc

%block positions_abs
H 2 2 2
F 2.91 2 2
%endblock positions_abs
```

Since we are just trying to look at a single diatomic molecule, the cell is defined rather simply - an arbitrarily large cube for the cell (making it too large would make the calculation take longer, but make it too small and it'll simulate a loose crystal rather than a disperse molecule), 1 atom placed about in the middle, and the 2nd atom placed a bond length away from it - in this case F is 0.91$\mathring{\text{A}}$ to the right of the H . The bond lengths can be found on a [database](https://cccbdb.nist.gov/), or you may perform a [geometry optimisation](../../../documentation/Geometry_Optimisation/overview) to find it yourself if you wish.

Using a `param` file identical to before and running castep yields this towards the end of `HF.castep`

```
Atomic Populations (Mulliken)
-----------------------------
Species          Ion     s       p       d       f      Total   Charge (e)
==========================================================================
H               1     0.309   0.000   0.000   0.000   0.309     0.691
F               1     1.960   5.731   0.000   0.000   7.691    -0.691
==========================================================================

            Bond                   Population      Length (A)
======================================================================
          H 1 -- F 1                    0.34        0.91000
======================================================================
```
There are a couple of interesting things to note:

- Like GaAs (and unlike Si and diamond), there are 2 opposite charges on both atoms. However, the charge is significantly larger, indicating that the molecule is highly polar/ionic.
- The population of the H-F bond is rather low - this indicates that the molecule has little covalent character

We will now compare HF to very similar molecules - HCl and HBr - keeping the trend of hydrogen bonded to a group 7 element. The `param` files are completely identical and in the `cell` files the bond lengths used are 1.275$\mathring{\text{A}}$ for HCl and 1.44$\mathring{\text{A}}$ for HBr.

HCl has the result

```
Species          Ion     s       p       d       f      Total   Charge (e)
==========================================================================
  H               1     0.620   0.000   0.000   0.000   0.620     0.380
  Cl              1     1.936   5.443   0.000   0.000   7.379    -0.379
==========================================================================

                 Bond                   Population      Length (A)
======================================================================
               H 1 -- Cl 1                   0.56        1.27500
======================================================================
```

While HBr has

```
Atomic Populations (Mulliken)
-----------------------------
Species          Ion     s       p       d       f      Total   Charge (e)
==========================================================================
H               1     0.824   0.000   0.000   0.000   0.824     0.176
Br              1     1.908   5.267   0.000   0.000   7.176    -0.176
==========================================================================

            Bond                   Population      Length (A)
======================================================================
          H 1 -- Br 1                   0.53        1.44000
======================================================================
```
The most significant thing this shows us is that the charges on both atoms decrease as you go down group 7. This successfully demonstrates something we already know: as you go down group 7, the electronegativity decreases. The same principle can be applied to estimate relative electronegativities of different atoms.
