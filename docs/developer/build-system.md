# The CASTEP Build Sytem

## Introduction
This documentation is intended for developers who intend to add new features/sources to the CASTEP system. A quick-start
guide on how to build CASTEP can be found in the `CASTEP_ROOT` in `README.INSTALL` for the GNU Make build-system or
`README.cmake` for the new CMake build system.

The CASTEP build system is designed to be efficient, but also intuitive. There are two existing build systems, one
relying on GNU Make, which is faster to build and intended for rapid development, and one based on CMake which is
designed to be more intuitive to those who are used to CMake build systems and for automatically detecting the best
options for the average user.

### CASTEP directory structure

When adding new sources to CASTEP it is important to consider the hierarchical directory/module structure of CASTEP.
CASTEP sources are currently organised into sub-libraries which each depend on the library above them in the hierarchy.

These libraries, in order of hierarchy are:

- `Utility`
- `Fundamental`
- `OTFG`
- `Dispersion`
- `Functional`

There are also `Tools` which are separately built programs which depend on the CASTEP sub-libraries.

### GNU Make

The [GNU make](https://www.gnu.org/software/make/) build system is broken down into a hierarchical tree which build up the required rules for compiling CASTEP on as
many varied systems as possible while still being isolated and maintable.

The hierarchy of these make files is as follows:

```
├ `<CASTEP_ROOT>/`
└─┬─ `Makefile` - Root Makefile
  ├─ `obj/`
  └──┬─ `include_rules.mk`
     ├─ `include_utility.mk`
     ├─ `include_fundamental.mk`
     ├─ `include_otfg.mk`
     ├─ `include_dispersion.mk`
     ├─ `include_functional.mk`
     ├─ `include_test.mk`
     ├─ `include_tools.mk`
     ├─ `platforms/`
     └──── Various make rules for different platforms
```

### CMake

The [CMake](https://cmake.org/) system is designed to be intuitive for those who are used to CMake build systems while still being familiar to
those who are used to the CASTEP GNU Make style syntax. This means that many of the CASTEP CMake variables have names
which are chosen to match, or are aliased to, the CASTEP GNU Make variables. This is intended to minimise confusion for
people who transition from GNU Make to CMake.

The CMake system is also intended to expand the capabilities of CASTEP to be able to compile and run efficiently on
Windows systems.

## Adding New Source Files

In order to add new sources to CASTEP, first it is necessary to work out the relevant dependencies and where they fit
into the directory structure (i.e. the CASTEP sub-libraries).

### Adding to GNU Make build-system
Following this the source should be added to the relevant `obj/include_<sub_library>.mk` `SRCS_$(D)`. This will
automatically include your new source in the CASTEP sub-library.

### Adding to the CMake build-system
The next step is to navigate into the sub-library folder which contains your new source and add the source file into the
`CMakeLists.txt` therein.

## Conditional inclusion
If your source file provides functions which should only conditionally be included in CASTEP (e.g. interfaces to
external libraries), then it must provide stub functions (generally `no-op`s returning relevant arguments) in order that
the conditional inclusions can be compiled. These are generally saved as `source_name.stub.f90` and these must be
conditionally included into the compilation.

### Adding to GNU Make build-system
First off, it is important to add a conditional into the relevant `obj/include_<sub_library>.mk` to include either your
stub or your main source into the compilation.

`obj/include_<sub_library>.mk`
```
ifeq (${MY_LIBRARY_VAR},none)
SRCS_$(d) := $(SRCS_$(d)) source_name.stub.f90
else
SRCS_$(d) := $(SRCS_$(d)) source_name.f90
endif
```

If extra libraries are needed to be conditionally linked these should be added as follows:
`obj/include_rules.mk`
```
ifneq (${MY_LIBRARY_VAR},none)
  ifneq ($(strip $(MY_LIB_REL_LIB_DIR)), )
    CASTEP_LIB_SEARCH_PATH += -L"../$(MY_LIB_REL_LIB_DIR)"
  ifdef SUN
    CASTEP_LIB_SEARCH_PATH += -R "$(abspath ../$(MY_LIB_REL_LIB_DIR))"
  else ifdef NAG
    CASTEP_LIB_SEARCH_PATH += -Wl,-Wl,,-rpath="$(abspath ../$(MY_LIB_REL_LIB_DIR))"
  else ifdef LINUX
    CASTEP_LIB_SEARCH_PATH += -Wl,-rpath="$(abspath ../$(MY_LIB_REL_LIB_DIR))"
  endif
  LIBS += -lmy_extra_lib
endif

```

### Adding to CMake build-system
The process with the CMake is similar, create a variable which selects either your source or stub based on an option.

e.g.
`CASTEP_ROOT/CMakeLists.txt`
```
option(WITH_MY_LIB "my lib's features")
```

`cmake/extralibs.cmake`
```
if(WITH_MY_LIB)
    set(MY_LIB_MOD source_name.f90)
else()
    set(MY_LIB_MOD source_name.stub.f90)
endif()
```

`SOURCE_DIR/CMakeLists.txt`
```
add_castep_lib(NAME sub_lib
   SRCS
   ...
   ${MY_LIB_MOD}
   ...
   )
```

If extra libraries are needed to be conditionally linked these should be added as follows:
`cmake/extralibs.cmake`
```
if(WITH_MY_LIB)
  find_library(my_extra_lib NAMES my_extra_lib
               HINTS ${EXTERNAL_MY_LIB}
               DOC "Doc")

  if (NOT my_extra_lib)
    message(FATAL_ERROR "MY_EXTRA_LIB requested, but not found.
Set EXTERNAL_MY_LIB to manually specify location of libraries (currently: '${EXTERNAL_MY_LIB}')")
  endif()

  set(MY_EXTRA_LIB ${my_extra_lib})
  set(MY_LIB_MOD source_name.f90)
else()
  set(MY_EXTRA_LIB "")
  set(MY_LIB_MOD source_name.stub.f90)
endif()

...

mark_as_advanced(... my_extra_lib)
```

`SOURCE_DIR/CMakeLists.txt`
```
target_link_libraries(sub-lib ... ${MY_EXTRA_LIB})
```

## Special Compilation Options
If you need to add special per-file compilation options, first you should check that your code is properly standards
conforming. Failing that, it is possible to override options by setting them up in each platform, however, this is
discouraged unless absolutely necessary.

### Adding to GNU Make build-system
In the GNU make system it is necessary to add the special compilation flags to each relevant platform under the
`obj/platforms` directory. e.g.

`obj/platforms/<platform>.mk`
```
<source_file>.o: private OPT = -O2
```

### Adding to CMake build-system
In the CMake build system, flags are set up in the `cmake/buildflags_<platform>.cmake` files. To override flags, the
`set_special_flags` function has been defined, which override flags for a particular build optimisation.

```
set_special_flags(OPT FAST FILES <source_file>.f90 FLAGS -O2)
```
