
CASTEP contains in built internal profiling in the `trace` module.  This can be switched on using any of the following `devel_code` options.

``` yaml
# Prints a complete list of function calls to the profile file.
%block devel_code
TRACE
%endblock devel_code
```

``` yaml
# Prints profiling information for the whole run - i.e. how long is spent in each subroutine.
%block devel_code
PROF: * :ENDPROF
%endblock devel_code
```

``` yaml
# Profiling for a subset of routines only
%block devel_code
PROF: <part_of_subroutine_name> :ENDPROF
%endblock devel_code
# e.g. PROF:wave:ENDPROF profiles all routines which contain "wave" in their name.\\
```

If any of these `devel_codes` are present, a CASTEP run writes a table of calls to each subroutine in (something similar to) the following format:

```
+------------------------------------------------------------
| o-- list of parent routines 
|  /
| O->name of subroutine   
|  /
| --o-> list of child routines 
+------------------------------------------------------------
```

The list of parent routines has information on the number of calls this parent routine calls this current routine.  

The subroutine of interest has information on how many times in total it was called.

The list of child routines has a list of how many times a particular child routine was called from the subroutine of interest.

If profiling is on, for all or some of the routines, there is an additional column for number of times the routine was profiled and a total time spent in each routine.

`devel_code : PROFCLASS:FFT ORTHOGONALISATION:ENDPROFCLASS` will prints a table of the total time spent in routines labelled with a particular class.  The class of a routine is assigned in the `trace_entry` call by the class optional argument.

e.g.
```
Class of operation                  Time spent
FFT                                     1.41s
ORTHOGONALISATION                       0.05s
```

!!! note 
        For `PROF:<stuff>:ENDPROF` and `PROFCLASS:<stuff>:ENDPROFCLASS` there must be no whitespace in the `devel_code` before or after the colon (:) character, i.e `PROF:wave:ENDPROF` and not `PROF: wave :ENDPROF`


