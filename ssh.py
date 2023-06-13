import paramiko

class SSH_connection:
    """"Class responsible for SSH connection"""

    def __init__(self):
        self.ip = 0
        self.user = "user"
        self.passw = "pass"

    def connect(self, ip, user, passw):
        """Connecting to device's SSH"""
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=passw, port=223)

        client.close()