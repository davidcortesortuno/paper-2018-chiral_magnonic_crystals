# Chiral Magnonics: Micromagnetic Simulations

This repository has all the necessary tools to reproduce the micromagnetic
simulations from the publication: **Chiral Magnonic Crystals: Breaking the Spin
Wave Symmetry with a Periodic Dzyaloshinskii-Moriya Interaction**

The system under study is a 3000 nm long and 200 nm wide Permalloy stripe with
a periodic DMI, which can be obtained by patterning periodic arrays of heavy
metal wires on top of the sample.

The periodicity depends on two factors: the lattice parameter `a` and the HM width `w` ...

For example, the system for `w=50` looks like:

![](images/simulation_system_a100nm_w50nm.png)

## Damping

The theory is based on infinitely long and wide stripes. In the simulation
we use a finite width of 200 nm which we set with an exponentially growing
damping towards the width

![](images/exponential_damping_along_width.png)

# Docker

The simulations can be run automatically with
