# X-ray Structure Factors

## Basic Theory
The X-ray structure factor (SF) intensities can be measured by diffraction experiments involving either X-rays, $\gamma$-rays or electron beams. It is directly related to the electron density within the unit cell of a material, $n(\mathbf{r})$, by a Fourier transformation[@Coppens1997]:

$$F(\mathbf{H}) = \mathcal{F}[n(\mathbf{r})] = \int_\textrm{unit cell} n(\mathbf{r})\exp(i 2 \pi \mathbf{H} \cdot \mathbf{r}) \mathrm{d}\mathbf{r},$$

where $\mathbf{H} = h \mathbf{a}^* + k \mathbf{b}^* + l\mathbf{c}^*$ is the scattering vector corresponding to the $(hkl)$ plane, with $\mathbf{a}^*, \mathbf{b}^*$ and $\mathbf{c}^*$ being the reciprocal lattice vectors of the conventional unit cell.

Computation of the SF is difficult within plane-wave pseudopotential DFT codes since the total "all-electron'' electron density is not normally directly computed and the FFT grids used to house the pseudised valence electron density do not have enough spatial resolution to capture the rapid oscillations near the atomic cores of the total electron density, requiring large plane-wave energy cutoffs in the order of several thousands of eV. Within CASTEP, we have developed an efficient and accurate approach towards calculating these SFs without having to move to large FFT grids or plane-wave energy cutoffs. Details of this implementation can be found in the paper (CITE PAPER WHEN PUBLISHED) but the key observation that has enabled this development is that the electron density can be separated into atom-centred contributions which can be treated on separate radial grids. The resulting structure factor has the form[@Shmueli2001]:

$$F(\mathbf{H}) = \sum_{j} f_{j} (\mathbf{H}) \exp(i 2\pi \mathbf{H} \cdot \mathbf{r}_{j}),$$

where $f_j(\mathbf{H})$ is an effective atomic scattering factor of atom $j$ within the unit cell, defined to be the Fourier transform of its effective atomic density $\rho_j(\mathbf{r})$:

$$f_j (\mathbf{H}) = \int \rho_j (\mathbf{r}) \exp(i 2 \pi \mathbf{H} \cdot \mathbf{r}) \mathrm{d}{\mathbf{r}}.$$

### Incorporating Thermal Effects
Within experiments, thermal vibrations (i.e. phonons) can modify the (time-averaged) electron density and, hence, SFs. Making the approximation that the electron density assigned to each atom $\rho_j(\mathbf{r})$ directly follows its nuclear motion perfectly, the structure factors can incorporate these thermal vibration effects by including an atomic temperature factor $T(\mathbf{H})$:

$$F(\mathbf{H}) = \sum_j T_j(\mathbf{H}) f_j (\mathbf{H}) \exp(i 2 \pi \mathbf{H} \cdot \mathbf{r}_j).$$

Taking the vibrations of an atom to follow that of a harmonic oscillator, the temperature factor can be shown to be of the form:

$$T(\mathbf{H}) = \exp \left(-\frac{1}{4} \mathbf{H}^\mathbf{T} \mathbf{B} \mathbf{H} \right),$$

where $\mathbf{B}^{jk} = 8 \pi^2 \langle u^j u^k \rangle$ $\langle u^j u^k \rangle$ are the averaged, squared, thermal displacements of the atom. For the case where the vibrations are isotropic, this equation reduces to:

$$T(\mathbf{H}) = \exp \left(-\frac{B |\mathbf{H}|^2}{4} \right),$$

where B is termed the Debye-Waller factor.
## Keywords

Currently, to enable CASTEP (versions 21 and beyond) to calculate X-ray SFs, the desired SFs must be placed between ``CALCULATE_XRD_SF:`` and ``:ENDCALCULATE_XRD_SF`` within the ``devel_code`` block of the ``seed.param`` file. For example, the $(111)$ and $(200)$ and $(220)$ SFs can be calculated by appending the following code to the end of the ``seed.param`` file:

```
%block devel_code
CALCULATE_XRD_SF:
1 1 1
2 0 0
2 2 0
:ENDCALCULATE_XRD_SF
%endblock devel_code
```

Alternatively, if no structure factors are listed, as in:

```
%block devel_code
CALCULATE_XRD_SF:
:ENDCALCULATE_XRD_SF
%endblock devel_code
```
then the SFs on the entire FFT grid will be written out.

Thermal effects can also be incoporated by placing the desired atomic Debye-Waller (DW) factors between ``DW_FACTOR:`` and ``:ENDDW_FACTOR`` within the ``devel_code`` block of the ``seed.param`` file. For isotropic DW factors, the value of the DW factor can be written next to the corresponding atomic symbol as below:

```
%block devel_code
DW_FACTOR:
Mg 0.305
O 0.340
:ENDDW_FACTOR

CALCULATE_XRD_SF:
1 1 1
2 0 0
2 2 0
:ENDCALCULATE_XRD_SF
%endblock devel_code
```

Alternatively, the entire anisotropic displacement tensor of each atomic species may be specified as follows:

```
%block devel_code
DW_FACTOR:
Mg
0.305 0.000 0.000
0.000 0.305 0.000
0.000 0.000 0.305
O
0.340 0.000 0.000
0.000 0.340 0.000
0.000 0.000 0.340
:ENDDW_FACTOR

CALCULATE_XRD_SF:
1 1 1
2 0 0
2 2 0
:ENDCALCULATE_XRD_SF
%endblock devel_code
```
!!! note
    Structure factor calculations are a post-processing calculation, so they can be restarted from a previous DFT calculation's ``.check`` file by using the ``CONTINUATION`` parameter in CASTEP.

## Output Files
The resulting structure factors that have been calculated will be outputted into a file named ``seed.xrd_sf``. For the following inputs:

```
! MgO.param
xc_functional : PBE

%block devel_code
DW_FACTOR:
Mg 0.305
O 0.340
:ENDDW_FACTOR

CALCULATE_XRD_SF:
1 1 1
0 0 2
0 2 2
:ENDCALCULATE_XRD_SF
%endblock devel_code
```

```
! MgO.cell
%BLOCK LATTICE_CART
ang
 4.2112  0.0     0.0
 0.0     4.2112  0.0
 0.0     0.0     4.2112
%ENDBLOCK LATTICE_CART

%BLOCK POSITIONS_FRAC
Mg 0.00 0.00 0.00
Mg 0.50 0.50 0.00
Mg 0.50 0.00 0.50
Mg 0.00 0.50 0.50
O  0.00 0.50 0.00
O  0.50 0.00 0.00
O  0.00 0.00 0.50
O  0.50 0.50 0.50
%ENDBLOCK POSITIONS_FRAC

kpoint_mp_grid 8 8 8

SYMMETRY_GENERATE
```

We get a resulting ```seed.xrd_sf``` file with the output:
```
   h   k   l   Re(F_PAW)   Im(F_PAW)   Re(F_IAM)   Im(F_IAM)    Re(F_PP)    Im(F_PP)  Re(F_core)  Im(F_core)  Re(F_soft)  Im(F_soft)   Re(F_aug)   Im(F_aug)
   1   1   1   11.115757   -0.000000   12.492143   -0.000000   10.926445   -0.000000    0.085890   -0.000000   -9.892234    0.000000   20.922101   -0.000000
   0   0   2   52.877502    0.000000   51.830521   -0.000000   52.626486    0.000000   15.464656   -0.000000   15.585172   -0.000000   21.827675    0.000000
   0   2   2   41.051122    0.000000   40.948429   -0.000000   40.609195    0.000000   14.950468   -0.000000    7.954567   -0.000000   18.146087    0.000000
```

After the header, the structure factors are listed along each row based on the order in which they have been listed in the ```seed.param``` file. Across the columns along each row, the $h, k,l$ vectors are first listed before the real and imaginary components of the SF are listed under ``Re(F_PAW)`` and ``Im(F_PAW)`` respectively. Several other (less accurate) SFs that are commonly found in literature as well as charge contributions to ``F_PAW`` are also listed in columns further to the right, as described below:

Label      | Description
-----------|----------------------------------------------------------------
``F_PAW``  | DFT structure factor with all-electron augmentation charge
``F_IAM``  | Indepedent atom model structure factor; electron densit formed from superposition of atomic electron densities obtained by numerically solving the Koelling-Harmon equation
``F_PP``   | DFT structure factor with pseudised (inaccurate) augmentation charge
``F_core`` | Structure factor contribution to ``F_PAW`` due to the (frozen) core electrons
``F_soft`` | Structure factor contribution to ``F_PAW`` due to the soft valence charge (where augmentation charge contribute is removed)
``F_aug``  | Structure factor contribution due to the all-electron valence augmentation charge
