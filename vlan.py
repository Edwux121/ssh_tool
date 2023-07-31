import tkinter as tk
import paramiko

from ssh import SSH_connection

class Vlan:
    """Class for VLAN configuration Window"""

    def __init__(self, root):
        self.root = root
        self.ssh_calls = SSH_connection()
        self.ip = 0
        self.user = "user"
        self.passw = "pass"
        self.port_nr = 22


    def open_vlan_window(self, root, ip, user, passw, port_nr):
        """Opens Vlan Window"""

        #SSH connection
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=passw, port=port_nr)


        vlan_window = tk.Toplevel(root)
        vlan_window.title("Vlan")
        vlan_window.minsize(600, 600)

        #Layout for Vlan window
        grid_vlan = tk.Frame(vlan_window, width=600, height=600)
        grid_vlan.grid(column=0, row=0)

        ip_label = tk.Label(grid_vlan, text="IP", font=("Arial 24"))
        port_label = tk.Label(grid_vlan, text="Select Physical Port:", font=("Arial 24"))
        ip_label.grid(column=0, row=0)
        port_label.grid(column=0, row=1)
        
        ip_entry = tk.Entry(grid_vlan, font=("Arial 24"))
        ip_entry.grid(column=1, row=0)

        button = tk.Button(grid_vlan, text="Create", font=("Arial 24"), width=15, command=lambda:self.ssh_calls.vlan_config(client, ip_entry.get(), port_number.get()))
        button.grid(column=0, row=3)

        #Dropdown options
        port_number = tk.IntVar()
        options = [1, 2, 3, 4, 5]
        port_number.set(options[0])
        dropdown_menu = tk.OptionMenu(grid_vlan, port_number, *options)
        dropdown_menu.grid(column=1, row=1)