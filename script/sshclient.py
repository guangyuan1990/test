import paramiko
import time


class sshclient(object):
    def __init__(self,serverip):
        #paramiko.SSHClient()连接有问题
        self.serverip = serverip
        self.ssh = paramiko.Transport((self.serverip,9822))
        self.ssh.connect(username = 'admin',password='admin')
        self.chan = self.ssh.open_session()
        self.chan.settimeout(30)
        self.chan.get_pty()
        self.chan.invoke_shell()


    #@ssh执行命令
    def sshaction(self,li):
        action = li
        self.chan.send('\n')
        time.sleep(1)
        one = self.chan.recv(65535)
        self.chan.send(action+'\n')
        time.sleep(3)
        re = self.chan.recv(65535)
        sre = bytes.decode(re)#bytes转str
        

    #@ssh查询命令
    def ssh_query(self,li):
        action = li
        self.chan.send('\n')
        time.sleep(1)
        one = self.chan.recv(65535)
        self.chan.send(action+'\n')
        time.sleep(5)
        re = self.chan.recv(65535)
        sre = bytes.decode(re)#bytes转str
        data = ""
        for node in sre.split("\n")[3:-1]:
            data = data + node+"\n"
        return data

#ssh = sshclient("192.168.60.50")
#ssh.sshaction("show dss")
#re = ssh.ssh_query("webctl show")
#print(re)
#node_list = re.split("\n")[3:-1]
#for node in node_list:
    #print(node)
