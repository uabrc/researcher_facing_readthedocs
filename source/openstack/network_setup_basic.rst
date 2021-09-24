Basic Network Setup
===================

Networking setup should be a one-time setup. Security Groups can and should be
added as needed. While Floating IPs fall under the Networking fold-out, they
should be allocated and released together with instances to maximize security.

Creating a Network
------------------

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ./images/networks_000.png
      :alt: Image showing the OpenStack Overview page. Networks is selected in the Network Topology fold-out menu in the left-hand navigation pane.

2. Click "Networks" in the fold-out menu.

   a. The "Networks" page will open.
   b. The "uab_campus" network entry should already be in the table.

   .. figure:: ./images/networks_001.png
      :alt: Image showing the OpenStack Networks page. The Networks table has one entry. The entry is the default, persistent uab-campus network.

3. Click "+ Create Network" to open a dialog box.
4. Fill out the dialog box. Only the "Network" tab is important, we will create a subnet as a separate step.

   a. Enter a "Network Name".
   b. Leave "Enable Admin State" checked.
   c. Uncheck "Create Subnet". We will do this as a separate step. The other tabs should be removed.
   d. Leave the "Availability Zone Hints" box empty.

   .. figure:: ./images/networks_003.png
      :alt: Image showing Create Network dialog. The dialog form is empty.

5. Click "Create".

   a. Redirects to the "Networks" page.
   b. There should be a new entry in the table with the name given in (4.a)

   .. figure:: ./images/networks_004.png
      :alt: Image showing the OpenStack Networks page. There is an additional entry in the table. The new entry is my_network.

Creating a Subnet
-----------------

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ./images/networks_000.png
      :alt: Image showing the OpenStack Overview page. Networks is selected in the Network Topology fold-out menu in the left-hand navigation pane.

2. Click "Networks" in the fold-out menu.

   a. The "Networks" page will open.
   b. The "uab_campus" network should already be an entry in the table.
   c. At least one other entry must be in the table. See :ref:`Creating a Network`.

   .. figure:: ./images/networks_004.png
      :alt: Image showing the OpenStack Networks page. There are two entries in the table. One is the default, persistent uab-campus network. The other is my_network created previously.

3. Under the "Actions" column, select the drop-down triangle button in the row corresponding to the network you want to add a subnet to.

   .. figure:: ./images/subnet_002.png
      :alt: Image Showing the drop-down box under the Actions column in the my-network row of the Networks table. The drop-down box has been clicked, revealing two options. One of the options is Create Subnet.

4. Click "Create Subnet" in the drop-down to open a dialog box.
5. Fill out the dialog box.

   a. The "Subnet" tab.

      i. Enter a "Subnet Name".
      ii. Enter :code:`192.168.0.0/24` as the "Network Address". The trailing :code:`/24` allocates the entire range from :code:`192.168.0.0` through :code:`192.168.0.255` to the subnet.
      iii. Ensure "IPv4" is selected in the "IP Version" drop-down box.
      iv. Leave "Gateway IP" empty to use the default value of :code:`192.168.0.0`.
      v. Leave "Disable Gateway" unchecked.
      vi. Click the "Next >>" button to move to the "Subnet Details" tab.

      .. figure:: ./images/subnet_003.png
         :alt: Image Showing the Create Subnet dialog box. The Subnet tab is selected. The form has not been filled out beyond default values.

   b. The "Subnet Details" tab.

      i. Leave "Enable DHCP" checked.
      ii. Enter :code:`192.168.0.20,192.168.0.100` in the "Allocation Pools" box. The IP addresses in that range will be assigned to instances on this subnet.
      iii. Leave "DNS Name Servers" empty.
      iv. Leave "Host Routes" empty.

      .. figure:: ./images/subnet_004.png
         :alt: Image Showing the Create Subnet dialog box. The Subnet Details tab is selected. The form has been filled out.

6. Click "Create".

   a. Redirects to the "Overview" page for the network the subnet was added to.

   .. figure:: ./images/subnet_005.png
      :alt: Image Showing the my_network overview page. There are three tabs. The Overview tab is selected.

   b. Click the "Subnets" tab next to "Overview" to verify the subnet was added to the table for this network.

   .. figure:: ./images/subnet_006.png
      :alt: Image Showing the my_network overview page. The Subnets tab is selected. The table has one entry labeled my_subnet.

Creating a Router
-----------------

To follow these directions for creating a router, a :ref:`network<Creating a Network>` and :ref:`subnet<Creating a Subnet>` must already exist.

1. Click "Network" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ./images/networks_000.png
      :alt: Image showing the OpenStack Overview page. Routers is selected in the Network Topology fold-out menu in the left-hand navigation pane.

2. Click "Routers" in the fold-out menu.

   .. figure:: ./images/routers_001.png
      :alt: Image showing the OpenStack Router page. The Routers table is empty.

3. Click "+ Create Router" to open a dialog box.
4. Fill out the dialog box.

   a. Enter a "Router Name".
   b. Leave "Enable Admin State" checked.
   c. Select "uab-campus" in the "External Network" drop down box.
   d. Leave the "Availability Zone Hints" box empty.

   .. figure:: ./images/routers_002.png
      :alt: Image showing the Create Router dialog. The dialog is filled out. The name is my_router.

5. Click "Create Router".

   a. Redirects to the "Routers" page.
   b. There should be a new entry in the table with the name given in (4.a)

   .. figure:: ./images/routers_003.png
      :alt: Image showing the OpenStack Routers page. The Routers table has one entry. The entry is the my_router.

6. Now we need to connect the router to our subnet. Click the name of the new entry under the "Name" column to open the router "Overview" page.

   .. figure:: ./images/routers_004.png
      :alt: Image showing the my_router overview page. Three tabs are available. The Overview tab is selected.

7. Click the "Interfaces" tab.

   .. figure:: ./images/routers_005.png
      :alt: Image showing the my_router overview page. The Instances tab is selected. The table is empty.

8. Click "+ Add Interface" to open a dialog box.
9. Fill out the dialog box.

   a. Select an existing network-subnet pair in the "Subnet" drop down box.
   b. If this is your only router on the selected subnet, leave "IP Address" empty to use the subnet gateway.

   .. figure:: ./images/routers_006.png
      :alt: Image showing the Add Interface dialog. The dialog is filled out. The my_network subnet is selected as subnet.

10. Click "Submit"

    a. Redirects to the "Interfaces" page for the router.
    b. There should be a new entry in the table.

    .. figure:: ./images/routers_007.png
       :alt: Image showing the my_router overview page. The Instances tab is selected. The table has one entry with a random UUID string as name.

Creating a Security Group
-------------------------

These instructions show you how to prepare to use SSH with your instances. Security Groups are used to set rules for how external devices can connect to our instances. Here we will create an SSH Security Group using a method that can be applied to other types of connections. The method used can be applied to other types of Security Groups as well.

1. Click "Networks" in the left-hand navigation pane to open the fold-out menu.

   .. figure:: ./images/networks_000.png
      :alt: Image showing the OpenStack Overview page. Security Groups is selected in the Network Topology fold-out menu in the left-hand navigation pane.

2. Click "Security Groups" in the fold out menu.

   .. figure:: ./images/security_groups_001.png
      :alt: Image showing the OpenStack Security Groups page. The Security Groups table has one entry, the default, persistent entry labeled default.

3. Click "+ Create Security Group" to open a dialog box.
4. Fill out the dialog box.

   a. Under "Name" enter :code:`ssh`.
   b. Leave "Description" empty.

   .. figure:: ./images/security_groups_002.png
      :alt: Image showing the Create Security Group dialog. The dialog has been filled out with the name set as ssh.

5. Click "Create Security Group".

   a. Redirects to the "Manage Security Group Rules: ssh" page.
   b. There should be an entry for "Egress IPv4" and "Egress IPv6". Leave these alone.

   .. figure:: ./images/security_groups_003.png
      :alt: Image showing the Manage Security Group Rules for ssh. The Table has two entries, both Egress direction. One is for IPv4 and the other for IPv6. Both have no IP restrictions.

6. Click "+ Add Rule" to open a dialog box.

   a. Select "SSH" in the "Rule" drop down box. This will change the remaining fields.
   b. Leave "Description" empty.
   c. Select "CIDR" in the "Remote" drop down box.
   d. Type :code:`0.0.0.0/0` in the "CIDR" box. **WARNING!** This is **NOT** good practice! For your research instances, you'll want to constrain the CIDR value further to a narrower range of IP addresses. The rule we have shown here leaves the SSH port open to all IP addresses world-wide.

   .. figure:: ./images/security_groups_004.png
      :alt: Image showing the Add Rule dialog box. The dialog box is filled out. The rule is set to SSH.

7. Click "Add".

   a. Redirects to the "Manage Security Group Rules: ssh" page.
   b. There should be a new entry in the table.

   .. figure:: ./images/security_groups_005.png
      :alt: Image showing the Manage Security Group Rules for ssh. The Table has three entries. The new entry is Ingress direction with IPv4. It is restricted to TCP port 22 on all IPs.