Basic Network Setup
===================

Networking setup should be a one-time setup. Security Groups can and should be
added as needed. While Floating IPs fall under the Networking fold-out, they
should be allocated and released together with instances to maximize security.

Creating a Network
------------------

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ../img/networks_000.png

2. Click "Networks" in the fold-out menu.

   a. The "Networks" page will open.
   b. The "uab_campus" network entry should already be in the table.

   .. figure:: ../img/networks_001.png

3. Click "+ Create Network" to open a dialog box.
4. Fill out the dialog box. Only the "Network" tab is important, we will create a subnet as a separate step.

   a. Enter a "Network Name".
   b. Leave "Enable Admin State" checked.
   c. Uncheck "Create Subnet". We will do this as a separate step. The other tabs should be removed.
   d. Leave the "Availability Zone Hints" box empty.

   .. figure:: ../img/networks_003.png

5. Click "Create".

   a. Redirects to the "Networks" page.
   b. There should be a new entry in the table with the name given in (4.a)

   .. figure:: ../img/networks_004.png

Creating a Subnet
-----------------

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ../img/networks_000.png

2. Click "Networks" in the fold-out menu.

   a. The "Networks" page will open.
   b. The "uab_campus" network should already be an entry in the table.
   c. At least one other entry must be in the table. See :ref:`Creating a Network`.

   .. figure:: ../img/networks_004.png

3. Under the "Actions" column, select the drop-down triangle button in the row corresponding to the network you want to add a subnet to.

   .. figure:: ../img/subnet_002.png

4. Click "Create Subnet" in the drop-down to open a dialog box.
5. Fill out the dialog box.

   a. The "Subnet" tab.

      i. Enter a "Subnet Name".
      ii. Enter :code:`192.168.0.0/24` as the "Network Address". The trailing :code:`/24` allocates the entire range from :code:`192.168.0.0` through :code:`192.168.0.255` to the subnet.
      iii. Ensure "IPv4" is selected in the "IP Version" drop-down box.
      iv. Leave "Gateway IP" empty to use the default value of :code:`192.168.0.0`.
      v. Leave "Disable Gateway" unchecked.
      vi. Click the "Next >>" button to move to the "Subnet Details" tab.

      .. figure:: ../img/subnet_003.png

   b. The "Subnet Details" tab.

      i. Leave "Enable DHCP" checked.
      ii. Enter :code:`192.168.0.20,192.168.0.100` in the "Allocation Pools" box. The IP addresses in that range will be assigned to instances on this subnet.
      iii. Leave "DNS Name Servers" empty.
      iv. Leave "Host Routes" empty.

      .. figure:: ../img/subnet_004.png

6. Click "Create".

   a. Redirects to the "Overview" page for the network the subnet was added to.

   .. figure:: ../img/subnet_005.png

   b. Click the "Subnets" tab next to "Overview" to verify the subnet was added to the table for this network.

   .. figure:: ../img/subnet_006.png

Creating a Router
-----------------

To follow these directions for creating a router, a :ref:`network<Creating a Network>` and :ref:`subnet<Creating a Subnet>` must already exist.

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ../img/networks_000.png

2. Click "Routers" in the fold-out menu.

   .. figure:: ../img/routers_001.png

3. Click "+ Create Router" to open a dialog box.
4. Fill out the dialog box.

   a. Enter a "Router Name".
   b. Leave "Enable Admin State" checked.
   c. Select "uab-campus" in the "External Network" drop down box.
   d. Leave the "Availability Zone Hints" box empty.

   .. figure:: ../img/routers_002.png

5. Click "Create Router".

   a. Redirects to the "Routers" page.
   b. There should be a new entry in the table with the name given in (4.a)

   .. figure:: ../img/routers_003.png

6. Now we need to connect the router to our subnet. Click the name of the new entry under the "Name" column to open the router "Overview" page.

   .. figure:: ../img/routers_004.png

7. Click the "Interfaces" tab.

   .. figure:: ../img/routers_005.png

8. Click "+ Add Interface" to open a dialog box.
9. Fill out the dialog box.

   a. Select an existing network-subnet pair in the "Subnet" drop down box.
   b. If this is your only router on the selected subnet, leave "IP Address" empty to use the subnet gateway.

   .. figure:: ../img/routers_006.png

10. Click "Submit"

    a. Redirects to the "Interfaces" page for the router.
    b. There should be a new entry in the table.

    .. figure:: ../img/routers_007.png

Creating a Security Group
-------------------------

These instructions show you how to prepare to use SSH with your instances. Security Groups are used to set rules for how external devices can connect to our instances. Here we will create an SSH Security Group using a method that can be applied to other types of connections. The method used can be applied to other types of Security Groups as well.

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ../img/networks_000.png

2. Click "Security Groups" in the fold out menu.

   .. figure:: ../img/security_groups_001.png

3. Click "+ Create Security Group" to open a dialog box.
4. Fill out the dialog box.

   a. Under "Name" enter :code:`ssh`.
   b. Leave "Description" empty.

   .. figure:: ../img/security_groups_002.png

5. Click "Create Security Group".

   a. Redirects to the "Manage Security Group Rules: ssh" page.
   b. There should be an entry for "Egress IPv4" and "Egress IPv6". Leave these alone.

   .. figure:: ../img/security_groups_003.png

6. Click "+ Add Rule" to open a dialog box.

   a. Select "SSH" in the "Rule" drop down box. This will change the remaining fields.
   b. Leave "Description" empty.
   c. Select "CIDR" in the "Remote" drop down box.
   d. Type :code:`0.0.0.0/0` in the "CIDR" box. **WARNING!** This is **NOT** good practice! For your research instances, you'll want to constrain the CIDR value further to a narrower range of IP addresses. The rule we have shown here leaves the SSH port open to all IP addresses world-wide.

   .. figure:: ../img/security_groups_004.png

7. Click "Add".

   a. Redirects to the "Manage Security Group Rules: ssh" page.
   b. There should be a new entry in the table.

   .. figure:: ../img/security_groups_005.png