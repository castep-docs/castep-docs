# Long-range dispersion corrections

## Why and when are long range-dispersion corrections needed

## Topics
* What is dispersion and when do you need it?
* What are the families of schemes available
* Using dispersion corrections in castep
  * tags
  * restrictions (e.g. numerical forces / castep versions / compiler flags)
* Grimme
  * What it is / when applicable
  * How to compile with this
* vdW DFs ?



## Summary of methods in CASTEP




<!-- ## Types of correction

At the moment, CASTEP only seems to support semiclassical methods

### Semiclassical

### Nonlocal density-based
vdW-DF 

### Effective one-electron potentials  -->

### Main .param file keywords 

**`SEDC_APPLY`**: 
only use this option for CASTEP $\geq$ 8. ``true`` turns on dispersion correction.    
**`SEDC_SCHEME`**: The semi-empirical dispersion/van der Waals correction scheme to use. Default is `NONE`, other possible values are:


| SEDC_SCHEME       | Available from CASTEP version                          | Compatible XC functionals                                | Elements supported (e.g. up to Z=70)  | Stresses | Phonons<sup>*</sup>   |
|-------------------|--------------------------------------------------------|----------------------------------------------------------|---------------------------------------|----------|-----------|
| TS                | Predates 2012                                          | PBE, PBE0, PBE1PBE, BLYP, B3LYP, AM0, RPB, PBESOL, PW91  | Up to Z=54 with first row Lanthanides | Analytic | DFPT & FD |
| TSSURF            | Not sure if working                                    |                                                          |                                       |          |           |
| TSSCS             | Not sure if working                                    |                                                          | Up to Z=54 with first row Lanthanides | Analytic |           |
| MBD* (Alias: MBD) | 2015? Rewritten (and fixed) for CASTEP 18              | PBE, PBE0, PBE1PBE, HSE03, HSE06, RSCAN                  | Up to Z=54 with first row Lanthanides | Numeric  | FD        |
| G06 (= D2)        | Predates 2012                                          | PBE, BLYP,  BP86, B3LYP, TPSS                            | Up to Z= 54                           | Analytic | DFPT & FD |
| D3                | CASTEP 20 ([Compilation instructions](#D3compilation)) | PBE, PBE0, HF                                            |                                       | Analytic | FD        |
| D3-BJ             | CASTEP 20 ([Compilation instructions](#D3compilation)) | PBE, PBE0, HF                                            |                                       | Analytic | FD        |
| OBS               | Predates 2012                                          | LDA, PW91                                                | Up to Z=57                            | Analytic | DFPT & FD |
| JCHS              | Predates 2012                                          | PBE, BLYP, B3LYP, TPSS                                   | H, C, N, O, F, Cl, Br                 | Analytic | DFPT & FD |
| XDM               | CASTEP 20                                              | PBE                                                      | Up to Z=102                           | Analytic | FD        |
<sup>*</sup> DFPT: Density functional perturbation theory; FD: finite displacement. 


All of the above methods support analytic forces. 



## Method details and customisation


#### Tkatchenko−Scheffler schemes
A density-dependent, atom pairwise dispersion-correction scheme

**`TS`**:<a name="TS"></a>     
[Phys. Rev. Lett.,102, 073005 (2009)](https://doi.org/10.1103/PhysRevLett.102.073005)

Restrictions: 
* Can only be used with the following XC functionals:
* The following elements are supported: 

Available from CASTEP v???

**`TSSURF`**:<a name="TSSURF"></a>    
 [Phys. Rev. Lett., 108, 146103 (2012)](https://doi.org/10.1103/PhysRevLett.108.146103)


??? keyword "Customisation keywords for TS schemes"
    `SEDC_SR_TS`    
      Type: `R:E`    
      Description:
            Customisable SR value for the damping function in the TS
            semi-empirical dispersion/van der Waals correction scheme. 
      Modifiable: restart and on the fly 
      Default is determined by `XC_FUNCTIONAL`.

    `SEDC_D_TS`    
      Type: `R:E`    
      Description:
            Customisable d value for the damping function in the TS
            semi-empirical dispersion/van der Waals correction scheme. 
      Modifiable: restart and on the fly 
      Default is determined by `XC_FUNCTIONAL`.







#### Many-body dispersion
**`(A)MBD`**:<a name="MBD"></a> 
[Phys. Rev. Lett., 108, 236402 (2012)](https://doi.org/10.1103/PhysRevLett.108.236402)    

**`(A)TSSCS`**: TS with self-consistent screening<a name="TSSCS"></a>    
[Phys. Rev. Lett., 108, 236402 (2012)](https://doi.org/10.1103/PhysRevLett.108.236402)    

**`(A)MBD*`**<a name="MBD*"></a>     
[J. Chem. Phys. 140, 18A508 (2014)](https://aip.scitation.org/doi/10.1063/1.4865104)    







#### Grimme 'D' corrections
**`G06`** (This is CASTEP's name for the Grimme D2 correction):<a name="G06"></a>     
[J. Comput. Chem. 27, 1787, (2006)](https://doi.org/10.1002/jcc.20495)

??? keyword "Customisation keywords G06"
      `SEDC_S6_G06`    
      Type: `R:E`    
      Description:
            Customisable S6 value for the damping function in the G06
            semi-empirical dispersion/van der Waals correction scheme. 
      Modifiable: restart and on the fly 
      Default is determined by `XC_FUNCTIONAL`.

      `SEDC_D_G06`    
      Type: `R:E`    
      Description:
            Customisable d value for the damping function in the G06
            semi-empirical dispersion/van der Waals correction scheme. 
      Modifiable: restart and on the fly 
      Default is determined by `XC_FUNCTIONAL`.



**`D3`**:<a name="D3"></a>     
[J. Chem. Phys. 132, 154104 (2010)](https://doi.org/10.1063/1.3382344)    

**`D3-BJ`**:<a name="D3-BJ"></a>    
[J. Comput. Chem. 32, 1456 (2011)](https://doi.org/10.1002/jcc.21759)

??? warning "Compilation flags: for the D3 correction, CASTEP must be compiled with `GRIMMED3 := compile`<a name="D3compilation"></a>"
      
      Note that for the D3 correction to work, CASTEP must be compiled with the following flag:
      ```
      # Grimme D3 library support. Options are none or compile
      GRIMMED3 := compile
      ```
      in the `Makefile`

      For CASTEP 20, the D3 library is included in the distribution and the setting the flag above should be sufficient. 

      For CASTEP 19, you have to download the D3 library and modify a few things:

      TODO: is this supported?
      
      1. Get the D3 source code:

         a) Go into the LibSource directory within the CASTEP main directory. 

         b) Clone branch 0.9.2 of dftd3:
         ```
         git clone --depth 1 --branch 0.9.2 https://github.com/dftbplus/dftd3-lib.git dftd3-lib-0.9.2
         ```

         c) prepend “dftd3_” to the names of the .f90 files within dftd3-lib-0.9.2/lib/
         (e.g. `mv api.f90 dftd3_api.f90`)


      2. Edit the main Makefile:
         1. set the flag to compile D3:
            ```
            # Grimme D3 library support. Options are none or compile
            GRIMMED3 := compile
            ```
      

         2. correct the path to the D3 library (later on in the `Makefile`)


      3. Recompile CASTEP


#### Other Schemes (TODO: rename)
**`OBS`** (Ortmann, Bechstedt and Schmidt)<a name="OBS"></a>    

Semiempirical van der Waals correction to the density functional description of solids and molecular structures

[Phys. Rev. B 73, 205101, (2006)](https://doi.org/10.1103/PhysRevB.73.205101)
??? keyword "Customisation keywords"
    "`SEDC_LAMBDA_OBS`"
        Type: `R:E`


        Description:
                Customisable lambda value for damping function in the the OBS
                semi-empirical dispersion/van der Waals correction scheme.     
          Modifiable: restart and on the fly    
          Default is determined by `XC_FUNCTIONAL`.

    "`SEDC_N_OBS`"
        Type: `R:E`
        Description:
              Customisable n value for the damping function in the OBS
              semi-empirical dispersion/van der Waals correction scheme.    
        Modifiable: restart and on the fly    
        Default is determined by `XC_FUNCTIONAL`.

**`JCHS`** (Jurečka, Černý, Hobza and Salahub)<a name="JCHS"></a>   

[J. Comput. Chem. 28, 555, (2007)](https://doi.org/10.1002/jcc.20570)

??? keyword "Customisation keywords"
    `SEDC_SR_JCHS`    
      Type: `R:E`    
      Description:
            Customisable SR value for the damping function in the JCHS
            semi-empirical dispersion/van der Waals correction scheme.    
      Modifiable: restart and on the fly    
      Default is determined by `XC_FUNCTIONAL`.

    `SEDC_S6_JCHS`    
      Type: `R:E`    
      Description:
            Customisable S6 value for the damping function in the JCHS
            semi-empirical dispersion/van der Waals correction scheme.    
      Modifiable: restart and on the fly    
      Default is determined by `XC_FUNCTIONAL`.

    `SEDC_D_JCHS`    
      Type: `R:E`    
      Description:
            Customisable d value for the damping function in the JCHS
            semi-empirical dispersion/van der Waals correction scheme.    
      Modifiable: restart and on the fly    
      Default is determined by `XC_FUNCTIONAL`.





**`XDM`**:<a name="XDM"></a>    
A unified density-functional treatment of dynamical, nondynamical, and dispersion correlations.

[J. Chem. Phys. 127, 124108 (2007)](https://doi.org/10.1063/1.2768530)

??? keyword "Customisation keywords for XDM"
      `SEDC_A1_XDM`    
      Type: `R:E`    
      Description:
            Customisable A1 value for the damping function in the XDM
            semi-empirical dispersion/van der Waals correction scheme.    
      Modifiable: restart and on the fly    
      Default is determined by `XC_FUNCTIONAL`.

      `SEDC_A2_XDM`    
      Type: `P:E`    
      Description:
            Customisable A2 value for the damping function in the XDM
            semi-empirical dispersion/van der Waals correction scheme.     
      Modifiable: restart and on the fly      
      Default is determined by `XC_FUNCTIONAL`.

      `SEDC_SC_XDM`    
      Type: `R:E`    
      Description:
            Customisable SC value for the damping function in the XDM
            semi-empirical dispersion/van der Waals correction scheme.    
      Modifiable: restart and on the fly    
      Default is determined by `XC_FUNCTIONAL`.

      `SEDC_C9_XDM`    
      Type: `L:B`    
      Description:
            Specifies whether three-body dispersion coefficients are 
            to be computed in the XDM semi-empirical dispersion/ 
            van der Waals correction scheme.    
      Modifiable: restart and on the fly    
      Allowed values: `TRUE` or `FALSE`    
      Default is `FALSE`






