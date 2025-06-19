CASTEP writes output data in a variety of files. Some of these will be in human readable ASCII format (i.e. plaintext) and
can be read with commands such as `less` or `more` on linux, or with a simple text editor (textedit, notepad etc). Other files will be in binary format and are designed to be read or processed with an external program.  See  [Tools](../Tools/tools.md) for software and libraries to read and analyse them.


## Groundstate


* `.castep`
ASCII. CASTEP's main outputfile.

* `.bib`
ASCII. Bibtex file containing citations to the methods CASTEP has used in the calculation.

* `.check`
Binary. This checkpoint file contains the results of the calculation including the groundstate charge density and wavefunctions. It is typically a very large file. Will be read by CASTEP when performing a continuation calculation. Also read by postprocessing software such as c2x or euphonic.

* `.check_bak`
Binary. backup of the checkpoint file.

* `.castep_bin`
Binary. This file is identical to `.check` except that does not contain the wavefunctions. Therefore it is usually much smaller than the `.check` file, making it suitable for archiving a calculation. It may also be processed by euphonic, c2x or other software which can read checkpoint file.

* `.cst_esp`
Binary. The local part of the Kohn-Sham potential (Vloc + Hartree + XC).

* `.usp`
ASCII. Pseudoptential data, written for each species. See the page on [reading usp headers](../Pseudopotentials/reading_headers.md).

* `.uspso`
ASCII. Pseudoptential data, written for each species. This is the J-dependant version of the `.usp`. See the page on [reading usp headers](../Pseudopotentials/reading_headers.md).

* `.beta`
Xmgrace (.agr) format. Beta projectors for each generated pseudopotential. Only written if a test configuration `[]` is present in the OTF string.

* `.pwave`
Xmgrace (.agr) format. Pseudo-wavefunctions for each generated pseudopotential. Only written if a test configuration `[]` is present in the OTF string.

* `.econv`
Xmgrace (.agr) format. Isolated atom energy cutoff convergence for each generated pseudopotential. Only written if a test configuration `[]` is present in the OTF string.

* `.bands`
ASCII. Kohn-Sham eigenvalues at the requested k-points. Can be used to plot band structures or density of states. Note that the eigenvalues are given in atomic units (Hartree).

* `.den_fmt`
ASCII. Charge density. Only written if `write_formatted_density : T `.

* `.pot_fmt`
ASCII. Groundstate local potential  (Vloc + Hartree + XC) (See `.cst_esp`). Only written if `write_formatted_potential : T `.

* `.chdiff`
Binary. Difference between the groundstate charge density and a superposition of atomic densities. Only written if `calculate_densdiff : T`

* `.chdiff_fmt`
ASCII. same data as `.chdiff` in human readable format. Only written if `calculate_densdiff : T` and `write_formatted_density : T `.

* `.xrd_sf`
ASCII. X-ray structure factors. See the [documentation page](../XRD/overview.md).

*  `.elf`
Binary. Result of ELF calculation.

* `.elf_fmt`
ASCII.  Result of ELF calculation.Only written if `write_formatted_elf : T `.

## Geometry Optimisation

* `*.geom`
ASCII. State of the system (coordinates, unit cell etc) at each step of the geometry optimisation. See for specification. Can be used to animate the geometry optimisation and can be read directly by Jmol.

## Molecular Dynamics

* `*.md`
ASCII. State of the system (coordinates, unit cell etc) at each step of the molecular dynamics simulation. Same format as the `.geom` file.  See for specification. Can be used to animate the trajectory, and can be read directly by Jmol.

* `*.hug`
ASCII. Hugoniot data for hugoniostat MD.

## Spectral

* `.pdos_bin`
Binary. Matrix elements used for plotting a projected density of states. Used by Optados.

* `.ome_bin`
Binary. Matrix elements used for calculating optical properties. Used by Optados.

* `.dome_bin`
Binary. Diagonal elements of the optical matrix elements. Used by Optados to plot densities of states / spectral properties using adaptive smearing.

* `.elnes_bin`
Binary. Matrix elements used for plotting the core-loss spectrum. Used by Optados.

* `.orbitals`
Binary. Kohn-Sham states at each kpoints. Used by `orbital2bands` to make a reorganised `.bands` file for a cleaner looking bandstructure.

## Phonon and Efield

* `.phonon`
ASCII. Phonon eigenvalues and eigenvectors.

* `.phonon_dos`
ASCII. Phonon branch gradients and density-of-states when param keyword `phonon_calculate_dos` is true.

* `.efield`
ASCII. Mode oscillator strengths and frequency-dependent permittivity tensor in the ir band.

## Electron-Phonon coupling

* `.epme`
ASCII. Electron-phonon matrix elements.

* `.epme_bin`
Binary. Electron-phonon matrix elements.

## Elastic Constants

* `.elastic`
ASCII. Elastic constants, compliance matrix, Frozen ion constants, Internal Strain and Piezoelectric tensors

## TDDFT

* `.tddft`
ASCII. TDDFT state band projection analysis and TDDFT excitation energies.

## Magres

* `.magres`
ASCII. Contain the NMR tensors (depending on `magres_task` shielding, EFG or J). Read by MagresView or the Soprano python libraries.

* `_current.dat`
ASCII. Written if `MAGRES_WRITE_RESPONSE=True`. Used to compute NICS (nucleus independent chemical shifts) see https://www.ccpnc.ac.uk/docs/nics .

## Transition state search

* `.ts`
ASCII. See the specification in the [documentation pages](../Transition_State_Search/neb.md).
