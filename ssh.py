import paramiko

class SSH_connection:
    """"Class responsible for SSH commands execution"""

    def vlan_config(self, client, ip, port_number):
        """VLAN configuration via SSH"""
       
        #Preparing VLAN and Metric 

        stdin, stdout, stderr = client.exec_command("awk '/metric/ { if ($NF > max) max = $NF } END { print max }' /etc/config/network")
        stdin1, stdout1, stderr1 = client.exec_command("awk '/vid/ { if ($NF > max) max = $NF } END { print max }' /etc/config/network")

        #Getting the last used VLAN ports and removing the new prot from the list
        stdin4, stdout4, stderr4 = client.exec_command("grep 'option ports' /etc/config/network | awk -F \"'\" '{print $2}' | head -n 1")
        ports_before_change = stdout4.read().decode().strip()

        highest_metric = stdout.read().decode().strip().replace("'", "")
        highest_vlan = stdout1.read().decode().strip().replace("'", "")

        highest_metric = int(highest_metric) + 1
        highest_metric_str = str(highest_metric)

        highest_vlan_str = str(highest_vlan)
        highest_vlan_plus = int(highest_vlan) + 1
        highest_vlan_plus_str = str(highest_vlan_plus)

        port_number = port_number + 1
        port_number_str = str(port_number)
        port_number_for_replacement = " " + port_number_str

        #Creating a new interface + dhcp pool commands
        interface = f"uci set network.test50=interface && uci set network.test50.metric='{highest_metric_str}' && uci set network.test50.ipaddr='{ip}' && uci set network.test50.netmask='255.255.255.0' && uci set network.test50.delegate='1' && uci set network.test50.force_link='0' && uci set network.test50.proto='static' && uci set dhcp.test50=dhcp && uci set dhcp.test50.start='100' && uci set dhcp.test50.leasetime='12h' && uci set dhcp.test50.limit='51' && uci set dhcp.test50.interface='test50' && uci commit"
        stdin2, stdout2, stderr2 = client.exec_command(interface)

        #Creating VLAN and attaching it to the interface
        vlan = f"uci add network switch_vlan && uci set network.@switch_vlan[{highest_vlan_str}].device='switch0' && uci set network.@switch_vlan[{highest_vlan_str}].vlan='{highest_vlan_plus_str}' && uci set network.@switch_vlan[{highest_vlan_str}].vid='{highest_vlan_plus_str}' && uci set network.@switch_vlan[{highest_vlan_str}].ports='{port_number_str} 0' && uci commit"
        stdin3, stdout3, stderr3 = client.exec_command(vlan)

        ports_after_change = ports_before_change.replace(port_number_for_replacement, "")
        replcate_ports = f"uci set network.@switch_vlan[0].ports='{ports_after_change}' && uci set network.test50.device='eth0.{highest_vlan_plus_str}' && uci commit"
        stdin5, stdout5, stderr5 = client.exec_command(replcate_ports)
        
        stdin6, stdout6, stderr6 = client.exec_command("/etc/init.d/network restart")

    def l2tp_server_config(self, client, server_ip, client_ip):
        """Configuration for L2TP server via SSH"""

        #Server and ip clients variables for uci commands
        server_ip_str = str(server_ip)
        client_ip_str = str(client_ip)
        server_ip_limit = server_ip_str + ".30"
        server_ip_for_uci = server_ip_str + ".1"
        server_ip_start = server_ip_str + ".20"

        #Creating xl2tp interface
        xl2tp_server = f"uci add xl2tpd test51 && uci set xl2tpd.test51=service && uci set xl2tpd.test51.type='server' && uci set xl2tpd.test51.limit='{server_ip_limit}' && uci set xl2tpd.test51.localip='{server_ip_for_uci}' && uci set xl2tpd.test51.start='{server_ip_start}' && uci set xl2tpd.test51._name='test51' && uci set xl2tpd.test51.chap='0' && uci set xl2tpd.test51.enabled='1' && uci add xl2tpd login && uci set xl2tpd.@login[0].username='test' && uci set xl2tpd.@login[0].password='test12345' && uci set xl2tpd.@login[0].remoteip='{client_ip_str}' && uci commit"

        stdin, stdout, stderr = client.exec_command(xl2tp_server)

        #Gathering current firewall last setting number
        firewall_id = "uci show firewall | grep -Eo 'firewall\.([0-9]+)' | awk -F'.' '{print $2}' | tail -n 1"
        stdin1, stdout1, stderr1 = client.exec_command(firewall_id)
        highest_id = stdout1.read().decode().strip()

        highest_id = int(highest_id) + 1
        highest_id_str = str(highest_id)

        #Adding new firewall settings for l2tp connection

        #IDs for commands
        new_id = highest_id_str
        new_id_1 = highest_id + 1
        new_id_2 = highest_id + 2
        new_id_3 = highest_id + 3
        new_id_4 = highest_id + 4
        new_id_str = str(new_id)
        new_id_1_str = str(new_id_1)
        new_id_2_str = str(new_id_2)
        new_id_3_str = str(new_id_3)
        new_id_4_str = str(new_id_4)

        command = f"uci set firewall.{new_id_str}=zone && uci set firewall.{new_id_str}.name='l2tp' && uci set firewall.{new_id_str}.device='l2tp+ xl2tp+' && uci set firewall.{new_id_str}.input='ACCEPT' && uci set firewall.{new_id_str}.forward='REJECT' && uci set firewall.{new_id_str}.masq='1' && uci set firewall.{new_id_str}.output='ACCEPT'"
        stdin, stdout, stderr = client.exec_command(command)
            
        command1 = f"uci set firewall.{new_id_1_str}=forwarding && uci set firewall.{new_id_1_str}.dest='lan' && uci set firewall.{new_id_1_str}.src='l2tp'"
        stdin2, stdou2, stderr2 = client.exec_command(command1)
            
        command2 = f"uci set firewall.{new_id_2_str}=forwarding && uci set firewall.{new_id_2_str}.dest='wan' && uci set firewall.{new_id_2_str}.src='l2tp'"
        stdin3, stdout3, stderr3 = client.exec_command(command2)
            
        command3 = f"uci set firewall.{new_id_3_str}=forwarding && uci set firewall.{new_id_3_str}.dest='l2tp' && uci set firewall.{new_id_3_str}.src='lan'"
        stdin4, stdout4, stderr4 = client.exec_command(command3)
            
        command4 = f"uci set firewall.{new_id_4_str}=rule && uci set firewall.{new_id_4_str}.dest_port='1701' && uci set firewall.{new_id_4_str}.src='wan' && uci set firewall.{new_id_4_str}.name='Allow-l2tp-traffic' && uci set firewall.{new_id_4_str}.target='ACCEPT' && uci set firewall.{new_id_4_str}.vpn_type='l2tp' && uci set firewall.{new_id_4_str}.proto='udp && uci set firewall.{new_id_4_str}.family='ipv4'"
        stdin5, stdout5, stderr5 = client.exec_command(command4)

        stdin6, stdout6, stderr6 = client.exec_command("uci commit")