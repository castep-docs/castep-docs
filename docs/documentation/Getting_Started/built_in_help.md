CASTEP has an in-built help option to assist with using particular keywords. Information on using CASTEP can be seen by using:
```sh
castep -h
```

To get more information on a particular input file keyword (e.g. `kpoint_mp_grid`) use:

```sh
castep -h kpoint_mp_grid
```

If you don't know the keyword you need to use, then you can search on a particular keyword. This returns a list of keywords that you might be interested in, e.g. to look at all keywords which contain a reference to symmetry.

```sh
castep -s symmetry
```
Finally, to list all keywords, use:
```sh
castep -h all
```

To find out which version of CASTEP you have, use:
```sh
castep -v
```
