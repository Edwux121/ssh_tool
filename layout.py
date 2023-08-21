import tkinter as tk

from ssh import SSH_connection
from vlan import Vlan
from l2tp_server import L2TP_server

class Layout:
    """Class for the display window layout"""

    def __init__(self, frame1, frame2, main_app):
        self.frame1 = frame1
        self.frame2 = frame2
        self.main_app = main_app

        self.ssh_connect = SSH_connection()
        self.vlan_window = Vlan(main_app)
        self.l2tp_server_window = L2TP_server(main_app)


    def data_fields(self):
        """Function for data fiels/first grid"""

        #Labels
        ip_label = tk.Label(self.frame1, text="Device's IP", font=("Arial 24"))
        username_label = tk.Label(self.frame1, text="Username", font=("Arial 24"))
        pass_label = tk.Label(self.frame1, text="Password", font=("Arial 24"))
        port_label = tk.Label(self.frame1, text="Port", font=("Arial 24"))

        #Entries
        ip_entry = tk.Entry(self.frame1, font=("Arial 24"))
        username_entry = tk.Entry(self.frame1, font=("Arial 24"))
        pass_entry = tk.Entry(self.frame1, font=("Arial 24"))
        port_entry = tk.Entry(self.frame1, font=("Arial 24"))

        #Buttons
        #connect_button = tk.Button(self.frame1, text="Connect", font=("Arial 24"), command=lambda:self.ssh_connect.connect(
        #    ip_entry.get(), username_entry.get(), pass_entry.get(), port_entry.get()
        #))

        #Grid
        ip_label.grid(column=0, row=0, padx=15, pady=15)
        ip_entry.grid(column=0, row=1, padx=15, pady=15)
        username_label.grid(column=0, row=2, padx=15, pady=15)
        username_entry.grid(column=0, row=3, padx=15, pady=15)
        pass_label.grid(column=0, row=4, padx=15, pady=15)
        pass_entry.grid(column=0, row=5, padx=15, pady=15)
        port_label.grid(column=0, row=6, padx=15, pady=15)
        port_entry.grid(column=0, row=7, padx=15, pady=15)
        #connect_button.grid(column=0, row=8, padx=15, pady=15)

        #Buttons
        button1 = tk.Button(self.frame2, text="Vlan", font=("Arial 24"), width=15, command=lambda:self.vlan_window.open_vlan_window(self.main_app,
            ip_entry.get(), username_entry.get(), pass_entry.get(), port_entry.get()
        ))
        button2 = tk.Button(self.frame2, text="Button2", font=("Arial 24"), width=15)
        button3 = tk.Button(self.frame2, text="L2TP Server", font=("Arial 24"), width=15, command=lambda:self.l2tp_server_window.open_l2tp_window(self.main_app,
            ip_entry.get(), username_entry.get(), pass_entry.get(), port_entry.get()
        ))
        button4 = tk.Button(self.frame2, text="L2TP Client", font=("Arial 24"), width=15)
        button5 = tk.Button(self.frame2, text="Button5", font=("Arial 24"), width=15)
        button6 = tk.Button(self.frame2, text="Button6", font=("Arial 24"), width=15)

        #Grid
        button1.grid(column=0, row=0, padx=20, pady=20)
        button2.grid(column=1, row=0, padx=20, pady=20)
        button3.grid(column=0, row=2, padx=20, pady=20)
        button4.grid(column=1, row=2, padx=20, pady=20)
        button5.grid(column=0, row=3, padx=20, pady=20)
        button6.grid(column=1, row=3, padx=20, pady=20)