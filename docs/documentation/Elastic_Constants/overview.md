# Elastic Constants Tensor

## What are the Elastic Constants?

The Elastic Constants are important material properties which describe how a material responds to being deformed, i.e. the strength of a material. Mathematically, the elastic constants tensor relates an applied strain tensor to the resultant stress tensor of the crystal.

$$ \sigma_{i} = C_{ij}\varepsilon_{j} $$
where $\sigma_{i}$ is the stress tensor, $\varepsilon_{j}$ is the applied strain tensor and $C_{ij}$ is the elastic constants tensor. The elastic constants tensor can also be described as the derivative of the stress tensor with respect to an applied strain tensor:

$$ C_{ij} = \frac{d\sigma_{i}}{d\varepsilon_{j}} $$

Given the stress is the first derivative of the energy with respect to an applied strain, the elastic constants are therefore the second derivative of the energy with respect to two sets of strains applied to the material.

$$ C_{ij} = \frac{d^2 E}{d\varepsilon_{i}d\varepsilon_{j}} $$

From the Elastic Constant tensor, one can calculate several other proprerties of the material, such as the Bulk, Young's and Shear moduli, or the speed of sound through the material.

## Methods of Calculating Elastic Constants with CASTEP

There are a few options for calculating elastic constants tensor using CASTEP, they are described below:

### Python Scripts

For those with the academic licence for CASTEP, python scripts are provided which allows the user to calculate the elastic constants tensor. The tool comes in two parts - first is `generate_strain.py`, this takes the results of a successful variable cell geometry optimisation and creates a set of input files to be run through CASTEP. The second part is `elastics.py`, which takes the CASTEP results and constructs the matrix of elastic constants, Young's modulus, Poisson's ratios and bulk and shear moduli. Usage information for each script can be obtained by using the `--help` option.

### Materials Studio

If using the Materials Studio interface to CASTEP there is a built in method for calculating the elastic constants. This method works in a similar way to the python scripts but the process is automated by Materials Studio. This approach also enables the calculation of other material properites which are the responses to deformation such as the PiezoElectric Constants.

### Perturbation Theory (Beta Functionality)

There is also new beta functionality in the develpoment branch of CASTEP post version 24.1 which allows the elastic constants to be computed via Density Functional Perturbation Theory (DFPT). This method should be more computationally efficicent than the other available methods and when used correctly, more accurate.
