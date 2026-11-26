```
 BEGIN header
  Number of ions            [ION]
  Number of species         [SPE]
  Number of branches        [NBR]
  Number of bins in DOS     [NBN]
 Unit cell vectors (A)
 [CELL_XX  ] [CELL_XY  ] [CELL_XZ  ]
 [CELL_YX  ] [CELL_YY  ] [CELL_YZ  ]
 [CELL_ZX  ] [CELL_ZY  ] [CELL_ZZ  ]
 Fractional Co-ordinates
 [IDX]  [POSITIONX] [POSITIONY] [POSITIONZ] [EL] [MASS         ]
 ...
 END header
 BEGIN GRADIENTS   n   f   |Grad_q f|
     q-pt=[ IDX]  [Q_X     ][Q_Y     ][Q_Z     ]    [WEIGHT       ]
  [idx ][frequency    ]       [ gradient     ]
  ...
     q-pt=[ IDX]  [Q_X     ][Q_Y     ][Q_Z     ]    [WEIGHT       ]
  ...
 END GRADIENTS
 BEGIN DOS   Freq ([unit])  g(f)  [SPEC    ] {[SPEC    ]...}
[FREQ  ] [G(F)    ] [SPECIES ] {GSPECIES ]...}
 ...
  END DOS
```
