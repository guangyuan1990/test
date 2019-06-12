#coding:utf-8
import wmi
import win32api
import os

class vmwin(object):
    def __init__(self,serverip):
        self.serverip = serverip

    #@查询虚拟机磁盘信息
    def query_vmdisk(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        disk_dict = {}
        win = wmi.WMI(computer=computer,user=user,password=password)
        disk_data = win.Win32_LogicalDisk ()
        for disk in disk_data:
            if disk.Size:
                disk_dict[disk.Name] = str(float(disk.Size)/1024/1024/1024)[0:4]
            else:
                disk_dict[disk.Name] = None
        return str(disk_dict)

    #@查询虚拟机系统信息
    def query_vmsystem(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        os = {}
        win = wmi.WMI(computer=computer,user=user,password=password)
        system = win.Win32_OperatingSystem()
        memory = win.Win32_PhysicalMemory()
        os["osname"] = system[0].Caption
        os["osbit"] = system[0].OSArchitecture
        os["computername"] = system[0].CSName
        os["memory"] = int(memory[0].Capacity)/1024/1024
        os["SerialNumber"] = system[0].SerialNumber
        return str(os)

    #@远程重启虚拟机
    def reboot_vm(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        win = wmi.WMI(computer=computer,user=user,password=password)
        os = win.Win32_OperatingSystem(Primary=True)
        os[0].Reboot()

    #@远程关闭虚拟机
    def shutdown_vm(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        win = wmi.WMI(computer=computer,user=user,password=password)
        os = win.Win32_OperatingSystem(Primary=True)
        os[0].Shutdown()

    #@查询虚拟机进程信息
    def query_vmprocess (self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        processname = li[3]
        process_dict = {}
        win = wmi.WMI(computer=computer,user=user,password=password)
        process = win.Win32_Process(Name = processname)
        process_dict["handlecount"] = process[0].HandleCount
        process_dict["name"] = process[0].Name
        process_dict["creattime"] = process[0].CreationDate[0:14]
        process_dict["WorkingSetSize"] = int(process[0].WorkingSetSize)/1024        
        return str(process_dict)

    #@查询虚拟机网络适配器信息
    def query_vmnet(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        adapter = {}
        win = wmi.WMI(computer=computer,user=user,password=password)
        networkadapter = win.Win32_NetworkAdapter(NetEnabled = True)
        adapter["AdapterType"] = networkadapter[0].AdapterType
        adapter["MACAddress"] = networkadapter[0].MACAddress
        adapter["NetConnectionID"] = networkadapter[0].NetConnectionID
        adapter["Speed"] = int(networkadapter[0].Speed)/1000/1000
        return str(adapter)
    
    #@查询虚拟机网络信息
    def query_net(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        net = {}
        win = wmi.WMI(computer=computer,user=user,password=password)
        network = win.Win32_NetworkAdapterConfiguration(IPEnabled = True)
        net["DefaultIPGateway"] = network[0].DefaultIPGateway
        net["DHCPServer"] = network[0].DHCPServer
        net["DNSDomain"] = network[0].DNSDomain
        net["IPAddress"] = network[0].IPAddress
        net["MACAddress"] = network[0].MACAddress
        return str(net)

    #@修改虚拟机IPv4地址
    def set_staticip(self,li):#修改ip后由于wmi断开，导致连接一直无返回，进程卡住问题，暂未解决，该关键字不可用
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        ip = li[3]
        mask = li[4]
        win = wmi.WMI(computer=computer,user=user,password=password)
        networkadapter = win.Win32_NetworkAdapterConfiguration(IPEnabled=1)
        networkadapter[0].EnableStatic([ip],[mask])
    
    #@设置虚拟机域名地址
    def set_dns(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        dnsip = li[3]
        win = wmi.WMI(computer=computer,user=user,password=password)
        networkadapter = win.Win32_NetworkAdapterConfiguration(IPEnabled=1)
        networkadapter[0].SetDNSDomain(dnsip)

    #@查找虚拟机文件信息
    def query_file(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        filepath = li[3]
        file_dict = {}
        filename = os.path.basename(filepath).split(".")[0]
        win = wmi.WMI(computer=computer,user=user,password=password)
        files = win.CIM_LogicalFile(FileName = filename)
        for file in files:
            if file.Name == filepath:
                file_dict["name"] = file.FileName
                file_dict["FileSize"] = file.FileSize
                file_dict["filepath"] = file.Caption
                file_dict["FileType"] = file.FileType
        return str(file_dict)

    #@虚拟机文件重命名
    def rename_vmfile(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        filepath = li[3]
        name = li[4]
        filename = os.path.basename(filepath).split(".")[0]
        win = wmi.WMI(computer=computer,user=user,password=password)
        files = win.CIM_LogicalFile(FileName = filename)
        for file in files:
            if file.Name == filepath:
                file.Rename(name)

    #@启动虚拟机计划任务
    def start_task(self,li):
        li = li.split(',')
        computer = li[0]
        user = li[1]
        password = li[2]
        planname = li[3]
        win = wmi.WMI(computer=computer,user=user,password=password)
        process = win.Win32_Process
        process.Create('schtasks /run /tn \"'+planname+'"')
        
        
        
#vmwin = vmwin('192.168.60.200')
#re = vmwin.query_vmdisk("192.168.7.2,cloud,123456")
#print(re)                        
#re = vmwin.query_diskname("192.168.7.2,cloud,123456")
#re = vmwin.query_vmfreedisk("192.168.7.2,cloud,123456,C:")
#re = vmwin.query_vmname("192.168.7.2,cloud,123456")
#vmwin.reboot_vm("192.168.7.2,administrator,123456")
#re = vmwin.quer_vmVisibleMemorySize("192.168.7.2,cloud,123456")

#vmwin.set_dns("192.168.7.2,administrator,123456,192.168.39.160")
#re = vmwin.query_file("192.168.7.2,administrator,123456,c:\yhg")
#print (re)
#vmwin.rename_vmfile("192.168.7.2,administrator,123456,c:\yhg.txt,c:\yhgnew.txt")

#vmwin.start_task("192.168.7.2,administrator,123456,chrome")
