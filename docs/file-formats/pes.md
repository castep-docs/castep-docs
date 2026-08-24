```
 BEGIN header

  + + +  P E S  S C A N  O U T P U T  F I L E  + + +

   Date started: [DATE_AND_TIME               ]

 =============================================================================
   Input Parameters:
 =============================================================================

   Job: [JOB_TYPE]
   Probe species: [SPEC]
  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Energy unit: [E_UNIT]
   Force  unit: [F_UNIT]
  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Cell Vectors (Bohr)
 [CELL_XX ] [CELL_XY ] [CELL_XZ ]
 [CELL_YX ] [CELL_YY ] [CELL_YZ ]
 [CELL_ZX ] [CELL_ZY ] [CELL_ZZ ]
  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
   Number of samples in a: [COUNT_A ]
   Number of samples in b: [COUNT_B ]

 =============================================================================

 =============================================================================
   Potential energy surface scan results:
 =============================================================================
      a:      b:      c:                E:{    f_opt:      time:     clock:}
 END header
 BLOCK DATA
 [FRACA] [FRACB] [FRACC]  [ENERGY        ]{ [FORCE   ] [TIME    ] [CLOCK   ]}
 ...
 ENDBLOCK DATA
 =============================================================================
   Time taken to complete scan [TIME        ] seconds
 =============================================================================
```
