#coding:utf-8
import requests
import json
import time

class vm(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies
        
    #@创建单个虚拟机   
    def creat_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        templatename = li[1]
        usename = li[2]
        searchdata = {'searchType': 'strtemplatename','searchValue': templatename}
        searchurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/queryVmTemplateList.do'
        re = self.s.post(searchurl,cookies=self.cookies,data=searchdata)
        re_json = json.loads(re.text)
        tempalteid = re_json['data'][0]['id']
        tempaltestatus = re_json['data'][0]['irunstatus']
        searchuseurl = 'http://'+self.serverip+'/ark//account/user/query.do?searchParam={"searchType":"realOrUsername","searchValue":"'+usename+'"}&_=1543309277410'
        re_use = self.s.get(searchuseurl)
        re_use_json = json.loads(re_use.text)
        useid = re_use_json['data'][0]['uidUserId']
        vmdata = {
        "uidvmid": "",
        "edit_old_uidvmtemplateid":"", 
        "edit_old_strtemplatename": "",
        "irds": 0,
        "strvmname": vmname,
        "strdesc":"脚本创建测试虚拟机", 
        "strgroupid":"", 
        "uidvmpoolid": "",
        "uidcomputeresourcepoolid": "systemdefaultpool",
        "inettype": 1,
        "idhcp": 1,
        "strvmip":"", 
        "strvmmask": "255.255.255.0",
        "strvmgateway": "",
        "dns": 1,
        "strvmdns1": "",
        "strvmdns2": "",
        "basecreate": 1,
        "uidvmtemplateid": tempalteid,
        "basecreatecopyuidid": "",
        "basecreate_copy_strvmname":"", 
        "strosname": "Windows 7",
        "icpunum": 2,
        "imemorycapacity": 2048,
        "field_idiskcapacity": 60,
        "field_idiskcapacity_desc": "60GB",
        "iattachdisk":"", 
        "field_uiduserid": usename,
        "uiduserid": useid,
        "strsoundhwhda": "hda",
        "strsoundhwac97": "ac97",
        "strsoundhw": "all",
        "strnetcard": "virtio",
        "ivlan":"", 
        "strmgtname": "mgt0",
        "strdevtosynrvm":"", 
        "iifvirtio": 1,
        "iuefistart": 2,
        "strsoundhw": "all",
        "strnetcard": "virtio",
        "uidvmtemplateid": tempalteid,
        "uidvmimgid": ""
             }
        addvm_url = 'http://'+self.serverip+'/ark//cloud/desktop/saveVm.do'
        self.s.post(addvm_url,cookies=self.cookies,data=vmdata)
		
    #@查询虚拟机
    def query_vm(self,li):
        vmname = li
        querydata = {'searchType': 'strvmname','searchValue': vmname,'_': '1543978006678'}
        queryurl = 'http://'+self.serverip+'/ark/cloud/desktop/queryVmList.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        return re.text
		
    #@启动虚拟机
    def start_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/startVm.do'
        data = {'uidvmids': vmid,'irds': 0}
        self.s.post(url,cookies=self.cookies,data=data)
		
    #@停止虚拟机
    def stop_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/stopVm.do'
        data = {'uidvmids': vmid,'irds': 0}
        self.s.post(url,cookies=self.cookies,data=data)
		
    #@删除虚拟机
    def delete_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        delete_url = 'http://'+self.serverip+'/ark//cloud/desktop/deleteVm.do'
        delete_data = {"uidvmids": vmid,"irds": 0}
        self.s.post(delete_url,cookies=self.cookies,data=delete_data)

    #@新建虚拟机
    def creat_newvm(self,li):
        data = json.loads(li)
        if "," in data["field_uiduserid"]:
            userlist = data["field_uiduserid"].split(",")
        else:
            userlist = []
            userlist.append(data["field_uiduserid"])
        templatename = data["vmtemplate"]
        searchdata = {'searchType': 'strtemplatename','searchValue': templatename}
        searchurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/queryVmTemplateList.do'
        re = self.s.post(searchurl,cookies=self.cookies,data=searchdata)
        re_json = json.loads(re.text)
        tempalteid = re_json['data'][0]['id']
        strosname = re_json['data'][0]['strosname']
        icpunum = re_json['data'][0]['icpunum']
        idiskcapacity = re_json['data'][0]['idiskcapacity']
        imemorycapacity = re_json['data'][0]['imemorycapacity']
        vmdata = {
        "uidvmid": "",
        "edit_old_uidvmtemplateid":"", 
        "edit_old_strtemplatename": "",
        "irds": 0,
        "strvmname": data["strvmname"],
        "strdesc":"脚本创建测试虚拟机", 
        "strgroupid":"", 
        "uidvmpoolid": "",
        "uidcomputeresourcepoolid": "systemdefaultpool",
        "inettype": 1,
        "idhcp": 1,
        "strvmip":"", 
        "strvmmask": "255.255.255.0",
        "strvmgateway": "",
        "dns": 1,
        "strvmdns1": "",
        "strvmdns2": "",
        "basecreate": 1,
        "uidvmtemplateid": "",
        "basecreatecopyuidid": "",
        "basecreate_copy_strvmname":"", 
        "strosname": "Windows 7",
        "icpunum": icpunum,
        "imemorycapacity": imemorycapacity,
        "field_idiskcapacity": idiskcapacity,
        "field_idiskcapacity_desc": str(idiskcapacity)+"GB",
        "iattachdisk":"", 
        "field_uiduserid": data["field_uiduserid"],
        "uiduserid": "",
        "strsoundhwhda": "hda",
        "strsoundhwac97": "ac97",
        "strsoundhw": "all",
        "strnetcard": "virtio",
        "ivlan":"", 
        "strmgtname": "mgt0",
        "strdevtosynrvm":"", 
        "iifvirtio": 1,
        "iuefistart": 2,
        "strsoundhw": "all",
        "strnetcard": "virtio",
        "uidvmtemplateid": "",
        "uidvmimgid": ""
             }
        
        
        idlist = ""
        for usename in userlist:
            searchuseurl = 'http://'+self.serverip+'/ark//account/user/query.do?searchParam={"searchType":"realOrUsername","searchValue":"'+usename+'"}&_=1543309277410'
            re_use = self.s.get(searchuseurl)
            re_use_json = json.loads(re_use.text)
            useid = re_use_json['data'][0]['uidUserId']
            idlist = idlist + useid +","
        vmdata["uiduserid"] = idlist[:-1]
        vmdata["uidvmtemplateid"] = tempalteid
        addvm_url = 'http://'+self.serverip+'/ark//cloud/desktop/saveVm.do'
        self.s.post(addvm_url,cookies=self.cookies,data=vmdata)
        
    #@停用虚拟机
    def disable_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        disable_url = 'http://'+self.serverip+'/ark//cloud/desktop/disableVm.do'
        disable_data = {"uidvmids": vmid,"irds": 0}
        self.s.post(delete_url,cookies=self.cookies,data=delete_data)

    #@启用虚拟机
    def enable_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        disable_url = 'http://'+self.serverip+'/ark//cloud/desktop/enableVm.do'
        disable_data = {"uidvmids": vmid,"irds": 0}
        self.s.post(delete_url,cookies=self.cookies,data=delete_data)
        
    #@修复虚拟机
    def recover_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/recoveryVM.do'
        data = {'uidvmids': vmid,'irds': 0}
        self.s.post(url,cookies=self.cookies,data=data)

    #@重置虚拟机
    def reset_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/resetVm.do'
        data = {'uidvmids': vmid,'irds': 0}
        self.s.post(url,cookies=self.cookies,data=data)

    #@强制关闭虚拟机
    def forcestop_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/forceStopVm.do'
        data = {'uidvmids': vmid,'irds': 0}
        self.s.post(url,cookies=self.cookies,data=data)

    #@创建虚拟机快照
    def creat_snapshot(self,li):
        li = li.split(",")
        vmname = li[0]
        strbackupdesc = li[1]
        re = self.query_vm(vmname)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/createSnapshot.do'
        data = {'uidvmids': vmid,'irds': 0,'strbackupdesc':strbackupdesc}
        self.s.post(url,cookies=self.cookies,data=data)

    #@快照启动虚拟机
    def snapshot_runvm(self,li):
        li = li.split(",")
        vmname = li[0]
        querydata = {'searchType': 'strvmname','searchValue': vmname}
        queryurl = 'http://'+self.serverip+'/ark/systemManage/vmBackup/queryVMBackupStatistics.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        re_json = json.loads(re)
        vmid = re_json["data"][0]["id"]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/startVmBySnapshoot.do'
        data = {'uidvmids': vmid,'irds': 0}
        self.s.post(url,cookies=self.cookies,data=data)

    #@查询快照
    def query_snapshot(self,li):
        li = li.split(",")
        vmname = li[0]
        backupdesc = li[1]
        querydata = {'searchType': 'strvmname','searchValue': vmname}
        queryurl = 'http://'+self.serverip+'/ark/systemManage/vmBackup/queryVMBackupStatistics.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        re_json = json.loads(re.text)
        for backup in re_json['data']:
            if backupdesc == backup['strbackupdesc']:
                return str(backup)

    #@还原快照
    def restore_vmbackup(self,li):
        li = li.split(",")
        vmname = li[0]
        strbackupdesc = li[1]
        querydata = {'searchType': 'strvmname','searchValue': vmname}
        queryurl = 'http://'+self.serverip+'/ark/systemManage/vmBackup/queryVMBackupStatistics.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        re_json = json.loads(re.text)
        for backup in re_json['data']:
            if strbackupdesc == backup['strbackupdesc']:
                vmbackupid = backup['uidvmbackupid']
        url = 'http://'+self.serverip+'/ark/systemManage/vmBackup/restoreVMBackup.do'
        data = {'uidvmbackupids': vmbackupid}
        self.s.post(url,cookies=self.cookies,data=data)

    #@删除快照
    def delete_vmbackup(self,li):
        li = li.split(",")
        vmname = li[0]
        strbackupdesc = li[1]
        querydata = {'searchType': 'strvmname','searchValue': vmname}
        queryurl = 'http://'+self.serverip+'/ark/systemManage/vmBackup/queryVMBackupStatistics.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        re_json = json.loads(re.text)
        for backup in re_json['data']:
            if strbackupdesc == backup['strbackupdesc']:
                vmbackupid = backup['uidvmbackupid']
        url = 'http://'+self.serverip+'/ark/systemManage/vmBackup/delVMBackup.do'
        data = {'uidvmbackupids': vmbackupid}
        self.s.post(url,cookies=self.cookies,data=data)

    #@虚拟机导出模板
    def vm_template(self,li):
        li = li.split(",")
        vmname = li[0]
        templatename = li[1]
        searchvmurl = 'http://'+self.serverip+'/ark/cloud/desktop/queryVmList.do?irds=0'
        searchvmdata = {"searchType": "strvmname","searchValue": vmname,"_": "1543313387455"}
        re_vm = self.s.post(searchvmurl,cookies=self.cookies,data=searchvmdata)
        re_vm_json = json.loads(re_vm.text)
        vmid = re_vm_json['data'][0]['id']
        strostype = re_vm_json['data'][0]['stroskey']
        icpunum = re_vm_json['data'][0]['icpunum']
        imemorycapacity = re_vm_json['data'][0]['imemorycapacity']
        idiskcapacity = re_vm_json['data'][0]['idiskcapacity']
        strmgtname = re_vm_json['data'][0]['strmgtname']
        iifvirtio = re_vm_json['data'][0]['iifvirtio']
        iuefistart = re_vm_json['data'][0]['iuefistart']
        data ={
           'uidvmtemplateid':'', 
           'strtemplatename': templatename,
           'stroskey':strostype,
           'strdesc': '虚拟机创建模板',
           'icpunum': icpunum,
           'imemorycapacity': imemorycapacity,
           'idiskcapacity': idiskcapacity,
           'iattachdisk': '',
           'strsoundhw': 'all',
           'uidvmimgid': '',
           'uidbasevmid': vmid,
           'basecreatecopyuidid': '',
           'ivlan': '',
           'strmgtname': strmgtname,
           'uidcomputeresourcepoolid': 'systemdefaultpool',
           'iifvirtio': iifvirtio,
           'iuefistart': iuefistart,
           'uidfolderid': '',
           'icreatetype': 0,
           'irds': 0
           }
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/saveVmTemplate.do'
        self.s.post(url,cookies=self.cookies,data=data)

#vm = vm('192.168.60.200')
#vm.start_vm("测试虚拟机-testuser02")
#time.sleep(60)
#vm.stop_vm("测试虚拟机-testuser02")
#vm.creat_newvm('{"strvmname": "yhg虚拟机","vmtemplate": "测试模板","field_uiduserid":"测试01,测试02,测试03"}')
#vm.creat_newvm('{"strvmname": "创建单个虚拟机","vmtemplate": "测试模板","field_uiduserid":"测试04"}')
#vm.query_snapshot('批量测试-yhg200,yhg')
#re = vm.query_vm("测试虚拟机-testuser02")
#print(re)
#vm.delete_vmbackup('批量测试-yhg200,yhg')
