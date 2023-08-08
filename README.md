# SSH Tool

The purpose of this application is to automate some of the networking configurations on Teltonika routers. This application only requires minor user input, most of the required settings will be taken from the Router/Gateway dynamically. In general, this application uses UCI commands(https://wiki.teltonika-networks.com/view/UCI_command_usage) for configuration.

# Usecase

The application requires access to the Router/Gateway via SSH, it can access either device via Private IP or Public IP. It is important to open a port for the SSH on the Router/Gateway, otherwise, the application will not be able to connect. The port for the SSH can be opened either on the Firewall rules or on the System > Administration > Access control: https://wiki.teltonika-networks.com/view/RUTX11_Administration#Access_Control

Once everything has been done on the Router/Gateway side we can continue with the Application. Once we run it, it will provide a simple interface, which will ask you for the IP address of the Router/Gateway, username for it(root), password, and SSH port.
And on the right side, you will see the buttons for each action you can perform. 

Before executing any actions we have to provide all of the login details, since once you press the action button the application will try to perform the SSH connection to the Router/Gateway.

Each action will be described below.

# VLAN

The VLAN action is used for creating a new fully working VLAN on a specific port on the Router.
The VLAN performs these actions in order:

1. Creates a new interface with the provided IP address (it automatically will use 255.255.255.0 netmask and enable the DHCP server)
2. The new interfaces metric will be set to the lowest
3. The script will create a new port-based VLAN, it will take the last known VLAN ID, and create a new VLAN with the higher ID number
4. Once the new VLAN is created, the new physical interface will appear, which will be assigned to the new network interface (step 1)
5. Lastly, the application will check for the assigned port-based VLANs on the First VLAN ID and remove the "Untagged" option from the port that was selected on the application GUI
