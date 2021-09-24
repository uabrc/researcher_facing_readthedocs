Basic Volume Setup
==================

These instructions are intended for users who want to setup a persistent volume for use across instances. To follow these instructions you'll need to have already setup an :ref:`instance<instance_setup_basic>`.

Creating a Volume
-----------------

1. Click the "Volumes" fold-out in the left-hand navigation pane - the fold-out should open.

   .. figure:: ./images/volumes_000.png
      :alt: Image showing the OpenStack Overview page. The Volumes fold-out is opened. The Volumes link in the fold-out is highlighted.

2. Click "Volumes" within the fold-out to open the "Volumes" table page.

   .. figure:: ./images/volumes_001.png
      :alt: Image showing the Volumes page. The Volumes table is empty.

3. Click "+ Create Volume" to open a dialog box.

4. Fill out the dialog box.

   a. Enter a "Volume Name".
   b. Enter a "Description".
   c. Select "No source, empty volume" in the "Volume Source" drop-down box to create an empty volume.
   d. Select "__DEFAULT__" in the "Type" drop down box.
   e. Select a size in GB appropriate for your needs.
   f. Select "nova" in the "Availability Zone" drop down box.
   g. Select "No group" in the "Group" drop down box.

   .. figure:: ./images/volumes_002.png
      :alt: Image showing the Create Volume dialog. The dialog is filled out. The volume name is set to my_volume.

5. Click "Create Volume"

   a. Returns to the "Volumes" table page.
   b. There will be a new entry in the "Volumes" table.

   .. figure:: ./images/volumes_003.png
      :alt: Image showing the Volumes page. The table has one entry labeled my_volume.


Attaching a Volume to a Running Instance
----------------------------------------

To attach a volume you must have already created at least one using the OpenStack interface. More information can be found in [link]

1. Open the instances table by clicking "Compute" in the left-hand navigation pane and clicking "Instances".

2. In the "Actions" column entry, click the drop down triangle button and select "Attach Volume".

   .. figure:: ./images/instances_018.png
      :alt: Image showing the OpenStack Instances Page. The table has one entry labeled my_instance. The drop-down box under the Actions column is open revealing many options. The Attach Volume option is highlighted.

3. A dialog box will open.

4. Select a volume in the "Volume ID" drop down box.

   .. figure:: ./images/instances_019.png
      :alt: Image showing the Attach Volume dialog box. The Volume ID is set to my_volume.

5. Click "Attach Volume".

Now the volume should be attached to the instance. From here you may format the volume and mount it.


Formatting a Volume
-------------------

To format a volume, you must have created a volume and attached it to an instance capable of formatting it correctly. These instructions assume a Linux operating system.

1. Click "Compute" in the left-hand navigation pane, then open the "Instances" menu. Click the name of any instance you wish to use to format the volume. Then click "Overview".

2. Scroll down to "Volumes Attached" and make note of the :code:`<mount>` part of :code:`<volume-name> on <mount>` for your attached volume as it will be used in later steps.

   .. figure:: ./images/persistent_volumes_000.png
      :alt: Image showing the my_instance overview page. The page has been scrolled to the bottom. The mouse is pointing to a label under the Volumes Attached heading. The mouse is pointing to the Attached To label reading my_volume on /dev/vdb.

3. SSH into the instance from your local machine or from Cheaha.

4. Verify the volume is attached by using :bash:`sudo fdisk -l | egrep "<mount>""`

   .. figure:: ./images/persistent_volumes_001.png
      :alt: Image showing the MINGW64 terminal on Windows. The last three lines show the sudo fdisk -l command entered. The result includes the disk label /dev/vdb.

5. Format the volume using :bash:`sudo fdisk "<mount>"`

   a. You will be in the :code:`fdisk` utility.
   b. Enter :code:`n` to create a new partition.
   c. Enter :code:`p` to make it the primary partition.
   d. Enter numeral :code:`1` to make it the first partition.
   e. Press enter to accept the default first sector.
   f. Press enter to accept the default last sector.
   g. Enter :code:`t` to change partition type.
   h. Enter numerals :code:`83` to change to Linux partition type.
   i. Enter :code:`p` to display the partition setup. Note that the partition will be labeled :code:`<mount>1`. This literally whatever :code:`<mount>` was from earlier followed by the numeral :code:`1`. Further steps will refer to this as :code:`<pmount>`
   j. Enter :code:`w` to execute the setup prepared in the previous substeps.

   .. figure:: ./images/persistent_volumes_002.png
      :alt: Image showing the MINGW64 terminal. The sudo fdisk /dev/vdb command has been entered. Also shown are the various prompts guiding through the process of formatting the disk. The final command was the literal character w, which executed the previously entered commands.

6. Verify the volume is not mounted using :bash:`sudo mount | egrep "<mount>"`. If there is no output, then move to the next step. If there is some output then use :bash:`sudo umount -l "<mount>"` to unmount the volume and verify again.

   .. figure:: ./images/persistent_volumes_003.png
      :alt: Image showing the MINGW64 terminal. The volume has been verified to be not mounted using the sudo mount | egrep /dev/vdb command.

7. Create the filesystem using :bash:`sudo mkfs.ext4 "<pmount>"`. Ensure that the output looks like the following:

   .. code-block::

      ubuntu@my-instance:~$ sudo mkfs.ext4 /dev/vdb1
      mke2fs 1.45.5 (07-Jan-2020)
      Discarding device blocks: done
      Creating filesystem with 26214144 4k blocks and 6553600 inodes
      Filesystem UUID: 335704a9-2435-440a-aeea-8ae29438ac64
      Superblock backups stored on blocks:
            32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
            4096000, 7962624, 11239424, 20480000, 23887872

      Allocating group tables: done
      Writing inode tables: done
      Creating journal (131072 blocks): done
      Writing superblocks and filesystem accounting information: done

   .. figure:: ./images/persistent_volumes_004.png
      :alt: Image showing the MINGW64 terminal. The sudo mkfs.ext4 /dev/vdb1 command has been used to create a partition labeled /dev/vdb1 on mount /dev/vdb.

The volume is now formatted and ready for mounting within an attached instance OS. You will need to make note of :code:`<pmount>` for when you are ready to mount the volume to an instance.


Mounting a Volume in an Instance
--------------------------------

Mounting a volume needs to be done once per instance it will be attached to. It is assumed you've already created and formatted a volume and attached it to some instance. You'll need the :code:`<pmount>` label from when you formatted the volume.

1. SSH into the instance from your local machine or from Cheaha.

2. Obtain the uuid of the volume using :bash:`sudo blkid | egrep "<pmount>"`. This will be referred to as :code:`<uuid>` in future steps.

   .. figure:: ./images/persistent_volumes_005.png
      :alt: Image showing the MINGW64 terminal on Windows. The sudo blkid | egrep "vdb1" command has been used to find the partition UUID.

3. Create a directory to mount the volume as. A good choice is :bash:`sudo mkdir /mnt/<volume-name>` where :code:`<volume-name>` is something meaningful for you or your project. This directory will be referred to as :code:`<directory>` in future steps.

4. Mount the volume to the directory using :bash:`sudo mount -U <uuid> <directory>`.

5. Verify the volume is mounted using :bash:`df -h | egrep <pmount>`

   .. figure:: ./images/persistent_volumes_006.png
      :alt: Image showing the MINGW64 terminal. The command mkdir /mnt/my-volume has been used to create a mount point. The command sudo mount -U <UUID> /mnt/my-volume has been used to mount the volume to the mount point. The command df -h | egrep "vdb1" has been used to verify mounting.

6. Edit the :code:`fstab` file to make mounting persistent across instance reboots.

   a. Edit the file using :bash:`sudo nano /etc/fstab`.
   b. Add the following line to the file:

   .. code-block:: bash

      /dev/disk/by-uuid/<uuid> <directory> auto defaults,nofail 0 3

   .. figure:: ./images/persistent_volumes_007.png
      :alt: Image showing the MINGW64 terminal. The nano editor is open and the file /etc/fstab is being edited with sudo privileges to allow saving. The suggested line has been added to the file.

7. Verify `fstab` was modified correctly by soft rebooting the instance and verifying the mount again using :shell:`df -h | egrep "<pmount>"`.

   .. figure:: ./images/persistent_volumes_008.png
      :alt: Image showing the MINGW64 terminal. The instance has been rebooted prior to this. The command df -h | egrep "vdb1" has been used to verify the partition was mounted on restart.

8. Set access control using the following commands:

   .. code-block:: bash

      sudo apt install acl # or yum install, etc., if not already installed
      sudo setfacl -R -m u:<username>:rwx <directory>

   .. figure:: ./images/persistent_volumes_009.png
      :alt: Image showing the MINGW64 terminal. The acl package has been installed using the command sudo apt install acl. The access controls have been set on the mount point /mnt/my-volume using the sudo setfacl command.

9. Verify the access controls were modified correctly by creating a test file and then listing files in :code:`<directory>` to ensure the file was created. The following commands will achieve this:

   .. code-block:: bash

      cd <directory>
      touch testfile
      ls

   .. figure:: ./images/persistent_volumes_010.png
      :alt: Image showing the MINGW64 terminal. Access control settings have been verified by creating an empty file in the mount point /mnt/my-volume and listing files.

The volume is now mounted to your instance and ready for use and re-use across sessions and reboots.