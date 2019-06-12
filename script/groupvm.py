#coding:utf-8
import requests
import json
import time

class groupvm(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    def query_vmid(self,vmname):#查询虚拟机id
        vmname = vmname
        querydata = {'searchType': 'strvmname','searchValue': vmname,'_': '1543978006678'}
        queryurl = 'http://'+self.serverip+'/ark/cloud/desktop/queryVmList.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        re_json = json.loads(re.text)
        vmid = re_json["data"][0]["id"]
        return vmid

    def query_vmgroupdict(self,groupname):#查询虚拟机分组,返回字典形式
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/queryAllVmGroups.do?_=1547446098477'
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for vmgroup in re_json['data']:
            if groupname == vmgroup['strgroupname']:
                return vmgroup
        
    #@创建虚拟机分组
    def creat_vmgroup(self,li):
        li = li.split(',')
        groupname = li[0]
        groupdesc = li[1]
        concurrent = li[2]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/saveVmGroup.do'
        data = {
               'strgroupid':'', 
               'strgroupname': groupname,
               'strgroupdesc': groupdesc,
               'maxconcurrent': concurrent,
               'vms': '',
               }
        self.s.post(url,data=data,cookies=self.cookies)
        
    #@查询虚拟机分组
    def query_vmgroup(self,li):
        li = li.split(',')
        groupname = li[0]
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/queryAllVmGroups.do?_=1547446098477'
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for vmgroup in re_json['data']:
            if groupname == vmgroup['strgroupname']:
                return str(vmgroup)
            
    #@删除虚拟机分组
    def delete_vmgroup(self,li):
        li = li.split(',')
        groupname = li[0]
        vmgroup = self.query_vmgroupdict(groupname)
        vmgroupid = vmgroup['strgroupid']
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/deleteVmGroups.do'
        data = {'vmGroupIds': groupid}
        self.s.post(url,data=data,cookies=self.cookies)

    #@添加虚拟机到分组
    def addvm_group(self,li):
        li = li.split(',')
        groupname = li[0]
        vmname = li[1]
        vmgroup = self.query_vmgroupdict(groupname)
        vmgroupid = vmgroup['strgroupid']
        groupdesc = vmgroup['strgroupdesc']
        concurrent = vmgroup['maxconcurrent']
        vmid = self.query_vmid(vmname)
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/saveVmGroup.do'
        data = {
               'strgroupid':vmgroupid, 
               'strgroupname': groupname,
               'strgroupdesc': groupdesc,
               'maxconcurrent': concurrent,
               'vms': vmid,
               'hideSelectVm': vmid
               }
        self.s.post(url,data=data,cookies=self.cookies)

    #@移除分组下虚拟机
    def remove_groupvm(self,li):
        li = li.split(',')
        groupname = li[0]
        vmgroup = self.query_vmgroupdict(groupname)
        vmgroupid = vmgroup['strgroupid']
        groupdesc = vmgroup['strgroupdesc']
        concurrent = vmgroup['maxconcurrent']
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/saveVmGroup.do'
        data = {
               'strgroupid':vmgroupid, 
               'strgroupname': groupname,
               'strgroupdesc': groupdesc,
               'maxconcurrent': concurrent,
               'vms': '',
               }
        self.s.post(url,data=data,cookies=self.cookies)

    #@修改虚拟机分组
    def repair_vmgroup(self,li):
        li = li.split(',')
        groupname = li[0]
        newgrouname = li[1]
        groupdesc = li[2]
        concurrent = li[3]
        vmgroup = self.query_vmgroupdict(groupname)
        vmgroupid = vmgroup['strgroupid']
        url = 'http://'+self.serverip+'/ark//cloud/desktop/vmGroup/saveVmGroup.do'
        data = {
               'strgroupid':vmgroupid, 
               'strgroupname': groupname,
               'strgroupdesc': groupdesc,
               'maxconcurrent': concurrent,
               'vms': '',
               }
        self.s.post(url,data=data,cookies=self.cookies)
       
#group = groupvm('192.168.60.200')
#group.creat_vmgroup('yhg分组,yhg,3')
#re=group.query_vmgroup('yhg分组')
#group.delete_vmgroup('yhg分组')
#re = group.query_vmgroupdict('yhg分组')
#data = '{"strgroupid": ,"strgroupname": "yhg分组1","strgroupdesc": "","maxconcurrent": 0,"vms": }'
#group.creat_vmsgroup(data)

