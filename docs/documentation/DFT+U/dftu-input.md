

## .cell file
A $U$ value can be specified in the .cell file as follows:
```
%BLOCK hubbard_u
Ni d : 6 eV
Er f : 5 eV
%ENDBLOCK hubbard_u
```
This will apply a $6$ eV Hubbard $U$ potential to the d states of all Ni atoms in the system. Similarly a $5$ eV potential for all Er atoms. The units can also be specified as follows:
```
%BLOCK hubbard_u
eV
Ni d : 6
Er f : 5
%ENDBLOCK hubbard_u
```

When omitted, the default units are eV.
