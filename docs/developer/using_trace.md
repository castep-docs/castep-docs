# Using the `trace` module

The `trace` module provides functionality useful to developers for debugging and
profiling particular sections of castep. It is common practice to put calls to
`trace_entry` and `trace_exit` at the beginning and end of function calls in
castep, but the reasoning why may be unclear.

The primary reason for most users is that when castep performs an `io_abort`, it
first calls into `trace` on each process to dump the current trace stack to the
`<seedname>.<process_id>.err` files. This is the main error message people see
when castep fails.

This document sets out to explain in more detail, the usage of the `trace`
module and how and why it benefits developers.


## The `trace` module

### Tracing code

#### Trace Blocks

The `trace` module provides a number of functions which are helpful in debugging
and profiling code. The key functions in `trace` for general usage are
`trace_entry` and `trace_exit` which should be used in all major functions. This
makes it so the subprogram is logged in tracing.

!!! note
    The `trace_entry` and `trace_exit` routines do have an associated
    cost, and therefore for short routines called very frequently (e.g. functions
    in loops) it can be a bad idea for performance to trace these routines.

The syntax for `trace_entry` is:

```fortran
call trace_entry(block_name, success[, profile][, class])
```
Where:

- `block_name` - `character, intent(in)` - is the name of the entry in the
  trace.
- `success` - `integer, intent(out)` - is the return status of the function, `0` if
  successful.
- `profile` - `logical, intent(in)` - whether to profile this block
- `class` - `character, intent(in)` - is the profile class for the purposes of
  [`profclass`](#profclass-block) enabling profiling.

The syntax for `trace_exit` is:
```fortran
call trace_exit(block_name, success)
```

Where:

- `block_name` - `character, intent(in)` - is the name of the entry in the
  trace.
- `success` - `integer, intent(out)` - is the return status of the function, `0` if
  successful.

!!! note
    `trace_entry` and `trace_exit` subroutines can be called around any
    arbitrary blocks of code. This makes it possible to narrow down failing
    points, but not only that, they can be used to profile sections of code
    where performance is falling below expectations.

#### Trace Sections

It is possible to mark a section of a code as a sub-element of a trace-block
rather than a block in its own right. These can also have extra arguments passed
through to log parameters at certain stages.

The syntax for `trace_section` is:

```fortran
call trace_section_entry(section_name[, variable_name, value], success[, class])
```
Where:

- `section_name` - `character, intent(in)` - is the name of the entry in the
  trace.
- `variable_name` - `character, intent(in)` - is the logging name to be attached
  to the section in the trace output
- `value` - `integer|character, intent(in)` - is the current value of the
  variable to be logged. `value` can either be an `integer` or
  `character(len=63)`
- `success` - `integer, intent(out)` - is the return status of the function, `0` if
  successful.
- `class` - `character, intent(in)` - is the profile class for the purposes of
  `profclass` enabling profiling.

The syntax for `trace_exit` is:

```fortran
call trace_section_exit(block_name, success)
```

Where:

- `block_name` - `character, intent(in)` - is the name of the entry in the
  trace.
- `success` - `integer, intent(out)` - is the return status of the function, `0` if
  successful.

### Debugging

The trace stack is built up from the `trace_entry` and `trace_exit` routines
which keep track of where the code is currently executing. This is why it is
recommended that all major routines (where possible, see note above) begin and
end with a `trace_entry`, `trace_exit`.

Tracing can also be used to dump information to a [logging file](#logging-files)
whenever a `trace_entry`/`trace_exit` call is hit. This is done using:

```fortran
call trace_set_debug(.true.)
```

It is then possible to check within a module whether trace debugging is on using:

```fortran
if (trace_debug_is_on()) then
   ...
end if
```

### Profiling

Trace also provides profiling functionality timing the duration between any
`entry` & `exit`. Timing can be enabled through setting the relevant `prof` or
`profclass` devel codes to true ([see: below](#devel-codes)).

It is also possible to enable profiling globally using:

```fortran
class trace_set_profile(.true.)
```

And subsequently disable it in a similar way:

```fortran
class trace_set_profile(.false.)
```

The `trace` module tracks a number of useful profiling factors including time
spent in function, call counts, and time per call.


#### Devel Codes

The `trace` module has several functions which can be enabled by devel codes.

##### Global

- `FULL_TRACE` - `logical` - Enable full profiling for all modules including the
  `trace` module itself.
- `TRACE` - `logical` - Enable automated dumping of function calls to the
  profiling filed

##### PROF block

Enables timing for the castep.

```
# Prints profiling information for the whole run
# i.e. how long is spent in each subroutine.
%block devel_code
PROF: * :ENDPROF
%endblock devel_code
```

##### PROFCLASS Block

List of "classes" to be matched against trace classes (see: [`trace_entry`](#tracing-code)), to
enable profiling for certain groups of operations.

```
%block devel_code
PROFCLASS:FFT ORTHOGONALISATION:ENDPROFCLASS
%endblock devel_code
```

will print a table of the total time spent in routines labelled with a
particular class.

This will produce an output like:
```
Class of operation                  Time spent
FFT                                     1.41s
ORTHOGONALISATION                       0.05s
```

!!! note
    For `PROF:<stuff>:ENDPROF` and `PROFCLASS:<stuff>:ENDPROFCLASS` there
    must be no whitespace in the `devel_code` before or after the colon (:)
    character, i.e `PROF:wave:ENDPROF` and not `PROF: wave :ENDPROF`

### Dumping info

It is possible to dump the info in the tracing at any time. In order to get all
information including timings, calls, etc. you can call `trace_output` as
follows:

```fortran
call trace_output(out_unit, success, order)
```

Where:

- `out_unit` - `integer, intent(in)` - Fortran file unit to write to
- `success` - `integer, intent(out)` - is the return status of the function, `0` if
  successful.
- `order` - `character, intent(in)` - Order in which to dump trace, must be one of:

    - `L` - Order they were (first) added to trace.
    - `T` - Descending order of total time spent in function.
    - `C` - Descending order of number of calls.
    - `P` - Descenging order of time per call.

It is also possible to quickly dump the current trace call stack. This is done
as follows:

```fortran
call trace_log_output(out_unit, success)
```

Where:

- `out_unit` - `integer, intent(in)` - Fortran file unit to write to
- `success` - `integer, intent(out)` - is the return status of the function, `0` if
  successful.

#### Output format

If any of the `TRACE`, `FULL_TRACE` or `PROF` `devel_codes` are present, or a
call is made to `trace_output`, CASTEP writes a table of calls to each
subroutine in (something similar to) the following format:

```
+------------------------------------------------------------
| o-- list of parent routines
|  /
| O->name of subroutine
|  /
| --o-> list of child routines
+------------------------------------------------------------
```

The list of parent routines has information on the number of calls this parent
routine calls this current routine.

The subroutine of interest has information on how many times in total it was
called.

The list of child routines has a list of how many times a particular child
routine was called from the subroutine of interest.

If profiling is on, for all or some of the routines, there is an additional
column for number of times the routine was profiled and a total time spent in
each routine.

#### Logging Files

By default, CASTEP creates `<seedname>.<process_id>.profile` files to log trace
information.
