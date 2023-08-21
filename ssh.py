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

        