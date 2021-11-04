OpenStack (cloud.rc)
====================

Our OpenStack portal `cloud.rc <https://dashboard.cloud.rc.uab.edu>`__ provides a home for more permanent research applications such as web pages and database hosting. In contrast with our High Performance Computing (HPC) environment Cheaha, where all jobs must have a time limit, instances on cloud.rc are allowed to exist indefinitely. Resource quotas are set to ensure that every user has a fair share. Currently, access to cloud.rc must be made while on campus, or on the campus Virtual Private Network (VPN). For more information about using the VPN, please visit `VPN - UAB IT <https://www.uab.edu/it/home/tech-solutions/network/vpn>`__.

To get started using cloud.rc, please navigate to `<https://dashboard.cloud.rc.uab.edu/>`__. For a first time setup, it is highly recommended to visit the pages below in order. Network setup is a create-once, use-many set of instructions which provides a foundation for instances, volumes, and other features. Instances provide homes for services and are connected to the outside world, and each other, via the network. Volumes provide storage which can be moved among instances or held for future use.

.. toctree::
  :maxdepth: 2

  network_setup_basic
  instance_setup_basic
  volume_setup_basic
