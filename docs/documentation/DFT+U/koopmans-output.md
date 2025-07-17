
## Work to do
After the base $\alpha_{I}=0\;\forall\;I$ calculation, a description of the work to be performed will be written to the .castep file:
```
 Performing   6 alpha calculations for the following   3 channels:
   Mn              1  d
   Fe              1  d
   Co              1  d

 The remaining   9 channels are computed by the following symmetry mappings:
   Mn              2  d          ->          Mn              1  d
   Fe              2  d          ->          Fe              1  d
   Co              2  d          ->          Co              1  d
   Co              3  d          ->          Co              1  d
   Co              4  d          ->          Co              1  d
   Co              5  d          ->          Co              1  d
   Co              6  d          ->          Co              1  d
   Co              7  d          ->          Co              1  d
   Co              8  d          ->          Co              1  d
```

Helpful hints as to the progress of the calculation will then be given, such as:
```
 Doing calc  1/ 6 for Mn              1 d -> alpha =  -0.24000000        eV
```
The beginning and end of each of the non-self consistent (NSC) and self consistent (SC) calculations will also be indicated. An SCF cycle output will be written for each of the SC calculations akin to the base calculation.


## Occupancy data
After the completion of the NSC and SC calculations for a given $\alpha_{I}$, the occupancy data of all ions of $U$ interest will be written:
```
    Occupancy data for Mn              1 d -> alpha =  -0.24000000 eV
  ----------------------------------------------------------------------------
       Species         Ion        l          NSC occ           SC occ
  ============================================================================
        Mn               1        d           6.3872           6.2727
        Mn               2        d           6.2167           6.2244
        Fe               1        d           6.9979           7.0029
        Fe               2        d           6.9979           7.0029
        Co               1        d           8.2707           8.2810
        Co               2        d           8.2709           8.2811
        Co               3        d           8.2709           8.2811
        Co               4        d           8.2709           8.2811
        Co               5        d           8.2711           8.2813
        Co               6        d           8.2711           8.2813
        Co               7        d           8.2711           8.2813
        Co               8        d           8.2712           8.2815
  ============================================================================
```
The header here indicates which ion has had the $\alpha_{I}$ potential applied. This data, along with the data from all other $\alpha_{I}$ calculations, would (in principle) allow a user to compute the Hubbard $U$ value for each ion manually if any sanity checks were required.


## U values
Once all the work is complete, the calculated $U$ values will be output:
```
                     Hubbard U values
                     ================

   ====================================================
         Species           Ion    l        U / eV
   ----------------------------------------------------
         Mn                 1     d        3.458
         Mn                 2     d        3.458
         Fe                 1     d        3.569
         Fe                 2     d        3.569
         Co                 1     d        5.870
         Co                 2     d        5.870
         Co                 3     d        5.870
         Co                 4     d        5.870
         Co                 5     d        5.870
         Co                 6     d        5.870
         Co                 7     d        5.870
         Co                 8     d        5.870
   ====================================================
```
Each of the Mn, Fe and Co are all equivalent sites here, and thus the computed $U$ values for each species are all identical as expected.

