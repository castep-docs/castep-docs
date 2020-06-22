In addition to Chris' OTFG document, some more description of the
OTF string

    2|3.1|4.0|2.2|2|3|5|50U3.4:60U3.1:51:52U3.1{6s1.45,5d0.05}(qc=3)[]

Quantities in <> are descriptions not literals.  All chars outside <>
are literal

    <Local cpt>|<r_c(loc)>|<r_c(nonloc)>|<rinner/rcore>|<COARSE>|<MEDIUM>|<FINE>|
    <proj1>:<proj2>...<projn>{<config>}(flags)[<test config>]

    Local cpt     :  0,1,2 for s,p,d
    r_c(loc)      :  pseudisation radius for local component (atomic units)
    r_c(nl)       :  pseudisation radius for nonlocal components (atomic units)
                 (can be overridden as part of projector description)
    rinner/rcore  :  Pseudisation radius for augmentation functions and pseudo-core charge
    COARSE/MEDIUM/FINE : Recommended cutoff energies in atomic units (Hartree)
    projn         : Descriptions of projectors to include, separated by semicolons.

   Syntax of a projector is in its briefest form

     <n><l>     	  where digits <n> and <l> denote the atomic quantum numbers eg 30 for 3s
              	  In fact this is equivalent to the expanded form "<n><l>UU" where the
              	  projector flags "UU" mean include two ultrasoft beta projectors for
              	  this channel.

     The full form is    
        <n><l>[<type>[<r_c>]][+/-<dE_use>][@<shift>] 
     where anything in brackets  [] is optional (here only).

         <type> can be
        U        - a single ultrasoft projector
        UU       - Two ultrasoft projectors
        N        - a single norm-conserving projector
        L        - use this projector as the local component
	    G        - an ultrasoft GIPAW Gamma projector
        H        - an norm-conserving GIPAW Gamma projector 
        P        - Dummy: do not make a projector.
        LG       - Make Gammas for local channel (not done by default)

        <r_c>    - the projector specific pseudisation radius.
        <dE_use> - the reference energy for the projector. A floating-point
                    value beginning with an explicit '=', '+' or '-' in Hartree.
                    '=E' means absolute energy, '+/-E' is relative to AE eigenvalue.
       <shift>  - Add this value to the projector, it shift it in energy. 

         config        : Reference configuration used to generate pseudopotential
                specified in obvious way, eg {3s1,3d0.5}. It is not necessary to
                explicitly mention all core states - CASTEP figures this out.
         flags         : Options controlling the type of pseudisation applied and parameters.
                Syntax (flag1,flag2,   ) allows multiple, comma separated flags

       qc=<val>     The optmisation parameter - KE for q < qc is minimised in optimised
                projector scheme.  Can also write (qc=3,qc1=3.5) to specify
                angular momentum channel-specific value of qc.
     tm           Troullier-Martins pseudosation scheme
     pn           polynomial fit
     pb           bessel fit
     es           "extra soft" scheme
     esr=val      extra-soft with explicit specification of r_c
     nonlcc       Do not generate of unscreen with a pseudo-core charge.
     schro        Use non-relativistic schroedinger equation for AE calculation
                 (default is scalar relativistic eqn)
     aug          Explicitly turn on augmentation charges
     scpsp        Generate a self-consistent pseudopotential

    test config   : Specify a non-default test configuration eg, [4s1.5,3d0.5].
