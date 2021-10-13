Python
======

Python is a high level programming language that is widely used in many branches
of science. The scientific python ecosystem is available to researchers as
Anaconda modules on Cheaha. Both python 2 and python 3 are installed. In order
to see the different versions of each, use:

.. code-block::

    module spider Anaconda

Libraries and Virtual Environments
---------------------------------

Anaconda includes a few very common libraries such as scikit-learn, pandas,
numpy, and scipy by default. However, most projects will need some external
libraries as well using ``pip`` or ``conda install``. In order to install
external libraries, users will need to create a virtual environment or use one
of the defaults.

Python virtual environments are self-contained environments containing necessary
packages for specific projects. It is recommended to have a separate environment
for each project you have. This solves cases where different projects have
dependencies on different versions of the same package. 

In order to create a basic environment with the default packages, use the
``conda create`` command:

.. code-block:: bash

    # create an environment named test
    conda create -n test

If 