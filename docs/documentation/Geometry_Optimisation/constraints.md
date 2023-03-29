## Atomic constraints

CASTEP can impose various forms of linear or non-linear constraints upon the positions of the atoms. This can be used with all forms of geometry optimization and 
molecular dynamics.

Some simple short cuts exist, such as to keep all the atoms fixed:

```
FIX_ALL_IONS : T
```
or to fix the Centre of Mass:
```
FIX_COM      : T
```

It is also possible to specify constraints on individual atoms, using the `IONIC_CONSTRAINTS` block. The simplest case is to control which atoms remain fixed during 
a geometry optimisation. e.g.

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

The last example in particularly useful in the case of molecular crystals, when you might want to allow the H atoms to move but keep all of the heavy atoms in the 
positions determined by diffraction.


To fix the individual Cartesian components of an atom's position use the full syntax of the `ionic_constraints` block, where each constraint removes one degree of 
freedom. For example
```
%BLOCK IONIC_CONSTRAINTS
       1       W       1    1.0000000000    0.0000000000    0.0000000000
       2       W       1    0.0000000000    1.0000000000    0.0000000000
       3       W       1    0.0000000000    0.0000000000    1.0000000000
       4       W       2    1.0000000000    0.0000000000    0.0000000000
%ENDBLOCK IONIC_CONSTRAINTS
```

The 1st line says that constraint number 1 is to fix the x coordinate of Tungsten atom 1. The 2nd line says that constraint 
number 2 is to fix the y coordinate of Tungsten atom 1. etc. To fix an atom in 3D requires 3 constraints to remove all 3 
degrees of freedom.

The ionic_constraints block can also be used to impose any arbitary linear constraint, such as to restrict an atom to move in a plane or along a line, or to fix the 
centre of mass. A constraint may involve more than 1 atom, and hence can span mulitple lines, but each constraint operates on 1 degree of freedom. It cannot be used 
to fix a bond length - that is a non-linear constraint - see below for more details.

The general syntax for constraint $i$ operating on atom $j$ of element X at position $r^j$ is
```
%BLOCK IONIC_CONSTRAINTS
...
    i X j a1 a2 a3
...
%ENDBLOCK IONIC_CONSTRAINTS
```
and the constraint is specfied as
\begin{equation}
   C^i={\bf a^i}\cdot{\bf r^j}
\end{equation}

where $C^i$ is given by the initial conditions. For example to fix the second S atom to move in the plane parallel to $y=x$ use this:
```
%BLOCK IONIC_CONSTRAINTS
    1 S 2 -1 1 0
%ENDBLOCK IONIC_CONSTRAINTS
```


## Cell Constraints

Cell constraints can be used with all forms of geometry optimization and molecular dynamics that allow the cell size/shape 
to vary. Some simple short cuts exist, such as to keep the unit cell fixed during the optimisation
```
FIX_CELL : T
```

or to fix the volume (but not the shape) of the unit cell
```
FIX_VOL  : T
```


It is also possible to apply an arbitary set of constraints to the cell angles and cell lengths using the `CELL_CONSTRAINTS` block.

```
%BLOCK CELL_CONSTRAINTS
  a       b     c
  alpha  beta  gamma
%ENDBLOCK CELL_CONSTRAINTS
```

Setting an element to zero means to keep it fixed. Two or more elements set to the same positive integer, means that these elements should be kept equal during the 
geometry optimisation. For example
```
%BLOCK CELL_CONSTRAINTS
       0       0       0
       4       5       6
%ENDBLOCK CELL_CONSTRAINTS
```
would keep all cell lengths fixed, and allow the three cell angles to vary independently, and  
```
%BLOCK CELL_CONSTRAINTS
       0       0       0
       4       4       6
%ENDBLOCK CELL_CONSTRAINTS
```
would enforce $\alpha=\beta\neq\gamma$ and keep the cell lengths fixed.

## Symmetry
The application of symmetry with constraints (for ionic positions and/or cell vectors) needs to be considered carefully. In general, if symmetry is on, then there is 
no need to add a constraint to explicitly impose a restriction that is implied by the symmetry. If there is a need for an additional restriction, then that can be 
added on top of the symmetry, but the user needs to be careful that the additional constraint does not conflict with symmetry. If in doubt, turn symmetry off and 
impose all the desired constraints explicitly.


## Non-linear Constraints

CASTEP can also support non-linear constraints, such as fixed bond length, in both molecular dynamics, and also in geometry 
optimization if using `GEOM_METHOD=DELOCALISED`:
```
%BLOCK NONLINEAR_CONSTRAINTS
    constraint_type atom1 atom2 (atom3 (atom 4))
...
%ENDBLOCK NONLINEAR_CONSTRAINTS
```
where the first element specifies a constraint type (distance, bend angle or torsion angle). Then depending on the type of 
constraint, either 2, 3 or 4 atoms need to be specified, and the corresponding quantity (distance, bend angle or torsion angle) is held 
constant at the initial value.

As for (linear) ionic constraints, atoms are specified by species and number within that 
species. In addition, it is necessary to specify which periodic image of the cell the atom is located in (so constraints can straddle a cell boundary).

For instance
```
%BLOCK NONLINEAR_CONSTRAINTS
    distance H 4 0 0 0   O 2 0 1 0
        bend H 5 0 0 0   C 1 1 0 1   H 2 0 0 0
     torsion H 6 0 0 0   H 3 1 0 0   H 1 0 0 1   H 9 1 1 1 0 
%ENDBLOCK NONLINEAR_CONSTRAINTS
```
specifies:

* the distance between the 4th hydrogen atom and the 2nd oxygen atom in the adjacent ( 0 1 0 ) cell
* the bend angle defined by the 5th hydrogen atom, the 1st carbon atom in the ( 1 0 1 ) cell and the 2nd hydrogen atom
* the torsion angle defined by 4 hydrogen atoms, etc.


