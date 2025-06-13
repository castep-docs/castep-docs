```
BEGIN header
 Number of ions          [num_ions]
Unit cell vectors (A)
  [CELL_XX             ]  [CELL_XY             ]  [CELL_XZ             ]
  [CELL_YX             ]  [CELL_YY             ]  [CELL_YZ             ]
  [CELL_ZX             ]  [CELL_ZY             ]  [CELL_ZZ             ]
Fractional Co-ordinates
 [IDX]   [POSITION_X          ]  [POSITIONY          ]  [POSITIONZ          ]   [ELEM][MASS                ]
...
END header
{
BEGIN Elastic Constants {xx yy zz yz zx xy} ([PRESSURE_UNIT])
    [ELASTIC_XX          ]    [ELASTIC_YY          ]    [ELASTIC_ZZ          ]    [ELASTIC_YZ          ]    [ELASTIC_ZX          ]    [ELASTIC_XY          ]
...x5
END Elastic Constants
BEGIN Compliance Matrix {xx yy zz yz zx xy} ([PRESSURE_UNIT]^-1)
    [COMPLIANCE_XX       ]    [COMPLIANCE_YY      ]    [COMPLIANCE_ZZ      ]    [COMPLIANCE_YZ       ]    [COMPLIANCE_ZX       ]    [COMPLIANCE_XY       ]
...x5
END Compliance Matrix
BEGIN Elastic Constants [Frozen Ion] {xx yy zz yz zx xy} ([PRESSURE_UNIT])
    [ELASTIC_XX          ]    [ELASTIC_YY          ]    [ELASTIC_ZZ          ]    [ELASTIC_YZ          ]    [ELASTIC_ZX          ]    [ELASTIC_XY          ]
...x5
END Elastic Constants [Frozen Ion]
BEGIN Relaxed Ion Contribution {xx yy zz yz zx xy} ([PRESSURE_UNIT])
    [ELASTIC_XX          ]    [ELASTIC_YY          ]    [ELASTIC_ZZ          ]    [ELASTIC_YZ          ]    [ELASTIC_ZX          ]    [ELASTIC_XY          ]
...x5
END Relaxed Ion Contribution
BEGIN Internal Strain {xx yy zz yz zx xy} ([FORCE_UNIT])
 [ION]   [SPEC]  X    [STRAIN_XX          ]    [STRAIN_YY          ]    [STRAIN_ZZ          ]    [STRAIN_YZ          ]    [STRAIN_ZX          ]    [STRAIN_XY          ]
 [ION]   [SPEC]  Y    [STRAIN_XX          ]    [STRAIN_YY          ]    [STRAIN_ZZ          ]    [STRAIN_YZ          ]    [STRAIN_ZX          ]    [STRAIN_XY          ]
 [ION]   [SPEC]  Z    [STRAIN_XX          ]    [STRAIN_YY          ]    [STRAIN_ZZ          ]    [STRAIN_YZ          ]    [STRAIN_ZX          ]    [STRAIN_XY          ]
...
END Internal Strain
BEGIN Piezoelectric {xx yy zz yz zx xy} ([PIEZO_UNIT])
    [PIEZOELECTRIC_XX    ]    [PIEZOELECTRIC_YY    ]    [PIEZOELECTRIC_ZZ    ]    [PIEZOELECTRIC_YZ    ]    [PIEZOELECTRIC_ZX    ]    [PIEZOELECTRIC_XY    ]
...x2
END Piezoelectric
BEGIN Piezoelectric [Frozen Ion] {xx yy zz yz zx xy} ([PIEZO_UNIT])
    [PIEZOELECTRIC_XX    ]    [PIEZOELECTRIC_YY    ]    [PIEZOELECTRIC_ZZ    ]    [PIEZOELECTRIC_YZ    ]    [PIEZOELECTRIC_ZX    ]    [PIEZOELECTRIC_XY    ]
...x2
END Piezoelectric [Frozen Ion]
BEGIN Relaxed Ion Piezoelectric Contribution {xx yy zz yz zx xy} ([PIEZO_UNIT])
    [PIEZOELECTRIC_XX    ]    [PIEZOELECTRIC_YY    ]    [PIEZOELECTRIC_ZZ    ]    [PIEZOELECTRIC_YZ    ]    [PIEZOELECTRIC_ZX    ]    [PIEZOELECTRIC_XY    ]
...x2
END Relaxed Ion Piezoelectric Contribution
BEGIN Unfolded K-point Set
[INDEX   ]    [Q_X           ]    [Q_Y           ]    [Q_Z           ]
...
END Unfolded K-point Set
BEGIN dBand/dStrain    xx yy zz yz zx xy   ([ENERGY_UNIT])
[N_BAND] [NUNFLD] [N_SPIN]
[BND_ID] [KPT_ID] [SPN_ID]     [ELASTIC_YY          ]    [ELASTIC_ZZ          ]    [ELASTIC_YZ          ]    [ELASTIC_ZX          ]    [ELASTIC_XY          ]
...
END dBand/dStrain
}
```
