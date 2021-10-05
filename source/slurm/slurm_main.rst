SLURM
================

All work on Cheaha must be submitted to the queueing system, Slurm. This doc
gives a basic overview of Slurm and how to use it. 

Slurm is software that gives users fair allocation of the cluster's resources.
It schedules jobs based using resource requests such as number of CPUs, maximum
memory (RAM) required per CPU, maximum run time, and many more.

The main Slurm documentation can be found at `the Slurm site
<https://slurm.schedmd.com/>`__. The `Slurm Quickstart
<https://slurm.schedmd.com/quickstart.html>`__ can also be helpful for orienting
users new to queueing systems on the cluster.

The basic workflow for non-interactive jobs follows:

1. Stage data to ``$USER_DATA``, ``$USER_SCRATCH``, or a project directory.
2. Research how to run your directives in 'batch' mode. In other words, how to
   run your analysis pipeline from the command line, with no GUIs or user input.
3. Identify the appropriate resources necessary to run the jobs (CPUs, time,
   memory, etc)
4. Write a job script specifying these parameters using Slurm directives.
5. Submit the job (``sbatch``)
6. Monitor the job (``squeue``)
7. Review the results, and modify/rerun if necessary (``sacct`` and ``seff``)
8. Remove data from ``$USER_SCRATCH``

Common Slurm Parlance
---------------------

- Node: A subdivision of the cluster that contains multiple cores.
  - Login nodes: Controls user access to Cheaha. Low count and shared among all
  users. DO NOT RUN JOBS ON THE LOGIN NODE
  - Compute nodes: Dedicated nodes for running user jobs.
- Core: A single CPU
- Partition: A job queue to submit your job to. Different partitions have
  different resource limits and priority.
- Batch jobs: Scripts to submit to the SLURM scheduler. Should run with no user
  input or graphical user interface (GUI)


Slurm Directives
----------------

Slurm has many directives a researcher can use when creating a job, but there
are a couple that are imperative:

1. ``--ntasks``: The number of nodes a job needs
2. ``--cpus-per-node``: The number of cores to request on each node
3. ``--partition``: The partition to submit the job to. Partition details can be
   seen below
4. ``--time``: Amount of time the job is estimated to run for. Acceptable time
   formats include "minutes", "minutes:seconds", "hours:minutes:seconds",
   "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds"
5. ``--mem-per-cpu``: Amount of RAM (in MB) needed per CPU. Can specify 4 GB
   with either 4000 or 4G
6. ``-o``: Path to a file storing the text output of the job commands.

Slurm Partitions
----------------

.. list-table:: Available Slurm Partitions
   :widths: 25 25 25 25
   :header-rows: 1

   * - Partition
     - Max Runtime
     - Max Compute Nodes
     - Priority
   * - express
     - 2 hours 
     - No limit
     - 2
   * - short
     - 12 hours
     - 44
     - 4
   * - medium
     - 2 days 2 hours 
     - 44
     - 6
   * - largemem
     - 2 days 2 hours 
     - 10
     - 6
   * - long
     - 6 days 6 hours
     - 5
     - 8
   * - pascalnodes
     - 12 hours 
     - No limit 
     - 8
   * - interactive 
     - 2 hours
     - 1
     - 10

Notes:

- Express jobs are highest priority in scheduling meaning they will be scheduled
  faster
- Most partitions have a max amount of requestable memory per node at 256 GB.
  Largemem has a maximum memory limit of 1.5 TB.
- Each user has a maximum amount of requestable resources across all jobs.
  Submitted jobs beyond this resource limit will be kept in the queue until
  a user's prior jobs have completed.