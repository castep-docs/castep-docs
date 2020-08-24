## Atomic constraints

The `ionic_constraints` block controls which atoms remain
fixed during a geometry optimisation. e.g.

```
%BLOCK IONIC_CONSTRAINTS
fix: C 1				!fix position of atom C 1
%ENDBLOCK IONIC_CONSTRAINTS
```
Some further examples include


    fix: all            !fix all atoms 
    fix: C N            !fix species C and N 
    fix: C 1            !fix position of atom C 1 
    fix: C{1,3,5-10}    !fix positions of atoms C1, C3, C5,C6,C7,C8,C9,C10 
    fix: all unfix: H   !fix positions of all atoms except H

The last example in particularly useful in the case of molecular
 crystals, when you might want to allow the H atoms to move but keep
 all of the heavy atoms in the positions determined by diffraction.


To fix the individual Cartesian components of an atom's
position use the full syntax of the `ionic_constraints` block e.g.
```
%BLOCK IONIC_CONSTRAINTS
       1       W       1    1.0000000000    0.0000000000    0.0000000000
       2       W       1    0.0000000000    1.0000000000    0.0000000000
       3       W       1    0.0000000000    0.0000000000    1.0000000000
       4       W       2    1.0000000000    0.0000000000    0.0000000000
%ENDBLOCK IONIC_CONSTRAINTS
```
The 1st line says that constraint number 1 is to fix the x coordinate of  
Tungston atom 1. The 2nd line says that constraint number 2 is to fix the y coordinate of Tungston atom 1. etc etc.



## Cell Constraints

To keep the unit cell fixed during the optimisation
```
FIX_CELL : T
```

To fix the volume of the unit cell
```
FIX_VOL  : T
```


It is also possible to apply constraints to the cell angles and cell lengths using the CELL_CONSTRAINTS block.

```
%BLOCK CELL_CONSTRAINTS
  alpha  beta  gamma
  a       b     c
%ENDBLOCK CELL_CONSTRAINTS
```
Setting an element to zero means to keep it fixed. Two or more elements set to the same positive integer, means that these elements should be kept equal during the geometry optimisation. For example

```
%BLOCK CELL_CONSTRAINTS
       0       0       0
       4       5       6
%ENDBLOCK CELL_CONSTRAINTS
```
would keep all cell lengths fixed, and allow the three cell angles to vary independently.  
```
%BLOCK CELL_CONSTRAINTS
       0       0       0
       4       4       6
%ENDBLOCK CELL_CONSTRAINTS
```
would enforce $\alpha=\beta\neq\gamma$ and keep the cell lengths fixed.

!!! Symmetry
    Should we have a discussion about the implications of symmetry here?


## Non-linear Constraints

!!! Missing
