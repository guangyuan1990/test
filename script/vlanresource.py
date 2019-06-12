#coding:utf-8
import requests
import json
import time

class vlanresource(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    #@添加vlan
    def add_vlan(self,li):
        li = li.split(",")
        vlanid = li[0]
        vlanname = li[1]
        vmnum = li[2]
        desc = li[3]
        data = {
            'id': vlanid,
            'name': vlanname,
            'max_vm_num': vmnum,
            'vm_download_speed': -1,
            'desc': desc}
        url = 'http://'+self.serverip+'/ark/resourcePool/netResource/vlan/addVlan.do'
        self.s.post(url,data = data,cookies = self.cookies)
        
    #@删除vlan
    def del_vlan(self,li):
        li = li.split(",")
        vlanid = li[0]
        vlanname = li[1]
        data = {"uidvlanids": vlanid,"strVlanNames": vlanname}
        url = 'http://'+self.serverip+'/ark/resourcePool/netResource/vlan/delVlan.do'
        self.s.post(url,data = data,cookies = self.cookies)
        
    #@查询vlan
    def query_vlan(self,li):
        vlanid = li
        url = 'http://'+self.serverip+'/ark/resourcePool/netResource/vlan/query.do?_=1553671525358'
        re = self.s.get(url)
        re_json = json.loads(re.text)
        return (str(re_json['data']))

#test = vlanresource("192.168.60.200")
#test.add_vlan("8,vlan8,100,测试创建")
#re = test.query_vlan("8")
#print(re)
#test.del_vlan("8,vlan8")
#re = test.query_vlan("8")
#print(re)
        
