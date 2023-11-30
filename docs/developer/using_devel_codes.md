# Using Devel Codes

This document is intended to describe the use of devel codes for
developers to speed up implementation of experimental parameters.

## What are devel codes

Devel codes are handy tools for developers to control features while
they are not ready for public release. Devel codes are read from the
`devel_code` block of the `.param` file.

Devel codes are much simpler to use than keywords, however they do not
have the rigorous type/value checking or unit conversion that keywords
do. Nor are they searchable and do not provide any help. In order to
use devel codes you have to explicitly know how to call them, the
values they should take and what they do.

The devel code block is an arbitrary string which can be used to
provide parameters to a function, however, the devel code block also
has several useful standard structural elements to make it more useful
than just a string one has to parse themselves.

## Using devel codes

### Devel code sub-blocks

Devel codes are divided into sub-blocks which are usually named related to the
module or functions they support.

Examples include:

- `MD` - Relating to molecular dynamics options
- `FIRE` - Relating to the FIRE geometry optimisation method
- `ELECTRONIC` - Relating to electronic minimisation

However they can be anything the developer wants.

!!! note

    While in principle block names are general and arbitrary,
    keeping them related to the module where they are used or their
    functionality is useful for remembering how to call them.

Another use of blocks is to have a block dedicated to a particular algorithm
or as a structured block in the style of `.cell` style blocks (i.e.
`%block ... %endblock`) ready for integration into the main parameters when
the feature is complete.

The structure of a sub-block in the `.param` file (here `XYZ`) is as follows:

```
%block devel_code
XYZ: param=3 :ENDXYZ
%endblock devel_code
```

### Extracting devel codes

The devel code block is converted upon reading the param file into
`parameters :: current_params%devel_code`. This block can then be
parsed using the following functions:

- `io :: io_code_present(code, key, block)`

    Check whether a particular parameter `key` is present in block
    `block`. If block is not given check the top-level devel-code.

- `io :: io_code_block(code, block)`

    Return the entire block `block` as a character array allowing you
    to manually process the data. Most useful for situations where the
    final parameter will be a block of data.

- `io :: io_code_logical(code, key, block)`

    Parse given parameter  `key` in block `block` as a logical
    according to list-directed Fortran logical rules.

- `io :: io_code_integer(code, key, block)`

    Parse given parameter `key` in block `block` as an integer according
    to list-directed Fortran integer rules.

- `io :: io_code_real(code, key, block)`

    Parse given parameter `key` in block `block` as an real according
    to list-directed Fortran real rules.

- `io :: io_code_complex(code, key, block)`

    Parse given parameter `key` in block `block` as an complex according
    to list-directed Fortran complex rules.

- `io :: io_code_string(code, key, block)`

    Parse given parameter `key` in block `block` as a character string.

### Example

For a `devel_code` block that looks like:

```
%block devel_code
mod_param=17
XYZ: param=3 :ENDXYZ
%endblock devel_code
```

The usual procedure for processing a devel code argument is as follows:

```fortran
module my_module
   ...
   ! Can read into module parameters if necessary
   integer :: module_param
   ...

   function use_devel_code()
      ! Ensure the devel_codes are available
      use parameters, only: current_params
      ! Ensure we can parse the devel-codes
      use io, only: io_code_present, io_code_integer
      ! Have the param available
      integer :: param


      ! Check that we're the master process for reading the strings
      if (on_root_node) then
         ! Check if the devel code has been set
         if (io_code_present(current_params%devel_code,'param','XYZ')) &
            ! Read and parse the parameter for use
            & param = io_code_integer(current_params%devel_code,'param','XYZ')

         !Since it's top-level we parse it without passing the block.
         if (io_code_present(current_params%devel_code,'mod_param')) &
            & module_param = io_code_integer(current_params%devel_code,'mod_param')

      endif

      ! Distribute the parameters to all nodes
      call comms_gcopy(param, 1)
      ...

```
