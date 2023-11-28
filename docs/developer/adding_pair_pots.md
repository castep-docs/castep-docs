# Adding Empirical potentials

If you have access to the source, it is possible to add a new formulation for an
empirical potential easily. The idea of the module is that this should be
trivial even to a beginner programmer with no expert knowledge of Fortran.

A summary of how to do this is in the header of the `pair_pot.f90` source,
a more in-depth description is below.

## Setting up parameters

First we need to make the `pair_pot_type` aware of your potential. There are
several key things we need to update in order to use our potential. First, we
need to update the number of potentials our code is looking for:

```fortran
BEFORE:
integer, parameter :: num_pot = 9
```

```fortran
AFTER:
integer, parameter :: num_pot = 10
```

Next we need to tell the code what our potential's keyword is and its
internal ID. This will be the highest number which isn't occupied.
(NOTE: Keywords have to have a length of 4 characters and must be padded
with spaces to this length):

```fortran
BEFORE:
integer :: lj=1,buck=2,coul=3,dz=4,pol=5,bb=6,bs=7,sw=8,mors=9
character(len=4), dimension(num_pot) :: name = &
    & ['LJ  ','BUCK','COUL','DZ  ','POL ','BB  ','BS  ','SW  ','MORS']
```

```fortran
AFTER:
integer :: lj=1,buck=2,coul=3,dz=4,pol=5,bb=6,bs=7,sw=8,mors=9,new=10
character(len=4), dimension(num_pot) :: name = &
    & ['LJ  ','BUCK','COUL','DZ  ','POL ','BB  ','BS  ','SW  ','MORS','NEW ']
```

We then need to add the parameters that our potential will use to the
`pair_pot_type`. The style of these parameters should be:

-   The variable name should be the keyword of your potential followed by an
    underscore, followed by the name or symbol for the parameter.

-   They should be of type `real(kind=dp)`.

-   They should be allocatable, and of dimensions equivalent to the number of
    particles involved in the interaction (i.e. 2-body $\Rightarrow{}$
    `dimension(:,:)`; 3-body $\Rightarrow{}$ `dimension(:,:,:)`).

-   They should have a comment describing the full name and form of your
    potential.

-   It is also important to note that Fortran is case-insensitive, meaning it
    does not distinguish between upper and lower cases in variable names.

    ```fortran
    !New example potential of the form b*exp(rij^-qi)*exp(rik^-qi) + (cos(rijk) - cos(s))
    real(kind=dp), dimension(:), allocatable :: new_q
    real(kind=dp), dimension(:,:), allocatable :: new_b
    real(kind=dp), dimension(:,:,:), allocatable :: new_s
    ```

We should now go into `pair_pot_print` and add our potential to the 1- and 2-
(and possibly 3-)body sections of the potential printing. This is of the form:

-   1-Body

    ```fortran
    if (pair_pot%pot_present(pair_pot%new)) then
       write(unit_out, 103) pre_str, 'r', pair_pot%cut_off(pair_pot%new, 1, 1), 'NEW'
       write(unit_out, 103) pre_str, 'q', pair_pot%new_q(1, 1), 'NEW'
    end if
    ```

-   2-Body

    ```fortran
    if (pair_pot%pot_present(pair_pot%new)) then
       write(unit_out, 202) pre_str, 'r', pair_pot_print_combinations(pair_pot%cut_off(pair_pot%new, :, :), ispec, jspec), 'NEW'
       write(unit_out, 202) pre_str, 'b', pair_pot_print_combinations(pair_pot%new_b, ispec, jspec), 'NEW'
    end if
    ```

-   3-Body

    ```fortran
    if (pair_pot%pot_present(pair_pot%new)) then
       write(unit_out, 301) pre_str, ispec_name, jspec_name, kspec_name
       write(unit_out, 103) pre_str, 'S', pair_pot%new_s(ispec, jspec, kspec), 'NEW'
    end if
    ```

And with that we should be done with setting up our potential in
`pair_pot_type`, things like cut-off and the activation of the potential are
handled automatically based on the potential keyword, although for some
specialised potentials advanced rules can be necessary.

## Allocation and deallocation

It is important in Fortran to ensure that our parameter arrays are allocated. We
need to go into the routine `pair_pot_allocate` and add our new parameters to
it. For our example potential, the syntax is as follows:

```fortran
if (pair_pot%pot_present(pair_pot%new)
   allocate(pair_pot%new_q(1:nspec),stat=ierr)
   if (ierr .ne. 0) call io_allocate_abort('new_q','pair_pot_allocate')
   allocate(pair_pot%new_b(1:nspec,1:nspec),stat=ierr)
   if (ierr .ne. 0) call io_allocate_abort('new_b','pair_pot_allocate')
   allocate(pair_pot%new_s(1:nspec,1:nspec,1:nspec),stat=ierr)
   if (ierr .ne. 0) call io_allocate_abort('new_s','pair_pot_allocate')
end if
```

We also need to do the same for cleaning up our potential at the end, in the
routine `pair_pot_deallocate`:

```fortran
if (allocated(pair_pot%new_q)) then
   deallocate(pair_pot%new_q, stat=ierr)
   if (ierr.ne.0) call io_abort('Error deallocating new_q in pair_pot_deallocate')
end if
if (allocated(pair_pot%new_b)) then
   deallocate(pair_pot%new_b, stat=ierr)
   if (ierr.ne.0) call io_abort('Error deallocating new_b in pair_pot_deallocate')
end if
if (allocated(pair_pot%new_s)) then
   deallocate(pair_pot%new_s, stat=ierr)
   if (ierr.ne.0) call io_abort('Error deallocating new_s in pair_pot_deallocate')
end if
```

## Initialising variables

We need to be able to set the values for our parameters. For this we need to add
an initialisation subroutine. The details can be found in the sample file,
available on request. For three-body routines it is necessary to set the
`pair_pot%three_body` flag on initialisation, and also to add a species triplet
loop.

## Writing the calculation routine

This is the only bit which is down to the the creator to consider how it
should be set up. The subroutine should obey the follow:

-   The name of the routine should be `pair_pot_<new_potential>`

-   The potential should have a header referencing the origin of the
    potential and the form of the potential.

-   Two-body potentials should obey the following input structure:

    ```fortran
    subroutine pair_pot_new(pair_pot, rij, mod_rij_2, ispec, jspec[, spins], dfij, de)
    ```

    Where:

    -   `pair_pot` is of type `pair_pot_type` and contains the initialised
        parameters of your new potential.

    -   `rij` is of type `real(kind=dp)` of dimension(3) and is the vector
        between the two particles.

    -   `mod_rij_2` is of type `real(kind=dp)` and is the distance between the
        two particles.

    -   `ispec` is of type `integer` and is the species of atom i.

    -   `jspec` is of type `integer` and is the species of atom j.

    -   `spins` [optional] is of type `real(kind=dp)` of dimension(4,2) and is
        the pair of spin vectors of (x, y, z, magnitude)

    -   `dfij` is of type `real(kind=dp)` of dimension(3) and is the vector
        force between the two particles.

    -   `de` is of type `real(kind=dp)` and is the contribution to the total
        potential energy of the two particles.

-   To reference two-body terms you should use the following syntax:

    ```fortran
    pair_pot%new_b(ispec,jspec)
    ```

-   Three-body potentials should obey the following input structure:

    ```fortran
    subroutine pair_pot_new(pair_pot, dr, mod_dr_2, rcjk, include_cjk, spec[, spins], dfij, de, stress)
    ```

    Where:

    -   `pair_pot` is of type `pair_pot_type` and contains the
        initialised parameters of your new potential.

    -   `dr` is of type `real(kind=dp)` of dimension(3,3) and is the
        vectors of the triplet of pairs of particles.

    -   `mod_dr_2` is of type `real(kind=dp)` of dimension(3) and is the
        distance between the triplet of particles.

    -   `rcjk` is of type `real(kind=dp)` of dimension(3,3) and is the
        absolute positions of the particles in the cell.

    -   `include_cjk` is of type `logical` of dimension(3) and is
        whether the magnitude of distances between particles is less
        than that of the cut-off.

    -   `spec` is of type `integer` of dimension(3) and is the species
        of the particles.

    -   `spins` [optional] is of type `real(kind=dp)` of dimension(4,3) and is
        the triplet of spin vectors of (x, y, z, magnitude)

    -   `dfij` is of type `real(kind=dp)` of dimension(3,3) and is the
        vector force between the triplet of particles.

    -   `de` is of type `real(kind=dp)` and is the contribution to the total
        potential energy of the interactions.

    -   `stress` is of type `real(kind=dp)` of dimension(6) and is the upper
        triangle of stress contributions of the particles.

-   To reference three-body terms you should use the following syntax:

    ```fortran
    pair_pot%new_s(spec(i_atom), spec(j_atom), spec(k_atom))
    ```

### Spins

If your potential uses spin as part of the force-field these are passed into the
calculation routines as a set of 4-vectors (2 for 2-body, 3 for 3-body) where
the 4 parameters are the 3 directions and the magnitude.

## Adding the contribution

To actually tell the code to calculate the contribution of your potential to the
system, we need to add it to the `pair_pot_contribution` routine, this has the
following syntax for two-body potentials:

```fortran
if (pot_include(pair_pot%new)) then
   call pair_pot_new(pair_pot, rij, mod_rij_2, species(1), species(2), dfij, de)
   e_cont = e_cont + de
   fij(:) = fij(:) + dfij(:)
end if
```

Three-body potentials are currently trickier and must currently be manually
inserted into the loop in `pair_pot_calc`, there are aims to simplify this in
future releases.

## Testing

We should now be able to activate your potential by adding `NEW=T` into the
devel code block and can set all the parameters just as for other potentials.

To verify that you potential is working as expected, there are several built-in
methods to check for developers.

1. The first is the `FD_CHECK` devel code which enables finite difference
   evaluation alongside the potential evaluation and dumps the output to a file
   `<seedname>.fd`. It aso prints warnings if the analytic and finite difference
   derivatives do not match. You should verify that the finite difference
   evaluated forces are the same as the analytic derivative.

2. The second is the `PRINT_POT` devel code which evaluates your potential over
   1000 evenly spaced points between 0 and your cut-off and dumps the computed
   forces and energies to a series of files of the form
   `<seedname>_<species_1>_<species_2>_<species_3>_<spin>.pot` these are just
   3-column tabular data of the form `Distance Energy Force` ready to be
   plotted.

3. Tests should be added to the test suite to compute the value of your new
   potential at known points.
