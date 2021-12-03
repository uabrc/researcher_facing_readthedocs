Detailed Hardware Information
=============================


Cheaha High Performance Computing (HPC) Hardware
------------------------------------------------

Node Summary
~~~~~~~~~~~~

The current HPC cluster is comprised of 8192 compute cores connected by
low-latency Fourteen Data Rate (FDR) and Enhanced Data Rate (EDR) InfiniBand
networks. In addition to the basic compute cores, there are also 72 NVIDIA Tesla
P100 GPUs available. 

A description of the different hardware generations are summarized in the following table:

- Gen10: (planned Sep 2021) 34 nodes with 2x64 core (4352 cores totals) 2.0 GHz AMD Epyc 7713 Milan each with 512GB RAM.
- Gen9: 52 nodes with EDR InfiniBand interconnect: 2x24 core (2496 cores total) 3.0GHz Intel Xeon Gold 6248R compute nodes each with 192GB RAM.
- Gen8: 35 2x12 core (840 cores total) 2.60GHz Intel Xeon Gold 6126 compute nodes with 21 compute nodes at 192GB RAM, 10 nodes at 768GB RAM and 4 nodes at 1.5TB of RAM
- Gen7: 18 2x14 core (504 cores total) 2.4GHz Intel Xeon E5-2680 v4 compute nodes with 256GB RAM, four NVIDIA Tesla P100 16GB GPUs, and EDR InfiniBand interconnect (supported by UAB, 2017). 

.. csv-table::
   :file: data/hardware_short_df.csv
   :header-rows: 1

TFLOPS
~~~~~~

The table below is a theoretical analysis based on processor instructions and core counts, and is not a reflection of efficiency in practice.

.. csv-table::
   :file: data/tflops_df.csv
   :header-rows: 1
