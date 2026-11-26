```
#$magres-abinitio-v1.0
# See http://www.ccpnc.ac.uk/pmwiki.php/CCPNC/Fileformat for format definition and code samples and libraries
[calculation]
calc_code CASTEP
calc_code_version  23.1
calc_code_hgversion 81dc23eb6+  LDA-fix  Tue May 24 15:32:31 2022 +0100
calc_code_platform linux_x86_64_gfortran
calc_name h
calc_comment
calc_xcfunctional PBE
calc_cutoffenergy    200.00000000 eV
calc_pspot H 1|0.8|0.8|0.6|2|6|8|10(qc=6)
calc_kpoint_mp_grid 1 1 1
calc_kpoint_mp_offset       0.25000000      0.25000000      0.25000000
[/calculation]
[atoms]
units lattice Angstrom
lattice           3.7042404783592575E+00          0.0000000000000000E+00          0.0000000000000000E+00          2.2681931225473627E-16          3.7042404783592575E+00          0.0000000000000000E+00          2.2681931225473627E-16          2.2681931225473627E-16          3.7042404783592575E+00
units atom Angstrom
symmetry x,y,z
atom H       H   1          0.0000000000000000E+00          0.0000000000000000E+00          0.0000000000000000E+00
[/atoms]
[magres]
units ms ppm
ms H    1          1.5935205760550641E+01         -2.9465207825065915E-02         -2.9465208436315116E-02         -2.9465209603394566E-02          1.5935205760174004E+01         -2.9465210306093507E-02         -2.9465207935827645E-02         -2.9465208297740641E-02          1.5935205759657912E+01
ms H11111 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0
isc_fc H    1 H    1 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0
[/magres]
[magres_old]
============
Atom: H        1
============
H        1 Coordinates      0.000    0.000    0.000   A

TOTAL Shielding Tensor

              15.9352     -0.0295     -0.0295
              -0.0295     15.9352     -0.0295
              -0.0295     -0.0295     15.9352

H        1 Eigenvalue  sigma_xx      15.9647 (ppm)
H        1 Eigenvector sigma_xx       0.3571     -0.8144      0.4573
H        1 Eigenvalue  sigma_yy      15.9647 (ppm)
H        1 Eigenvector sigma_yy       0.7343     -0.0579     -0.6764
H        1 Eigenvalue  sigma_zz      15.8763 (ppm)
H        1 Eigenvector sigma_zz      -0.5774     -0.5774     -0.5774

H        1 Isotropic:       15.9352 (ppm)
H        1 Anisotropy:      -0.0884 (ppm)
H        1 Asymmetry:        0.0000

[/magres_old]
```
