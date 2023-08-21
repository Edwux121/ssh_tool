import tkinter as tk
import paramiko

from ssh import SSH_connection

class L2TP_server:
    """Class for creating L2TP Server"""

    def __init__(self, root):
        self.root = root
        self.ssh_calls = SSH_connection()
        self.ip = 0
        self.user = "user"
        self.passw = "pass"
        self.port_nr = 22

    def open_l2tp_window(self, root, ip, user, passw, port_nr):
        """Opening L2TP server window"""

        #SSH connection
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=passw, port=port_nr)

        l2tp_window = tk.Toplevel(root)
        l2tp_window.title("L2TP Server")
        l2tp_window.minsize(600, 600)

        #Layout for L2TP
        l2tp_grid = tk.Frame(l2tp_window, width=600, height=600)
        l2tp_grid.grid(column=0, row=0)

        server_ip_label = tk.Label(l2tp_grid, text="Server IP", font=("Arial 24"))
        client_ip_label = tk.Label(l2tp_grid, text="Client IP", font=("Arial 24"))

        server_ip_label.grid(column=0, row=0)
        client_ip_label.grid(column=0, row=1)

        server_ip_entry = tk.Entry(l2tp_grid, font=("Arial 24"))
        client_ip_entry = tk.Entry(l2tp_grid, font=("Arial 24"))
        server_ip_entry.grid(column=1, row=0)
        client_ip_entry.grid(column=1, row=1)

        button = tk.Button(l2tp_grid, font=("Arial 24"), text="Create", width=15, command=lambda:self.ssh_calls.l2tp_server_config(client, server_ip_entry.get(), client_ip_entry.get()))
        button.grid(column=0, row=3)