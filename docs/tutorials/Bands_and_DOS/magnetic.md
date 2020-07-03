

## Fe

```
%BLOCK LATTICE_CART
      -1.433199999999999       1.433200000000001       1.433200000000001
       1.433200000000001      -1.433200000000000       1.433200000000000
       1.433200000000000       1.433200000000000      -1.433200000000000
%ENDBLOCK LATTICE_CART

%BLOCK POSITIONS_FRAC
 Fe   0.0000000000000000   0.0000000000000000   0.0000000000000000
%ENDBLOCK POSITIONS_FRAC

symmetry_generate

! Kpoint grid for the Groundstate (SCF) calculation
kpoint_mp_grid 8 8 8

! kpoint path through the Brillouin Zone for the Bandstructure
%BLOCK spectral_KPOINT_PATH
0.0 0.0 0.0 !G    
0.5 0.5 0.5 !H           
0.5 0.0 0.0 !N           
0.0 0.0 0.0 !G          
0.75 0.25 -0.25 !P       
0.5 0.0 0.0     !N
%ENDBLOCK spectral_KPOINT_PATH
```

```
task            spectral      ! The TASK keyword instructs CASTEP what to do
spectral_task   bandstructure !
xc_functional   LDA           ! Which exchange-correlation functional to use.
cut_off_energy  500 eV        !
grid_scale      2.0           !
opt_strategy    speed         ! Choose algorithms for best speed
spin            1             ! Set the spin in the original cell to 1.
spin_polarised  true          ! Run a spin polarised calculation
spectral_nbands       6       ! number of bands to compute during the BS run
```

## NiO

JRY to write
