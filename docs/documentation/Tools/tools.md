This page lists various analysis codes (some supplied with the CASTEP distribution as well as other third-party codes) which interoperate with CASTEP. Some of these programs require additional interface codes/scripts to take CASTEP output as their input, etc.


## Pre-processing Tools

* [c2x](http://www.c2x.org.uk/) (also bundled with the CASTEP distribution) reads and converts a selection of crystal structure file formats including `.cif` which relate to DFT and perform structure manipulations. It can rotate cells, make supercells, add vacuum space, create slabs and nanotubes.
* [Cif2Cell](https://sourceforge.net/projects/cif2cell/) is a tool to generate the geometrical setup for various electronic structure codes from a CIF (Crystallographic Information Framework) file. Also supports supercell generation and formats for visualisation tools.
* [SeeK-path](https://www.materialscloud.org/work/tools/seekpath) is a k-path finder that provides band paths compatible with space group symmetry, and an interactive 3D visualiser.

## Convergence Testing

* [castepconv](https://github.com/CCP-NC/castepconv) CASTEPconv (also bundled with the CASTEP distribution) automates convergence testing of plane-wave cutoff, k-point density and fine grid scale. Based on a proforma input, it prepares the files, analyses the output and generates summary data files. A standalone version is shipped with CASTEP source. Later versions depend upon ASE and can be downloaded from github (https://github.com/CCP-NC/castepconv) and can also generate plots.

## General Postprocessing

* [castep-outputs](https://github.com/oerc0122/castep_outputs) is a Python package to read and parse all of the output files of CASTEP into a standard form. This is the recommended CASTEP output parser interface. A simple CLI tool is provided to dump a `.json` file, but its main use is intended as a library to be called from future analysis codes. This is the recommended interface for developers of Python analysis tools. Currently this reads and parses all CASTEP text-format files but not the binary ones.
* [castepxbin](https://github.com/zhubonan/castepxbin.git) is a collection of readers for CASTEP binary output files `.check`,`.castep_bin`, `.orbitals` etc.
* [c2x](http://www.c2x.org.uk/) (also bundled with the CASTEP distribution) can read CASTEP binary output files `.check`,`.castep_bin`,`.orbitals` and extract cell geometry data, electron densities , wavefunctions and prepare for visualization and further analysis. It can interpolate densities via a combination of trilinear and Fourier interpolation, integrate densities and calculate their dipole moments, and analyse bands for inversion symmetry. It can be used to produce output formats compatible with XCrysDen, VESTA, VMD and Jmol amongst others, and can also produce 1D data in a format suitable for gnuplot.

## Spectroscopy Modelling Tools

* *dispersion.pl* and *dos.pl* (part of CASTEP distribution) are tools for producing band-structure and density of states plots from a CASTEP .bands file. They also support creating phonon dispersion and DOS plots. Dispersion.pl will perform simple modelling of a powder Raman spectrum for a specified laser frequency and temperature.
* [OptaDOS](http://www.tcm.phy.cam.ac.uk/~ajm255/optados/) is a code for calculating optical, core-level excitation spectra along with full, partial and joint electronic density of states (DOS).
* [SUMO](https://smtg-bham.github.io/sumo/) is a suite of tools for electronic band structure and phonon dispersion analysis and plotting.
* [PDielec](https://johnkendrick.github.io/PDielec/introduction.html) calculates model powder infra-red spectra including optical cavity effects from CASTEP (and other) phonon calculations.
* *orbitals2bands* (part of CASTEP distribution) Reads a  CASTEP `.orbitals` file from a spectral/bandstructure calculation, analyses the band crossings and generates a `.bands` file with reordered eigenvalues for producing a bandstructure plot with crossings taken into account.
* *bs_sc2pc* (part of CASTEP distribution)  is a band structure unfolding tool for CASTEP. It implements the effective band structure method described by Popescu and Zunger http://dx.doi.org/10.1103/PhysRevB.85.085201|10.1103/PhysRevB.85.085201, and is distributed as part of the CASTEP academic distribution. Peter Brommer and David Quigley (2014) "Automated effective band structures for defective and mismatched supercells." J. Phys.: Condens. Matter 26 485501. http://dx.doi.org/10.1088/0953-8984/26/48/485501|10.1088/0953-8984/26/48/485501.
* [band_up](https://github.com/band-unfolding/bandup) is another program for performing band unfolding calculations on defective supercells.
* [easyunfold](https://pypi.org/project/easyunfold/) is yet another band unfolding tool, with CASTEP support.
* [PhononUnfolding](https://fwzheng.github.io/PU/PU.html) is a program for unfolding of phonon dispersions.
* *mode_follow*  (part of CASTEP distribution) reads a `.phonon` output file and generates a sequence of `.cell` input files for single-point energy calculations to compute the energy profile along a mode for plotting and to analyse for anharmonicity or double-well depth.
* [molpdos](../Delta_SCF/molpdos.md) (part of CASTEP distribution)  calculates DOS, and DOS projected onto molecular states, as part of a [Delta SCF](../Delta_SCF/molpdos.md) calculation.
* [Abins](http://docs.mantidproject.org/v3.9.1/algorithms/Abins-v1.html) is a plugin for Mantid which allows scientists to compare experimental and theoretical inelastic neutron scattering spectra. AbINS uses the phonon data calculated by DFT programs, such as CASTEP, to generate an INS spectra of a powder sample, which makes it easier to establish a connection between theory and experiments.
* [Euphonic](https://euphonic.readthedocs.io/en/stable/) is a library and front-end for calculating the inelastic neutron scattering spectral function in 4-D (**Q**,$\omega$) space to compare with data from a in a single-crystal time-of-flight INS spectrometer.
* [OCLIMAX](https://sites.google.com/site/ornliceman/download) is a free program for simulation of inelastic neutron scattering using vibrational frequencies and polarization vectors as input. It can perform simulations on both powder and single crystal samples, and the input phonon data can be obtained from first-principles or empirical calculations.
* [phonopy](https://phonopy.github.io/phonopy/) is an open source package for phonon calculations at harmonic and quasi-harmonic levels.
* [phono3py](https://phonopy.github.io/phono3py/) calculates phonon-phonon interaction and related properties using the supercell approach. These properties include the lattice thermal conductivity, joint density of states and the phonon lifetimes.

## Visualisation

* [CrystalMaker](http://crystalmaker.com/crystalmaker/specs/index.html) is a visualisation suite for designing and investigating crystal and molecular structures. It also provides support for modelling and animation of atomistic and electronic properties.
* [JMOL](http://jmol.sourceforge.net/) is an open-source browser-based HTML5 viewer and stand-alone Java viewer for chemical structures in 3D with features for molecules, crystals, materials, and biomolecules.  It is able to read CASTEP `.cell`, `.castep`, `.den_fmt`, .`elf-fmt`, `.geom`, `.md`, `.phonon` and more, with rendering of crystal structure, densities, [ELF](../Groundstate/ELF.md) etc. and animation of optimization or MD trajectories and phonon vibrations.
* [MagresView](https://www.ccpnc.ac.uk/magresview/magresview/magres_view.html) is a tool for visualization and processing of computed solid-state NMR parameters.
* [OVITO](https://ovito.org/) is a scientific visualization and analysis software for atomistic and particle simulation data.
* [VESTA](http://jp-minerals.org/vesta/en/) is a 3D visualization program for structural models, volumetric data such as electron/nuclear densities, and crystal morphologies.
* [XCrysDen](http://www.xcrysden.org/) is a crystalline and molecular structure visualisation program aiming at display of isosurfaces and contours, which can be superimposed on crystalline structures and interactively rotated and manipulated. (`.c2x` can convert CASTEP output to the `.xsf` format, and other converters are supplied as part of the CASTEP distribution)
* [castep2fs](https://github.com/zachary-hawk/castep2fs) is a CASTEP utility for taking a CASTEP output and producing publication quality Fermi Surfaces and related quantities.
* *castep2cube* (Part of CASTEP distribution) reads `.check` or `.castep_bin` output files and converts the electron density to Gaussian `.cube` format which many other visualisation tools can read.

## Databases, Big Data and Workflow

* [NOMAD](https://repository.nomad-coe.eu/) supports CASTEP and its users. The service includes uploading, downloading, sharing, assigning DOIs, and more. Storing is guaranteed for at least 10 years, a requirement set by several funding agencies. The NOMAD Repository is also the only repository in Computational Materials Science that is recommended by NATURE Scientific Data. The repository currently contains over 10<sup>8</sup> entries - see the [archive](https://metainfo.nomad-coe.eu/nomadmetainfo_public/archive.html) for the latest data.
* [aiida-castep](https://aiida-castep.readthedocs.io/en/latest/index.html) Interface to [AiiDA](https://www.aiida.net/) workflow infrastructure.
* [Soprano](https://ccp-nc.github.io/soprano/) is a Python library meant to help crystallographers with the search and classification of new crystal forms for a given material. It provides a number of classes and functions to handle large amounts of candidate structures, compare them, sort them and cluster them.

## Structure Prediction

* *CASTEP_GA* (part of CASTEP distribution) is a crystal structure prediction tool based upon a modified Genetic Algorithm (GA) for periodic systems. It can handle 3D bulk materials, and also 2D surface reconstructions/interfaces and 1D edges of nanoribbons etc. It has a population of parent crystals, that are mutated and bred to make candidate children, that are then fed to CASTEP for (local) structure optimization. It is also possible to add structures that are randomly generated according to a random space group. After a number of generations, a candidate global minimum enthalpy structure can emerge. The functionality has also been extended to a MOGA (Multi-Objective GA) so that a Pareto front of optimal structures is generated, with minimum enthalpy on one axis, and a user defined property on the other. Example scripts that can be used to generate this property value are included in the distribution. Finally, recent work has been on the CHGA (Convex Hull GA) approach, wherein the stoichiometry is optimized as well, resulting in the generation of a multi-dimensional convex hull. More detailed documentation is included in the 'ReadMe' directory.
* [AIRSS](https://www.mtg.msm.cam.ac.uk/Codes/AIRSS) (''Ab initio Random Structure Searching'') is a very simple, yet powerful and highly parallel, approach to structure prediction. It generates random sensible structures and relaxes them to nearby minima. The sensible random structures are constructed so that they have reasonable densities, and atomic separations. Additionally they may embody crystallographic, chemical or prior experimental/computational knowledge. Beyond these explicit constraints the emphasis is on a broad, uniform, sampling of structure space. It is tightly integrated with CASTEP and has been used in a number of landmark studies to find novel phases of materials.
* [Calypso](http://www.calypso.cn/) (''Crystal structure AnaLYsis by Particle Swarm Optimization'') is an efficient structure prediction code. The approach requires only chemical compositions for a given compound to predict stable or metastable structures at given external conditions and can be used to predict/determine the crystal structure and design multi-functional materials.
* [USPEX](http://uspex-team.org/) (''Universal Structure Predictor: Evolutionary Xtallography'') is a method developed by the Oganov laboratory for crystal structure prediction. It can very efficiently handle molecular crystals (including those with flexible and very complex molecules) and can predict stable chemical compositions and corresponding crystal structures, given just the names of the chemical elements. In addition to this fully non-empirical search, USPEX allows one to predict also a large set of robust metastable structures and perform several types of simulations using various degrees of prior knowledge.
* [XtalOPT](http://xtalopt.github.io/)  is a free and truly open source evolutionary algorithm designed for a priori crystal structure prediction implemented as an extension to the [Avogadro](http://avogadro.cc/) molecular editor.

## MD analysis

* *geom2xyz.pl*, *geom2xsf*, *geom2dcd* (part of CASTEP distribution) are filters to convert CASTEP `.geom` and `.md` output files to other trajectory formats and may be used to interface with a number of other analysis codes.
* *md_to_phonon* (part of CASTEP distribution) is a simple python tool for reading a CASTEP trajectory file and performing various phonon-based analyses, including mass-weighted velocity autocorrelation function (VACF) vs frequency (which is close to the experimental VDOS). It can also project out a particular eigenmode and eigenvector from a user specified peak in the VACF and write as a single-mode CASTEP phonon file for visualization by other tools, e.g. JMol.
* [MDANSE](https://mdanse.org/) (''Molecular Dynamics Analysis for Neutron Scattering Experiments'') is a python application designed for computing properties that can be directly compared with neutron scattering experiments such as the coherent and incoherent intermediate scattering functions and their Fourier transforms, the elastic incoherent structure factor, the static coherent structure factor or the radial distribution function.
* [LiquidLib](https://z-laboratory.github.io/LiquidLib/) is a "comprehensive toolbox for analyzing classical and ab initio molecular dynamics simulations of liquids and liquid-like matter with applications to neutron scattering experiments".
* [potfit](https://www.potfit.net/) attempts to fit a model
forcefield to a data set provided. There is a python converter tool in the CASTEP distribution for reading a CASTEP trajectory file and generating an atomic configuration file to be used as input for the [potfit](https://www.potfit.net/) code.
* [MDTEP](http://www.tcm.phy.cam.ac.uk/castep/MD/node19.html) is a simple code for analysing MD trajectories and calculating thermodynamic properties such as the heat capacity and the velocity autocorrelation function.


## Machine-Learned Potentials

* [QUIP](https://github.com/libAtoms/QUIP) is  is a collection of software tools to carry out molecular dynamics simulations. It implements a variety of interatomic potentials and tight binding quantum mechanics. See https://pubs.aip.org/aip/jcp/article/159/4/044803/2904492/Machine-learned-acceleration-for-molecular.

## Transport

* [ShengBTE](http://www.shengbte.org/) is a software package for solving the Boltzmann Transport Equation for phonons. Its main purpose is to compute the lattice contribution to the thermal conductivity of bulk crystalline solids, but nanowires can also be treated under a hypothesis of diffusive boundary conditions.
* [AlmaBTA](http://www.almabte.eu/|AlmaBTE) extends the ShengBTE approach currently employed for homogeneous bulk materials, into the mesoscale, to fully describe thermal transport from the electronic ab initio level, through the atomistic one, all the way into the mesoscopic structure level.
* [BoltzTraP](https://www.imc.tuwien.ac.at//forschungsbereich_theoretische_chemie/forschungsgruppen/prof_dr_gkh_madsen_theoretical_materials_chemistry/boltztrap/) is a program for calculating the semi-classic transport coefficients.
* [BoltzTrap2](https://www.tuwien.at/en/tch/tc/theoretical-materials-chemistry/boltztrap2) is a modern implementation of the smoothed Fourier interpolation algorithm for electronic bands that formed the base of the original and widely used BoltzTraP code. One of the most typical uses of BoltzTraP is the calculation of thermoelectric transport coefficients as functions of temperature and chemical potential in the rigid-band picture. However, many other features are available, including 3D plots of Fermi surfaces based on the reconstructed bands.
* [EMC](https://github.com/afonari/emc) (''Effective Mass Calculator'') implements calculation of the effective masses at the bands extrema using finite difference method. There are two versions of the program: written in FORTRAN and Python.

## Miscellaneous

* [ASE](https://wiki.fysik.dtu.dk/ase/index.html) is a set of tools and Python modules for setting up, manipulating, running, visualizing and analyzing atomistic simulations. The code is freely available under the GNU LGPL license. It can interface with many different electronic structure codes.
* [Bader](http://theory.cm.utexas.edu/henkelman/code/bader/) is a tool to perform Bader charge analysis on a charge density grid. Typically in molecular systems, the charge density reaches a minimum between atoms and this is a natural place to separate atoms from each other. Besides being an intuitive scheme for visualizing atoms in molecules, Bader's definition is often useful for charge analysis. For example, the charge enclosed within the Bader volume is a good approximation to the total electronic charge of an atom.
* [ATAT](https://www.brown.edu/Departments/Engineering/Labs/avdw/atat/) (Alloy Theoretic Automated Toolkit) is a collection of alloy theory tools developed by Axel van de Walle.
* [CASINO](https://vallico.net/casinoqmc/) is a computer program system for performing quantum Monte Carlo (QMC) electronic structure calculations that has been developed by members of the Theory of Condensed Matter group in the Cambridge University physics department, and their collaborators, over more than 20 years.  It is capable of calculating incredibly accurate solutions to the Schrödinger equation of quantum mechanics for realistic systems built from atoms. An interface `castep2casino` is supplied with the CASTEP distribution.
* *Emacs mode* (part of CASTEP distribution) is an emacs major mode for CASTEP input files with datatype based syntax highlighting and inbuilt help functionality.
* [i-PI](http://ipi-code.org/) is a package for performing molecular dynamics and path-integral MD via a unix socket driver interface. More details [elsewhere](/documentation/Molecular_Dynamics/pimd/) in this site.

## Commercial Codes

[BIOVIA Materials Studio](https://www.3ds.com/products-services/biovia/products/molecular-modeling-simulation/biovia-materials-studio/) is a suite of graphical tools and codes for quantum and classical simulation of materials, and is how CASTEP is distributed commercially.
