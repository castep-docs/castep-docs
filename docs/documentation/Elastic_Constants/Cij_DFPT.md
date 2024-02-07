# Elastic Constants from DFPT

This method for calculating the elastic constants closely follows approach of Hamann *et al* described in [^1]^,^[^2]. In [^1] Hamann *et al* shows how to treat strain as a perturbation with in the framework of Density Functional Perturbation Theory (DFPT), allowing the response of the electronic states to a strain to be calculated and from them the second derivaitve of the energy with respect to a strain and another perturbation, the elastic constants being the second derivative with respect to two strains.

The elastic constants may be defined allowing or not allowing internal atomic displacements, “relaxed-ion” or “frozen-ion”. The frozen-ion quantities are computed by the DFPT calculation, however these are often of little physical relevance on their own. In [^2] it is shown how to combine various of repsonse properties of the cystal such as the dynamical matrix and Born effective charges to calculation the correction to the frozen-ion quantities to obtain the relaxed-ion quantitites.

When strains and electric fields are simultaneously present, care is needed in the interpretation of the effects on the material. In short, one must be careful to distinguish between “proper” and “improper” piezoelectric constants; the difference is describe thoroughly in the appendix of [^2].

[^1]: Hamann, D. R. *et al*, Phys. Rev. B 71 035117 (2005) *Metric tensor formulation of strain in density-functional perturbation theory*
[^2]: Wu, X. *et al*, Phys. Rev. B 72 035105 (2005) *Systematic treatment of displacements, strains, and electric fields in density-functional perturbation theory*

## How to run a strain response calculation

The calculation of elastic constants via this method is currently enabled via developer code. Adding the line `CALC_ELASTIC` to the `devel_code` block in the `.param` file in the following way:

```text
%Block devel_code
CALC_ELASTIC
%endBlock devel_code
```

will cause CASTEP to attempt a strain response calculation once it has completed the task specified by the task keyword, i.e. if the task is set to a geometry optimisation, once the geometry calculation has completed sucessfully the strain response calculation will run. This will compute the strain response of the system for a symmetry reduced set of perturbations which will enable the frozen-ion elastic constants to be computed. For details on how to compute more extensive properities see below.

## Computatble Properties

* The frozen-ion elastic constants - this computes the second derivative of the energy with respect to two sets of strains, but ingnores the relaxation of the ions due to change in the ionic forces under strain. This is computed by default in any strain response calculation.
* The internal strain force response - this computes the mixed second derivative of the energy with repect to strain and the atomic positions, i.e. the derivative of the ionic forces with respect to a strain. This is not computed by default and is enabled by the following devel code:

```text
%Block devel_code
CALC_ELASTIC
ELASTIC:
INTERNAL_STRAIN
:ENDELASTIC
%endBlock devel_code
```

* The frozen-ion proper piezoelectric constants - this computes the mixed second derivative of the energy with respect strain and an applied efield, but ingnores the relaxation of the ions due to change in the ionic forces under strain/efield perturbation. This is not computed by default and is enabled by the following devel code:

```text
%Block devel_code
CALC_ELASTIC
ELASTIC:
INTERNAL_STRAIN
PIEZOELECTRIC
:ENDELASTIC
%endBlock devel_code
```

The relaxed-ion version of the elastic constants and the piezoelectric constants can also be computed, however not purely from an strain response calculation. The relaxed-ion tensors require additional response calculations in order to compute the correction to the frozen-ion tensors, see below.

### Relaxed Ion Elastic Constants

In order to calculate the relaxed-ion elastic constants, the frozen ion elastic constants are calculated, the internal strain force response must also be calculated as well as the gamma point phonon modes, see equation 15 of ref [^2]. The simplest way to ensure CASTEP computes all those values is to run the `Phonon` task with the `phonon_kpoint_mp_grid` set to `1 1 1` in the `.cell` file and the appropriate `devel_code` block to subsequently run an elastic constants calculation, including calculation of the internal strain force response tensor.

### Relaxed Ion Proper Piezoelectric Constants

In order to calculate the relaxed ion Piezoelectric constants, the frozen ion piezoelectric constants are calculated, the internal strain force response must also be calculated as well as the gamma point phonon modes and the Born effective charges, see equation 16 of ref [^2]. The simplest way to ensure CASTEP computes all those values is to run the `Phonon+Efield` task with the `phonon_kpoint_mp_grid` set to `1 1 1` in the `.cell` fileand the appropriate `devel_code` block to subsequently run an elastic constants calculation, including calculation of the internal strain force response tensor and the frozen-ion proper piezoelectric constants.

### Keywords

Keywords have not yet been added for the strain response calculations. Fine control over the Sternheimer solver, i.e. convergence tolerances etc, currently piggy-backs off the equivalent efield parameters. E.g. to set the energy convergence tolerance for the strain repsonse calculations, one sets a value for `EFIELD_ENERGY_TOL` instead.

## Finite Displacement Method

In the case that the Linear response approach fails, or you are using functionality not compatiable with Linear Response methods, see below, there is also a finite displacement alternative. This works by applying a small positive strain to the system, recalculating the ground state for this perturbed system and repeating for a negative strain. The elastic constants and internal strain force response tensor can then be calculated a centered difference derivative of the stress and the forces.

Things to note:

* The method desribed above is a 3-point stencil finite-difference derivative. In practice, calculations make use of 5-point stencil.
* Piezoelectric constants cannot currently be calculated via the finite displacement code path.

The finite displacement implementation can be chosen via the following `devel_code`.

```text
%BLOCK devel_code
CALC_ELASTIC
ELASTIC:
USE_FD
INTERNAL_STRAIN
:ENDELASTIC
%ENDBLOCK devel_code
```

This approach differs from the python script approach and materials studio approach, both of which strain the system and then run a fixed cell geometry optimisation to find the stress tensor once the ions in the unit cell have relaxed. This negates the requirement for a phonon calculation to determine the relaxed ion elastic constants.

## Limitations

As with phonon and efield calculations there are several bits of functionality which are not fully implemented for linear response calculations. For elastic constants calculations these include:

* Ultrasoft psuedopotentials. (Norm Conserving Pseudopotentoals must be used).
* Non-Local Exchange-Correlation functionals, i.e. Hartree-Fock based methods.
* Meta-GGA functionals, e.g. RSCAN.
* Dispersion Correction Schemes.

For all of the above functionality one must rely on the Finite Displacement method described above, which will be used automatically when the above setting are used and the elastic constants are requested.

Efield and phonon calculations can make can make use of a `ALLBANDS` solver when solving the Sternheimer equation and calculating the response of the system to perturbations. The `ALLBANDS` solver is not available for Elastic constants calculations and we instead rely on the density mixing/Green's function method.

## Example Calculation

Below is the example input `.cell` and `.param` file to run a `Phonon+Efield` calculation for Quartz followed by an elastic constants calculation. This will generate values for the relaxed-ion elastic constants, the internal strain force response and the relaxed-ion Piezoelectric constants which will be written to the `.castep` file and the `.elastic` file.

### Example Input

#### Example `.cell.` File

```text
%BLOCK lattice_cart
2.35936443299494       -4.08653907151816       0.0
2.35936443299494        4.08653907151816       0.0
0.0                     0.0                    5.48672213137782
%ENDBLOCK lattice_cart

%BLOCK POSITIONS_FRAC
   O                0.359583516061271       0.285630774468240       0.266655506195778
   O               -0.285630774468240       0.073952741593031       0.933322172862444
   O               -0.073952741593031      -0.359583516061271       0.599988839529111
   O                0.285630774468240       0.359583516061271      -0.266655506195778
   O                0.073952741593031      -0.285630774468240       0.066677827137555
   O               -0.359583516061271      -0.073952741593031       0.400011160470889
   Si               0.449373149804166       0.000000000000000       0.166666666666667
   Si               0.000000000000000       0.449373149804166       0.833333333333333
   Si              -0.449373149804166      -0.449373149804166       0.500000000000000
%ENDBLOCK POSITIONS_FRAC

%BLOCK species_pot
O     NCP
Si    NCP
%ENDBLOCK species_pot

symmetry_generate

kpoints_mp_grid 3 3 2

phonon_kpoint_mp_grid 1  1  1

snap_to_symmetry
```

#### Example `.param` File

```text
task                : phonon+efield
opt_strategy        : speed

fix_occupancy       : true
cut_off_energy      : 300 eV
FINITE_BASIS_CORR   : Manual
BASIS_DE_DLOGE      : -204.670591 eV

xc_functional       : LDA_PW

calculate_polarisation : true
phonon_sum_rule     : false
born_charge_sumrule : false
calculate_raman     : false

iprint              : 1

efield_energy_tol   : 1.0e-7
phonon_energy_tol   : 1.0e-6
elec_force_tol      : 1.0e-5

%block devel_code
CALC_ELASTIC
ELASTIC:
INTERNAL_STRAIN
PIEZOELECTRIC
#USE_FD
:ENDELASTIC
%endblock devel_code
```

### Example Output

The above CASTEP input generates the following output in the `.castep` file.

N.B. This calculation is severly underconvereged and will the resultant calculated quantities are highly non physical, this is demonstrative output only.

```text
 ===============================================================================
          Elastic Constants Tensor (GPa)
 -------------------------------------------------------------------------------
    313.969309   -53.473669   -43.501739    11.738548     0.000000    -0.000000
    -53.473669   313.969309   -43.501739   -11.738548    -0.000000    -0.000000
    -43.501739   -43.501739   332.111499     0.000000    -0.000000     0.000000
     11.738548   -11.738548     0.000000   198.855435    -0.000000     0.000000
      0.000000    -0.000000    -0.000000    -0.000000   198.855435    11.738548
     -0.000000    -0.000000     0.000000     0.000000    11.738548   183.721489
 ===============================================================================

 ===============================================================================
          Elastic Constants Tensor (Frozen Ion) (GPa)
 -------------------------------------------------------------------------------
    484.968245   -53.187639   -10.943063    17.975538     0.000000    -0.000000
    -53.187639   484.968245   -10.943063   -17.975538    -0.000000    -0.000000
    -10.943063   -10.943063   467.964848    -0.000000     0.000000     0.000000
     17.975538   -17.975538    -0.000000   292.717459    -0.000000    -0.000000
      0.000000    -0.000000     0.000000    -0.000000   292.717459    17.975538
     -0.000000    -0.000000     0.000000    -0.000000    17.975538   269.077942
 ===============================================================================

 ===============================================================================
          Relaxed-Ion Correction to Elastic Constants (GPa)
 -------------------------------------------------------------------------------
   -170.998937    -0.286030   -32.558677    -6.236990     0.000000    -0.000000
     -0.286030  -170.998937   -32.558677     6.236990    -0.000000     0.000000
    -32.558677   -32.558677  -135.853349     0.000000    -0.000000     0.000000
     -6.236990     6.236990     0.000000   -93.862024     0.000000     0.000000
      0.000000    -0.000000    -0.000000     0.000000   -93.862024    -6.236990
     -0.000000     0.000000     0.000000     0.000000    -6.236990   -85.356453
 ===============================================================================

 ===============================================================================
          Compliance Matrix (GPa^-1)
 -------------------------------------------------------------------------------
      0.003373     0.000641     0.000526    -0.000161    -0.000000     0.000000
      0.000641     0.003373     0.000526     0.000161     0.000000     0.000000
      0.000526     0.000526     0.003149    -0.000000     0.000000     0.000000
     -0.000161     0.000161    -0.000000     0.005048     0.000000    -0.000000
     -0.000000     0.000000     0.000000     0.000000     0.005048    -0.000323
      0.000000     0.000000     0.000000    -0.000000    -0.000323     0.005464
 ===============================================================================

 ===============================================================================
                               Elastic Properties                               
 -------------------------------------------------------------------------------
                            x              y              z
 -------------------------------------------------------------------------------
  Young's Modulus ::     296.459903     296.459903     317.582263     (GPa)

 -------------------------------------------------------------------------------
                        xy        xz        yx        yz        zx        zy    
 -------------------------------------------------------------------------------
  Poisson Ratios  :: -.190127  -.155889  -.190127  -.155889  -.166996  -.166996

 -------------------------------------------------------------------------------
                          Voigt          Reuss          Hill          
 -------------------------------------------------------------------------------
   Bulk Modulus   ::      75.455091      75.295229      75.375160     (GPa)
  Shear Modulus   ::     189.654956     188.712303     189.183630     (GPa)

 -------------------------------------------------------------------------------
                                 Speed of Sound                                 
 -------------------------------------------------------------------------------
                            x              y              z
 -------------------------------------------------------------------------------
                  x      105.347623            NaN            NaN     (A/ps)
  (Anisotropic)   y             NaN     105.347623            NaN     (A/ps)
                  z             NaN            NaN     108.348549     (A/ps)

 Assuming Isotropic material 
  Longitudinal waves ::    107.613398   (A/ps)
   Transverse waves  ::     81.775446   (A/ps)
 ===============================================================================

 ===============================================================================
          Force-response internal strain tensor (eV/A)
       xx           yy           zz           zy           zx           yx
 -------------------------------------------------------------------------------
    O        1
 X  -6.18050283  10.77727915 -10.27087364   0.16125782  -8.56311238  -0.50804513
 Y  -4.93015722  30.11084223  -4.10026605   6.99992833   0.00136678   6.24674833
 Z  -8.47585956  12.54457301 -16.24474799  -1.93407528 -10.89247457   0.61809442
    O        2
 X -26.22414346   2.11864239   8.68637139   6.77828368   3.17958667 -14.23393220
 Y  -8.09932137  -0.51009607  -6.84470447  -4.74277072   6.61839264   0.55424639
 Z   7.82475034  -3.75603689 -16.24474799  -8.46612204   7.12119561   8.79306709
    O        3
 X  10.31618731   9.19253744   1.58450226  -6.69970494   3.03874964 -12.30083995
 Y -14.01333869  -2.55792889  10.94497052  -4.60193368  -6.85959598  15.28746426
 Z   6.75417940  -2.68546594 -16.24474799  10.40019733   3.77127896  -9.41116151
    O        4
 X  -6.18050283  10.77727915 -10.27087364   0.16125782   8.56311238   0.50804513
 Y   4.93015722 -30.11084223   4.10026605  -6.99992833   0.00136678   6.24674833
 Z   8.47585956 -12.54457301  16.24474799   1.93407528 -10.89247457   0.61809442
    O        5
 X -26.22414346   2.11864239   8.68637139   6.77828368  -3.17958667  14.23393220
 Y   8.09932137   0.51009607   6.84470447   4.74277072   6.61839264   0.55424639
 Z  -7.82475034   3.75603689  16.24474799   8.46612204   7.12119561   8.79306709
    O        6
 X  10.31618731   9.19253744   1.58450226  -6.69970494  -3.03874964  12.30083995
 Y  14.01333869   2.55792889 -10.94497052   4.60193368  -6.85959598  15.28746426
 Z  -6.75417940   2.68546594  16.24474799 -10.40019733   3.77127896  -9.41116151
    Si       1
 X  22.16989036 -12.24012343 -11.10886574 -10.58370537  18.05457602  -4.29439061
 Y  -4.30503980 -12.89382102  19.24111987 -18.05457602 -10.26392328 -12.24627175
 Z  20.65077093 -20.65077093  -0.00000000  19.68712136 -11.36636482 -11.92272816
    Si       2
 X  22.16989036 -12.24012343 -11.10886574 -10.58370537 -18.05457602   4.29439061
 Y   4.30503980  12.89382102 -19.24111987  18.05457602 -10.26392328 -12.24627175
 Z -20.65077093  20.65077093  -0.00000000 -19.68712136 -11.36636482 -11.92272816
    Si       3
 X  -0.16286275 -19.69667109  22.21773147  20.68773761   0.00000000  -0.00000000
 Y  -0.00000000   0.00000000  -0.00000000  -0.00000000  21.00751970 -19.68437447
 Z   0.00000000  -0.00000000  -0.00000000  -0.00000000  22.73272964  23.84545631
 ===============================================================================

 ===============================================================================
          Piezoelectric Constants Tensor (C/m^2)
       xx           yy           zz           zy           zx           yx
 -------------------------------------------------------------------------------
 X  -0.24726143   0.24726896  -0.00000047   0.17957656   0.00000000   0.00000000
 Y   0.00000719  -0.00000719  -0.00000000  -0.00000088  -0.17958362   0.24726537
 Z   0.00000000  -0.00000000   0.00000000   0.00000000   0.00000575   0.00000177
 ===============================================================================

 ===============================================================================
          Piezoelectric Constants Tensor (Frozen Ion) (C/m^2)
       xx           yy           zz           zy           zx           yx
 -------------------------------------------------------------------------------
 X   0.22623436  -0.22623436   0.00000000  -0.22372671   0.00000000  -0.00000000
 Y  -0.00000000   0.00000000   0.00000000   0.00000000   0.22372671  -0.22623436
 Z   0.00000000   0.00000000   0.00000000   0.00000000   0.00000000   0.00000000
 ===============================================================================

 ===============================================================================
          Relaxed-Ion Correction to Piezoelectric Tensor (C/m^2)
       xx           yy           zz           zy           zx           yx
 -------------------------------------------------------------------------------
 X  -0.47349579   0.47350332  -0.00000047   0.40330327   0.00000000   0.00000000
 Y   0.00000719  -0.00000719  -0.00000000  -0.00000088  -0.40331033   0.47349973
 Z   0.00000000  -0.00000000   0.00000000   0.00000000   0.00000575   0.00000177
 ===============================================================================
```
