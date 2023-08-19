# README #

* Ambit - A FEniCS-based cardiovascular physics solver

3D nonlinear solid and fluid mechanics finite element Python code using FEniCS and PETSc libraries, supporting

* Solid mechanics
  - Finite strain elastodynamics, implementing a range of hyperelastic isotropic and anisotropic as well as viscous constitutive laws
  - Active stress for modeling of cardiac contraction mechanics
  - Quasi-static, generalized-alpha, or one-step theta time integration
  - Nearly incompressible as well as fully incompressible formulations (latter using pressure dofs)
  - Prestressing using MULF method in displacement formulation
  - Volumetric growth & remodeling
* Fluid dynamics
  - Incompressible Navier-Stokes/Stokes equations, either in nonconservative or conservative formulation
  - Navier-Stokes/Stokes flow in an Arbitrary Lagrangian Eulerian (ALE) reference frame
  - One-step theta, or generalized-alpha time integration
  - SUPG/PSPG stabilization for equal-order approximations of velocity and pressure
* Lumped (0D) models
  - Systemic and pulmonary circulation flow models
  - 2-element as well as 4-element Windkessel models
  - Signalling network model
* Coupling of different physics:
  - Monolithic coupling of ALE and fluid, 3D solid/fluid/ALE-fluid with lumped 0D flow models
  - Multiscale-in-time analysis of growth & remodeling (staggered solution of 3D-0D coupled solid-flow0d and G&R solid problem)
* Fluid-reduced-solid interaction (FrSI)
  - Boundary subspace-projected physics-reduced solid model (incl. hyperelastic, viscous, and active parts) in an ALE fluid reference frame
* POD-based model order reduction (MOR)
  - Projection-based model order reduction applicable to main fluid or solid field (also in a coupled problem), by either projecting
    the full problem or a boundary to a lower dimensional subspace spanned by POD modes

- author: Dr.-Ing. Marc Hirschvogel, marc.hirschvogel@deepambit.com

Still experimental / to-do:

- Fluid-solid interaction (FSI) (started)
- Finite strain plasticity
- Electrophysiology/scalar transport
- ... whatever might be wanted in some future ...


### How do I get set up? ###

* Clone the repo:

``git clone https://github.com/marchirschvogel/ambit.git``

* Either, FEniCS-x from a Docker container can be used, or it can be installed from source (see https://github.com/FEniCS/dolfinx if needed)

* Assuming Docker is installed (if not, see e.g. https://docs.docker.com/engine/security/rootless), get latest tested Ambit-compatible digest (19 Aug 2023) of dolfinx Docker image:

``docker pull dolfinx/dolfinx@sha256:1f374e90d5e918a71a4bdba994bf434cdaf84fedc47aa11ac33295864180fb76``

* Put the following shortcut in .bashrc (replacing <PATH_TO_AMBIT_FOLDER> with the path to the ambit folder):

``alias fenicsdocker='docker run -ti -v $HOME:/home/shared -v <PATH_TO_AMBIT_FOLDER>:/home/shared/ambit -w /home/shared/ --env-file <PATH_TO_AMBIT_FOLDER>/.env.list --rm dolfinx/dolfinx@sha256:1f374e90d5e918a71a4bdba994bf434cdaf84fedc47aa11ac33295864180fb76'``

* If 0D models should be used, it seems that we have to install sympy (not part of docker container anymore) - in the folder where you pulled ambit to, do:

``cd ambit && mkdir modules/ext && pip3 install --target=ext mpmath --no-deps --no-cache-dir && pip3 install --target=ext sympy --no-deps --no-cache-dir && cd ..``

* Launch the container in a konsole/terminal window by simply typing

``fenicsdocker``

* Have a look at example input files in ambit/testing and the file ambit_template.py in the main folder as example of all available input options

* Best, check if all testcases run and pass, by navigating to ambit/testing and executing

``./runtests.py``

* Build your input file and run it with the command

``mpiexec -n <NUMBER_OF_CORES> python3 your_file.py``
