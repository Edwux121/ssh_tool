import paramiko

class SSH_connection:
    """"Class responsible for SSH commands execution"""

    def vlan_config(self, client, ip, port_number):
        """VLAN configuration"""
       
        #Preparing VLAN and Metric 

        stdin, stdout, stderr = client.exec_command("awk '/metric/ { if ($NF > max) max = $NF } END { print max }' /etc/config/network")
        stdin1, stdout1, stderr1 = client.exec_command("awk '/vid/ { if ($NF > max) max = $NF } END { print max }' /etc/config/network")

        highest_metric = stdout.read().decode().strip().replace("'", "")
        highest_vlan = stdout1.read().decode().strip().replace("'", "")

        highest_metric = int(highest_metric) + 1
        highest_metric_str = str(highest_metric)

        highest_vlan_str = str(highest_vlan)
        highest_vlan_plus = int(highest_vlan) + 1
        highest_vlan_plus_str = str(highest_vlan_plus)

        port_number = port_number + 1
        port_number_str = str(port_number)

        #Creating a new interface + dhcp pool commands
        interface = f"uci set network.test50=interface && uci set network.test50.metric='{highest_metric_str}' && uci set network.test50.ipaddr='{ip}' && uci set network.test50.netmask='255.255.255.0' && uci set network.test50.delegate='1' && uci set network.test50.force_link='0' && uci set network.test50.proto='static' && uci set dhcp.test50=dhcp && uci set dhcp.test50.start='100' && uci set dhcp.test50.leasetime='12h' && uci set dhcp.test50.limit='51' && uci set dhcp.test50.interface='test50' && uci commit"
        stdin2, stdout2, stderr2 = client.exec_command(interface)

        #Creating VLAN and attaching it to the interface
        vlan = f"uci add network switch_vlan && uci set network.@switch_vlan[{highest_vlan_str}].device='switch0' && uci set network.@switch_vlan[{highest_vlan_str}].vlan='{highest_vlan_plus_str}' && uci set network.@switch_vlan[{highest_vlan_str}].vid='{highest_vlan_plus_str}' && uci set network.@switch_vlan[{highest_vlan_str}].ports='0t {port_number_str}' && uci set network.test50.device='eth0.{highest_vlan_plus_str}' && uci commit"
        stdin3, stdout3, stderr3 = client.exec_command(vlan)

        #client.close()