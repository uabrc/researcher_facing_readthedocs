.. Main UAB RC documentation for anything relating to Cheaha and the new UAB
   Cloud system.

Welcome to UAB Research Computing Docs!
============================================

.. add short blurb about research computing here

UAB Research Computing (RC) is a group of IT and data scientists dedicated
technical support for researchers at UAB, specifically related to cloud and
cluster computing. The main resources run by UAB RC are the `Cheaha cluster
computing platform <rc.uab.edu>`__ and UAB Cloud (coming soon!). Both of these
resources are freely available to use by any researcher or instructor at UAB. 



.. MKD: currently thinking we place and edit all TOC in index, but hide them
   from rendering on the actual page. They'll appear on the sidebar. Then we
   keep things on the mainpage to a minimum, like the CGDS docs, Only including
   quickstart information. Modelled after https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html

Cheaha Quickstart
-----------------

Account Registration
^^^^^^^^^^^^^^^^^^^^

:doc:`user_registration/uab_user`
   Self-register your account using UAB credentials.

:doc:`user_registration/xias_guest`
   Access Cheaha as an non-UAB researcher using XIAS. Only available after a UAB
   employee :ref:`grants access <user_registration/xias_users>`


Using Cheaha
^^^^^^^^^^^^

:doc:`open_ondemand/ood_main`
   How to use Cheaha through the online web portal



.. Hidden ToC
.. Account Registration

.. toctree::
   :maxdepth: 2
   :hidden:

   /user_registration/index


.. Using Cheaha

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Using Cheaha

   /slurm/index
   /open_ondemand/index


.. UAB Cloud

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: UAB Cloud

   openstack/network_setup_basic
   openstack/volume_setup_basic

.. Resources

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Resources

   resources/globus.rst
   python.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


