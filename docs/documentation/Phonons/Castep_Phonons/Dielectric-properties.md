
Density functional perturbation theory is not limited to atomic
displacement perturbations, and may also be used to calculate other
response properties with respect to an electric field perturbation of an
insulating system[^16]. These are the dielectric permittivity

$$\epsilon_{\alpha,\beta}^{\infty} = \delta_{\alpha,\beta} - \frac{4 \pi}{\Omega}\frac{\partial^2 E}{\partial \varepsilon_{\alpha} \partial \varepsilon_{\beta}} \;,$$

the “molecular” polarizability

$$\alpha_{\alpha,\beta}^{\infty} =  - \frac{1}{\Omega}\frac{\partial^2 E}{\partial \varepsilon_{\alpha} \partial \varepsilon_{\beta}} \;,$$

and the Born effective charges

$$Z^{*}_{\alpha,\beta} = \Omega \frac{\partial P_{\beta}}{\partial u_{\kappa,\alpha}} = \frac{\partial F_{\kappa,\alpha}}{\partial  \varepsilon_{\beta}} = 
\frac{\partial^2 E}{\partial u_{\kappa,\alpha}\partial  \varepsilon_{\beta}}$$

which play a strong role in lattice dynamics of crystals, and in
particular governs the frequency-dependent dielectric response in the
infra-red region ([Gonze and Lee 1997](Bibliography.md#ref-GonzeL97)).

An electric field response calculation is selected using the `task`
keyword in the `.param` file.

> `task : EFIELD`

which computes the optical frequency dielectric permittivity tensor and
the low frequency (ionic lattice) response to a time-varying field in
the regime of the phonon modes and the Born charges. Alternatively

> `task : PHONON+EFIELD`

performs both dielectric and phonon tasks.

The low and near-infrared frequency contributions to the permittivity
and polarizability and the Born effective charges are printed to the
`.castep` output file. An extract for the same Wurtzite BN calculation
as earlier is shown in figure [[efield-out]](Dielectric-properties.md#fig:efield-out). An
additional output file *seedname*`.efield` is also written and contains
the frequency-dependent permittivity over the entire range, with a
spacing determined by parameter `efield_freq_spacing`, and a Lorentzian
broadening governed by a fixed $Q$, `efield_oscillator_q`.

The low-frequency contribution of the phonons to the dielectric
polarizability and permittivity is only well-defined when all mode
frequencies are real and positive. In the presence of any imaginary mode
or one of zero frequency the low-frequency dielectric and polarizability
tensors are not calculated and are reported as “infinity”. By default
the three lowest frequency modes are assumed to be acoustic modes and
not included in the calculation. To support molecule-in-supercell
calculations, the parameter `efield_ignore_molec_modes` may be set to
`molecule`, which excludes the 6 lowest frequency modes from the
dielectric calculation. Allowed values are `CRYSTAL`, `MOLECULE` and
`LINEAR_MOLECULE` which ignore 3, 6 and 5 modes respectively.

In fact CASTEP usually performs an electric field response calculation
even for a `task : PHONON` calculation because the permittivity tensor
and Born charges are required to calculate the LO/TO splitting terms.
Conversely a pure `task : EFIELD` calculation also performs a
$\Gamma$-point phonon calculation which is needed to compute the ionic
contribution to the permittivity and polarizability. Consequently the
only real difference between any of the tasks `PHONON`, `EFIELD` and
`PHONON+EFIELD` lies in what is printed to the output file as the same
computations are performed in each case. Only if one or other of those
properties is specifically turned off with one of the parameters

> `phonon_calc_lo_to_splitting : FALSE`  
> `efield_calc_ion_permittivity : FALSE`

is a “pure” phonon or E-field calculation ever performed.

It is well documented that the LDA tends to overestimate dielectric
permittivities - by over 10% in the case of Si or Ge ([Levine and Allan
1989](Bibliography.md#ref-LevineA89)). It is possible to include an ad-hoc correction
term to model the missing self-energy, by applying the so-called
“scissors operator”, which consists of a rigid upshift of all conduction
band states. This was incorporated into DFPT electric field response
calculations by Gonze and Lee ([Gonze and Lee 1997](Bibliography.md#ref-GonzeL97)). The
parameters keyword

> `excited_state_scissors 1.0 eV`

is used to model the effect of a 1 eV (in this example) upshift of
conduction band states and will include the effects on dielectric
permittivity and Born charges (but not phonons). The value to use must
be determined from high-level calculations or empirically.

```
 ===============================================================================
        Optical Permittivity (f->infinity)             DC Permittivity (f=0)
        ----------------------------------             ---------------------
         4.50788     0.00000     0.00000         6.64363     0.00000     0.00000
         0.00000     4.50788     0.00000         0.00000     6.64363     0.00000
         0.00000     0.00000     4.63846         0.00000     0.00000     7.15660
 ===============================================================================
```

```
 ===============================================================================
                                    Polarisabilities (A**3)
                Optical (f->infinity)                       Static  (f=0)
                ---------------------                       -------------
         6.52844     0.00000     0.00000        10.50324     0.00000     0.00000
         0.00000     6.52844     0.00000         0.00000    10.50324     0.00000
         0.00000     0.00000     6.77146         0.00000     0.00000    11.45793
 ===============================================================================
 ===================================================
                   Born Effective Charges
                   ----------------------
   B       1         1.84636     0.00000     0.00000
                     0.00000     1.84636     0.00000
                     0.00000     0.00000     1.94523
   B       2         1.84636     0.00000     0.00000
                     0.00000     1.84636     0.00000
                     0.00000     0.00000     1.94523
   N       1        -1.85371     0.00000     0.00000
                     0.00000    -1.85371     0.00000
                     0.00000     0.00000    -1.94009
   N       2        -1.85371     0.00000     0.00000
                     0.00000    -1.85371     0.00000
                     0.00000     0.00000    -1.94009
 ===================================================
```

: **Figure 6** Extract from the `.castep` output file generated from the hexagonal BN
run of figure [[example-gamma]](Running-phonon-calculations.md#fig:example-gamma), with
`task : EFIELD`. The Born effective charges are laid out with the
columns representing the X,Y,Z electric field directions and the rows
the X,Y,Z displacement directions.     
{#fig:efield-out}

[^16]: Because the response of a metallic system to an applied field is
    the generation of a current flow, the dielectric permittivity
    diverges and the Born charges become zero. CASTEP will check that
    the system has a band gap before proceeding with an E-field response
    calculation and abort if there is none.

### Non-linear optical susceptibility {#sec:nlo}

In addition to the linear response properties calculated with task
`EFIELD` or `phonon+efield` the non-linear dielectric susceptibility may
be computed if the parameter

> `efield_calculate_nonlinear : CHI2`

is set. The calculation uses the “2n+1 theorem” extension of
DFPT ([Baroni et al. 2001](Bibliography.md#ref-BaroniDDG01); [Miwa
2011](Bibliography.md#ref-Miwa2011)) to compute the static response, $\chi^{(2)}$. The
results are reported in the `.castep` file in reduced tensor form as the
“d-matrix” ([Boyd 2003](Bibliography.md#ref-Boyd03)). See
figure [[nlo]](Dielectric-properties.md#fig:nlo).

This is not activated by default, because it is substantially more
expensive than a baseline E-field linear response calculation. (It
requires the calculation of three sets of response functions with a full
k-point set in P1 symmetry, even for crystals with higher, even cubic
symmetry.)

```
 ===========================================================================
      Nonlinear Optical Susceptibility (pm/V)
      ---------------------------------------
         1.13621    -1.13625     0.00001     0.00002    -7.73417     0.00002
         0.00002    -0.00003    -0.00008    -7.73421     0.00002    -1.13625
        -7.73417    -7.73421   -30.12197    -0.00008     0.00001     0.00002
 ===========================================================================
```

: **Figure 7** Nonlinear optical susceptibility $\chi^{(2)}$ expressed as a d-matrix
for LiNbO3.     
{#fig:nlo}

