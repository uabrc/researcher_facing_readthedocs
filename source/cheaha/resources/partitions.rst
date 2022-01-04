Slurm Partitions
----------------

.. csv-table:: Available Slurm Partitions
   :file: /source/cheaha/slurm/partition.csv
   :widths: 20 20 20 20 20
   :header-rows: 1

Notes:

- Express jobs are highest priority in scheduling meaning they will be scheduled
  faster
- Most partitions have a max amount of requestable memory per node at 175 GB.
  Largemem has a maximum memory limit of 1.5 TB.
- Pascalnodes are specifically used for access to GPUs
- Each user has a maximum amount of requestable resources across all jobs.
  Submitted jobs beyond this resource limit will be kept in the queue until
  a user's prior jobs have completed. This will appear as
  ``QOSMaxResourceLimit`` in your ``squeue`` list.
- If a script finishes executing before the requested time limit, the job will
  automatically close and resources will be released. However requesting the max
  amount of time will cause scheduler priority to decrease.