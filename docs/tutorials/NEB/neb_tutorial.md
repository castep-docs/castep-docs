# Nudged elastic band tutorial


## Overview and background

The nudged elastic band (NEB) approach is a widely-used method for finding a minimum energy pathway between two configurations of atoms. 
You can use the method to estimate the barrier for the system to transition between the two structures. 

The technique starts with two fixed end points which are fully relaxed (local) minima: the initial and final configurations. It then connects these end points with a series of "images" via fictitious springs that "pull" the structures taught over one or more intermediate transition states. 

In this tutorial, we will use the well-known example of an ammonia molecule's [pyramidal inversion](https://en.wikipedia.org/wiki/Pyramidal_inversion#Energy_barrier)

![NH3 inversion diagram from wikipedia](https://upload.wikimedia.org/wikipedia/commons/2/2d/Nitrogen-inversion-3D-balls.png)

We will cover:

- How to set up the initial, final (and intermediate) structures
- How to actually run the NEB calculation efficiently
- How to analyse the results
- Other tips and tricks


## Files

You can find all the files needed for this tutorial here: [neb_tutorial.tar.gz](neb_tutorial.tar.gz)



## Setting up the structures

### Setting up the initial and final states
These and the local minima structures you want find the barrier between. They can be equivalent structures with e.g. a translation between them or they can be configurations with different energies (in which case your forward and reverse barriers will not be the same!). There are two crucial things to set up **before running the NEB** though:

1. The end point structures must be fully relaxed (geometry optimised) before you start the NEB.
2. The atoms must be in the correct order. A very common mistake is to use some third party tool to generate the final state from the initial state and end up with atoms that don't match the initial atom order. When CASTEP then goes to interpolate between the two structures, you end up with atoms "passing through each other", causing the calculation to blow up. Always check that the atoms connect up in the way you expect. 


The initial state is specified in the same way as the normal ionic positions in a .cell file. e.g.:

```
%BLOCK positions_frac
   H              0.500011764912384       0.634846485697942       0.443086003907125
   H              0.616593728396204       0.432553816946042       0.442828605918639
   H              0.383248448613152       0.432623959245757       0.443068863520867
   N              0.500000000000000       0.500000000000000       0.500000000000000
%ENDBLOCK positions_frac
```


The final state is specified using a similar block in the same .cell file but with `_product` appended to the name. e.g.:

```
%BLOCK positions_frac_product
   H              0.500154169007758       0.634858887961251       0.556834437330747
   H              0.616661280589956       0.432482046338754       0.556941161085851
   H              0.383366127862304       0.432719065607707       0.557277918851780
   N              0.500000000000000       0.500000000000000       0.500000000000000
%ENDBLOCK positions_frac_product
```


### Setting up the transition state guess
CASTEP will linearly interpolate between the initial and final structures you provide to generate the first guess of the minimum energy pathway.
This works well in many cases. However, if your minimum energy pathway is likely to contain e.g. a rotation of a (group of) atom(s) around a bond or something similar, then the linear path between initial and final configurations may be a bad starting guess. 

CASTEP allows you to provide **one** intermediate structure between the initial and final configurations in order to help get the NEB on the right track. You can use this to bias your results to one pathway over another, for example. To use this, simply add the position information for this intermediate configuration to the .cell file. e.g.:

```
%BLOCK POSITIONS_ABS_INTERMEDIATE
ang
N  3.500000  3.500000  3.500000
H  3.500000  4.443968  3.500000
H  4.316393  3.027626  3.500000
H  2.683149  3.028701  3.501215
%ENDBLOCK POSITIONS_ABS_INTERMEDIATE
```



### How many images do I need?

It depends... It's usually easier to start with a small number of images and increase if you need to. 

Using many (i.e. > 15) will result in slow convergence, but may lead to a more accurate minimum energy pathway. 

Using too few (i.e. < 5) might fail to find the minimum energy pathway. 

Some questions to help answer how many images you need:

- How complex is the landscape between the initial and final state? For example, if you expect more than one maximum between the end points, you probably need more images than for the single peak example we look at here.


!!! note 
      The number of images is the number of structures between the end points. The total number of structures in the path (i.e. including the end points) will therefore be the number of images + 2.


### Constraints

In many cases we can dramatically improve the efficiency of the transition state search by imposing some constraints on the ions. However, they must be used with care so as not to introduce artifacts. For example, when looking at NEB barriers for adsorbates on a surface slab, we can constrain the bottom slab layers, but probably want the top layer(s) unconstrained.

In the ammonia case, clearly we can constrain the N atom in x, y and z without affecting the physical set up. We do this by adding the ionic_constraints block:

``` 
%BLOCK IONIC_CONSTRAINTS
     1   N   1   1 0 0
     2   N   1   0 1 0
     3   N   1   0 0 1
%ENDBLOCK IONIC_CONSTRAINTS
```

to the `nh3.cell` file.



The NEB part of CASTEP should pick up on the imposed ionic constraint(s) and you'll see something like this:

```
  --- Initialising NEB constraints ---
     Fixed            3  degrees of freedom
```
 
in the `.castep` output file.


### Do I need climbing NEB?

The climbing NEB method modifies the force on the highest-energy image (usually close to the middle of the band) such that it tries to climb *up* the barrier. 
This is very useful to get accurate barrier estimates, but care must be taken when more complex pathways (i.e. with multiple maxima) are found.

In our example the path is quite straightforward and it makes sense to use the climbing image method. We therefore set:

`TSSEARCH_NEB_CLIMBING: TRUE`

in the .param file.


## Running the NEB

### Parallelisation
Because the NEB calculation essentially runs N parallel CASTEP calculations (where N is the number of images), we can make very efficient use of the high-performance computers. The way to do this is via "task farming". The idea is to first parallelise the NEB calculation over the N images evenly and only then to employ other forms of parallelisation (e.g. over k-point and bands) within each image. 

For example, if one CASTEP calculation fits on one node, and you have 7 images, then you could run on a total of 7 nodes and set the keywords:

`NUM_FARMS: 7`

in the .param file. 

In general, setting `NUM_FARMS` to the number of NEB images will lead to good performance, provided the available computing resources can be split neatly by this number.

You will notice that if you enable task farming, the seedname.castep output file will look relatively empty. Instead, the main output is split into the different task farm .castep files. The first indexed one contains the most important information (for example that's where you would grep for "Max NEB force") and will be called e.g. `seedname_farm001.castep`. 


### Is the calculation converging?
You can monitor the convergence by grepping for "Max NEB force" within the .castep output file.

Common convergence issues include:

- Not having consistent order in the initial and final structures -> non-physical initial path
- Too many (or too few) images

### Restarting

Sometimes the calculation will run out of time/number of iterations before the NEB calculation is finished. 
You will probably see a "Failed to converge" message in the .castep output in that case; always read through your output files!

If you simply re-run the calculation without changing anything, it will simply start from the beginning again -- probably not what you want!

In order restart the NEB from the last checkpointed state, you need to **explicitly** set the name of the .check file you want to continue from. In our example that would be:

```
continuation: nh3.check
```

In the .castep output you would then see this message: `Coordinates of NEB images loaded from checkpoint file`. 

!!! warning
      Unlike other parts of CASTEP, setting `continuation: default` does not seem to work for continuing/restarting NEB calculations! You must explicitly set the name of checkpoint file.




## Analysis

Once you have a converged NEB, you can use the provided Python utility: readTS to parse and analyse the NEB. 
You first need to make sure the readTS module is on your PYTHONPATH. You can do this by going to your CASTEP source directory, and in `castep/Utilities/readts` you will find a setup.py script. Running `python setup.py` should install the module to your path. You can also manually add it by: 

``` bash
export PYTHONPATH="/path/to/castep/Utilities/readts:$PYTHONPATH"
```

(changing the `/path/to/castep/` bit to wherever CASTEP is on your machine!).

You can then extract the NEB path using something like this python code:

```python
## get this by adding castep/Utilities/readts to your PYTHONPATH
from readts import TSFile 
from ase.neb import NEBTools


def get_images(tsfile):
    '''
   Function to extract the 
   final NEB images from a tsfile object

   Args: 
        tsfile (TSFile): tsfile object
   
   Returns:
        images (list): list of ASE atoms objects
   '''
    diam_tst = tsfile.blocks['TST']

    diam_i = tsfile.blocks['REA'][1][0]
    diam_f = tsfile.blocks['PRO'][1][0]
    nbeads = len(diam_tst[1])
    max_idx = diam_tst.last_index
    images = [diam_i.atoms]
    images += [diam_tst[max_idx][i].atoms for i in range(0, nbeads, 1)]
    images.append(diam_f.atoms)
    return images

def plot_band(images, filename='neb.png'):
    nt = NEBTools(images)
    energies = nt.get_barrier()
    print(f'Barrier height:      {energies[0]:16.5f} eV')
    print(f'E_final - E_initial: {energies[1]:16.5f} eV')
    nebplot = nt.plot_band()
    nebplot.savefig(filename)



if __name__ == '__main__':
    import sys
    seedname = sys.argv[1]
    path = './'
    tolerant = False
    if len(sys.argv) > 2:
        tolerant = bool(sys.argv[2])
    tsfile = TSFile(seedname, path=path, tolerant=tolerant)
    images = get_images(tsfile)
    plot_band(images)

    # we can use ASE to write out the structure 
    # in whatever format we want
    print('Image\t\t Energy (eV)')
    for i,atoms in enumerate(images):
        print(f'{i:03d}\t {atoms.get_potential_energy():16.5f} eV')
        ## this format includes the energy of the image
        atoms.write(f'image-{i:03d}.xyz') 


    ## We can also use the ASE GUI to 
    ## view the images and analyse the NEB path.
    ## Select Tools -> NEB Plot
    # from ase.visualize import view
    # view(images)
```

If we save this script as analysis.py and run it in the directory containing both the nh3.cell and nh3.ts files like this:

```bash
python analysis.py nh3
```

we will get an .xyz file for each structure in the optimised NEB path and the energy of each image. We will also get the barrier estimate and a NEB plot showing the barrier.

The ASE GUI can also be used to plot the NEB band (uncomment the last two lines in the above script and Select Tools → NEB Plot from the GUI). 


The ASE-generated plot looks like this:

![NEB Plot](../../img/neb.png)

The barrier we obtained is about 0.23 eV, which compares well with the value of 0.25 eV (24.2 kJ/mol) [from Wikipedia](https://en.wikipedia.org/wiki/Pyramidal_inversion#Energy_barrier).

We might also notice the slight difference in energy between the two end-points of the path (about 1 meV). These should be identical, so any difference can be used as a very rough guide for the amount of numerical noise in the geometry optimisations.

Using our favourite visualisation software, we can then look at how the structure evolves along the minimum energy pathway found via the NEB.

![NEB structures](../../img/nh3_neb.gif)

### Zero-point energy corrections

In many cases, particularly when lighter atoms are involved, the energy barrier estimates obtained above need to be corrected for quantum-nuclear effects. 
 
The simplest way to do this is in the harmonic approximation. You need to estimate the harmonic zero-point energy at the start, transition and final configurations.

For the particular case (ammonia) we have been looking at, it turns out to actually explain the observed transition rate between the two 'umbrella' configurations, we need to go beyond the harmonic approximation. [REF]

TODO: add instructions for harmonic ZPE corrections.
