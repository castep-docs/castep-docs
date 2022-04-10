There are many (many!) XC functionals (of varying quality and
applicability). LIBXC (https://www.tddft.org/programs/libxc/) is a
maintained library of functionals that is upgraded regularly. The list
of functionals available in LIBXC is at
https://www.tddft.org/programs/libxc/functionals/.

Castep interfaces to this library which can be used instead of
Castep's in-built library of XC functionals. Prepend the string LIBXC_
to Castep's functional name in the parameter keyword `xc_functional`
to use LIBXC. For example:  
`xc_functional : PBE` for Castep's in-built PBE functional  
`xc_functional : LIBXC_PBE` for the LIBXC version of the PBE functional  

In the LIBXC library there are many functionals, covering LDAs, GGAs,
Meta-GGAs, Hybrids, etc. Most of these are separated into exchange and
correlation contributions. To use these functionals, build your own
combination using Castep's `xc_definition` keyword in the .param
file. Firstly at https://www.tddft.org/programs/libxc/functionals/
find the exchange and correlation functionals that you require, note
the name LIBXC calls is and then prepend the string LIBXC_ to them.

For example to construct Perdew and Zunger's LDA, LDA exchange is
called LDA_X and correlation is called LDA_C_PZ.
In the .param file use
```
%block xc_definition
LIBXC_LDA_X 1.0
LIBXC_LDA_C_PZ 1.0
%endblock xc_definition
```
The "1.0" after each is the fraction of how much of each you require
to use, in this case 100% of each.

Example, construct the PBE functional from LIBXC: In LIBXC, PBE
exchange is called GGA_X_PBE and its correlation is called
GGA_C_PBE. Prepend with LIBXC_ and construct `xc_definition`:
```
%block xc_definition
LIBXC_GGA_X_PBE 1.0
LIBXC_GGA_C_PBE 1.0
%endblock xc_definition
```

There are a few functional in LIBXC that have combined exchange and
correlation parts, so this can be listed in `xc_definition` on its
own. For example the HCTH93 XC functional is called GGA_XC_HCTH_93 in
LIBXC hence it can be used in Castep with
```
%block xc_definition
LIBXC_GGA_XC_HCTH_93 1.0
%endblock xc_definition
```
LIBXC can also be used to construct hybrid (non-local) functionals
that contain (screened) Hartree-Fock components. Note that LIBXC does
not contain the non-local part of such functionals, just the local
part. Construct the functional using Castep's non-local
functionality. For example, the PBE0 functional is called
HYB_GGA_XC_PBE0 in LIBXC, so to construct this use
```
%block xc_definition
LIBXC_HYB_GGA_XC_PBE0 1.0
HF 0.25
%endblock xc_definition
```

Note here you need to know (ie. read the HYB_GGA_XC_PBE0 reference
given in https://www.tddft.org/programs/libxc/functionals/) what
fraction of local exchange is in the functional and so
infer what the fraction of non-local exchange is required (here 0.25).

If you want to vary the fraction of non-local exchange then you need to
balance this with offsetting it with the correct fraction of local
exchange. For this construct the whole functional yourself. For
example PBE0 is 0.25HF + 0.75PBE_X + 1.0PBE_C. Varying the HF
component in PBE0 can be done with
```
%block xc_definition
HF 0.20
LIBXC_GGA_PBE_X 0.80
LIBXC_GGA_PBE_C_1.0
%endblock xc_definition
```
where here it's set to 20% non-local and 80% local exchange, with 100%
PBE correlation.

Meta-GGAs are also supported. For example the RSCAN functional can be
used with
```
%block xc_definition
LIBXC_MGGA_X_RSCAN 1.0
LIBXC_MGGA_C_RSCAN 1.0
%endblock xc_definition
```
(although RSCAN is also natively supported in Castep with `xc_functional : RSCAN`).

The `xc_definition` keyword in the .param file will allow you to mix
and match any of the hundreds of functionals in LIBXC
https://www.tddft.org/programs/libxc/functionals/. DO SO WITH EXTREME CAUTION!
