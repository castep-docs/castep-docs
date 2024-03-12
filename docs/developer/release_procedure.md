# CASTEP new release procedure

## Initial setup

- [ ] Open an issue containing this checklist
- [ ] Open bug fix/release branch
- [ ] Cherry pick appropriate bug-fixes from `default`
- [ ] Update version number in `license.F90`
- [ ] Ensure BIOVIA release is tagged

## Functionality

- [ ] Check OTFG features exposed in `cell`
- [ ] Check CI
  - [ ] Create dedicated pipeline for release branch on ANVIL
  - [ ] Run full build tests on Make and CMake
  - [ ] Check `make dist` works -- Including unpacking and building from dist only!
  - [ ] Check that `cmake -t dist` also compiles and includes everything

- [ ] Ensure checkpoints forward & backward compatible
- [ ] Ensure compatibility between Academic and BIOVIA releases

- [ ] Check CASTEP builds and runs on ARCHER2 -- Both GNU and CMake
- [ ] Check GPU build on Tier-1 machines -- Both GNU and CMake

- [ ] Check supported compilers for oldest and latest and update README.install
      appropriately

## External Libraries

- [ ] Check linked/included library versions for updates
  - Current libraries:
    - [ ] dl_mg
    - [ ] simple-dftd3
    - [ ] d4
    - [ ] spglib
    - [ ] libxc
    - [ ] FoxXML

## External Tools

- [ ] Checked shipped versions of third-party tools and utilities for updates
  - Current tools:
    - [ ] c2x
    - [ ] cif2cell
    - [ ] optados
    - [ ] BoltzTrap
    - [ ] SHengBTE
    - [ ] emc
    - [ ] atat
    - [ ] elastic_constants
- [ ] Update emacs_mode keys for most recent keywords

- [ ] Check that version requirement of Python components and utilities are
      still up to date

## Documentation

- [ ] Check and update README.install docs
- [ ] Update release notes
- [ ] Update version in Ford Docs

- [ ] Check new parameters (cell and param keywords)
  - [ ] New parameters have correct help text
  - [ ] New parameters are documented in the manual


## Licences

- [ ] Update checksums file
- [ ] Upload appropriately to licences.stfc.ac.uk

## Finalisation

- [ ] Tag final release commit
- [ ] Pre-notify HPC providers of release
- [ ] Notify mailing list of release
- [ ] Update castep.org with latest info
- [ ] Check release branch for build system and documentation updates
      and back-port to default branch if needed
