#coding:utf-8
import requests
import json
import time

class authmanager(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    def query_sortid(self,sortname):
        url = "http://"+self.serverip+"/ark//appCenter/auth/queryAllAuth.do?_=1559011805787"
        re = self.s.get(url,cookies=self.cookies)
        re_json = json.loads(re.text)
        for sort in re_json["data"]:
            if sort["strisoname"] == sortname:
                return(sort["uidisoinfoid"])

    def query_vmid(self,vmname):
        querydata = {'searchType': 'strvmname','searchValue': vmname,'_': '1543978006678'}
        queryurl = 'http://'+self.serverip+'/ark/cloud/desktop/queryVmList.do?irds=0'
        re = self.s.post(queryurl,cookies=self.cookies,data=querydata)
        re_json = json.loads(re.text)
        return(re_json["data"][0]["id"])
        
    def query_vmgroupid(self,vmgroup):
        url = "http://"+self.serverip+"/ark//cloud/desktop/vmGroup/queryAllVmGroups.do?_=1559022497136"
        re = self.s.get(url,cookies=self.cookies)
        re_json = json.loads(re.text)
        for group in re_json["data"]:
            if group["strgroupname"] == vmgroup:
                return group["strgroupid"]
        
    #@查询软件授权
    def query_auth(self,li):
        sortname = li
        authdict = {"vm":[],"vmgroup":[]}
        url = "http://"+self.serverip+"/ark//appCenter/auth/queryAllAuth.do?_=1559011805787"
        re = self.s.get(url,cookies=self.cookies)
        re_json = json.loads(re.text)
        for sort in re_json["data"]:
            if sort["strisoname"] == sortname:
                for vm in sort["vmList"]:
                    authdict["vm"].append(vm["strvmname"])
                for vmgroup in sort["vmGroupList"]:
                    authdict["vmgroup"].append(vmgroup["strgroupname"])
        return(str(authdict))
                
    #@添加虚拟机授权
    def add_vmauth(self,li):
        data = {"uidisoinfoids":"","itype":2}
        li = li.split(",")
        sortname = li[0]
        vmlist = li[1:]
        sortid = self.query_sortid(sortname)
        data["uidisoinfoids"] = '{"'+sortid+'":"'
        for vm in vmlist:
            vmid = self.query_vmid(vm)
            data["uidisoinfoids"]=data["uidisoinfoids"]+vmid+','
        data["uidisoinfoids"]=data["uidisoinfoids"]+'"}'
        url = "http://"+self.serverip+"/ark//appCenter/auth/updateAuth.do"
        self.s.post(url,data=data,cookies=self.cookies)

    #@添加虚拟机组授权
    def add_vmgroupauth(self,li):
        data = {"uidisoinfoids":"","itype":1}
        li = li.split(",")
        sortname = li[0]
        grouplist = li[1:]
        sortid = self.query_sortid(sortname)
        data["uidisoinfoids"] = '{"'+sortid+'":"'
        for vmgroup in grouplist:
            vmgroupid = self.query_vmgroupid(vmgroup)
            data["uidisoinfoids"]=data["uidisoinfoids"]+vmgroupid+','
        data["uidisoinfoids"]=data["uidisoinfoids"]+'"}'
        url = "http://"+self.serverip+"/ark//appCenter/auth/updateAuth.do"
        self.s.post(url,data=data,cookies=self.cookies)

    #@清除软件授权
    def clear_auth(self,li):
        data = {}
        sortname = li
        sortid = self.query_sortid(sortname)
        data["uidisoinfoids"] = sortid
        url = "http://"+self.serverip+"/ark//appCenter/auth/updateAuth.do"
        self.s.post(url,data=data,cookies=self.cookies)
        
#test=authmanager("192.168.180.200")
#test.add_vmauth("VmToolAndVmagent.iso,数据-大数据用户096")
#test.add_vmgroupauth("VmToolAndVmagent.iso,group")
#test.clear_auth("VmToolAndVmagent.iso")
#re = test.query_auth("VmToolAndVmagent.iso")
#print(re)
