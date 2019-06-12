#coding:utf-8
import requests
import json
import time

class assort(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    #@查询软件分类
    def assort_query(self,li):
        asname = li
        url = "http://"+self.serverip+"/ark/appCenter/assort/query.do"
        re = self.s.post(url,cookies=self.cookies)
        re_json = json.loads(re.text)
        for asl in re_json["data"]:
            if asl["strname"] == asname:
                return str(asl["softwaresubclassList"])
            

    #@查询分类下软件个数
    def sum_query(self,li):
        asname = li
        sort_sum = {}
        url = "http://"+self.serverip+"/ark/appCenter/assort/query.do"
        re = self.s.post(url,cookies=self.cookies)
        re_json = json.loads(re.text)
        for asl in re_json["data"]:
            sort_sum[asl["strname"]] = asl["softwarecount"]
            for sub in asl["softwaresubclassList"]:
                sort_sum[sub["strname"]] = sub["softwarecount"]
        return(str(sort_sum[asname]))

    #@新增软件分类
    def add_assort(self,li):
        li = li.split(",")
        asname = li[0]
        father_as = li[1]
        pid = {"系统软件":1,"应用软件":2,"驱动程序":3,"其它":4}
        data = {"strname":asname,"icategoryid":pid[father_as]}
        url = "http://"+self.serverip+"/ark/appCenter/assort/addSoftwaresubclass.do"
        self.s.post(url,data=data,cookies=self.cookies)

    #@删除子类
    def delete_class(self,li):
        li = li.split(",")
        asname = li[0]
        isdelete = li[1]
        sort_sum = {}
        url = "http://"+self.serverip+"/ark/appCenter/assort/query.do"
        re = self.s.post(url,cookies=self.cookies)
        re_json = json.loads(re.text)
        for asl in re_json["data"]:
            for sub in asl["softwaresubclassList"]:
                sort_sum[sub["strname"]] = sub["isubclassid"]
        cid = sort_sum[asname]
        data = {"isubclassid":cid}
        url = "http://"+self.serverip+"/ark/appCenter/assort/deleteSoftwaresubclass.do?isDelSoftware="+isdelete
        self.s.post(url,data=data,cookies=self.cookies)
        
#test = assort("192.168.180.200")
#test.add_assort("声卡驱动,驱动程序")
#test.add_assort("测试软件,其它")
#re=test.assort_query("运用软件")
#print(re)
