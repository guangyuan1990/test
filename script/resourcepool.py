#coding:utf-8
import requests
import json
import time

class resourcepool(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies
        
    #@添加计算机资源池
    def add_resourcepool(self,li):
        li = li.split(",")
        name = li[0]
        desc = li[1]
        poliy = li[2]
        if poliy=="默认":
            strategy="0_0_0_0"
        else:
            first,second,thrid=0,0,0
            poliy = poliy.split("+")
            for i in poliy:
                if i == "会话数":
                    first = 1
                elif i=="cpu":
                    second = 1
                elif i=="内存":
                    thrid = 1
            strategy = str(first)+"_"+str(second)+"_"+str(thrid)+"_"+"0"
        data = {"name":name,"desc":desc,"strategy":strategy}
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/addComputeResourcePool.do"
        self.s.post(url,data=data,cookies=self.cookies)
        
    def query(self,li):
        name = li
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/queryComputeResourcePool.do?_=1548725379922"
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for pool in re_json["data"]:
            if pool["strresourcepoolname"] == name:
                return pool["uidresourcepoolid"]
            
    #@查询计算机资源池
    def query_resourcepool(self,li):
        name = li
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/queryComputeResourcePool.do?_=1548725379922"
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for pool in re_json["data"]:
            if pool["strresourcepoolname"] == name:
                return str(pool)
            
    #@删除计算机资源池
    def del_resourcepool(self,li):
        li = li.split(",")
        name = li[0]
        stopvm =li[1]
        poolid = self.query(name)
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/delComputeResourcePool.do"
        data = {"uidresourcepoolid":poolid,"stopAllVM":stopvm}
        self.s.post(url,data=data,cookies=self.cookies)

    #@编辑计算机资源池
    def edit_resourcepool(self,li):
        li = li.split(",")
        oldname = li[0]
        newname = li[1]
        desc = li[2]
        poliy = li[3]
        if poliy=="默认":
            strategy="0_0_0_0"
        else:
            first,second,thrid=0,0,0
            poliy = poliy.split("+")
            for i in poliy:
                if i == "会话数":
                    first = 1
                elif i=="cpu":
                    second = 1
                elif i=="内存":
                    thrid = 1
            strategy = str(first)+"_"+str(second)+"_"+str(thrid)+"_"+"0"
        poolid = self.query(oldname)
        data = {
            "uidresourcepoolid": poolid,
            "strresourcepoolname": newname,
            "strdesc":desc, 
            "strategy": strategy
               }
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/editComputeResourcePool.do"
        self.s.post(url,data=data,cookies=self.cookies)

    def query_nodeid(self,li):
        nodeip = li
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/queryComputeNode.do?_=1548725379952"
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for node in re_json["data"]:
            if node["strip"] == nodeip:
                return node["uiddomainid"]
            
    #@计算节点查询
    def query_computernode(self,li):
        nodeip = li
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/queryComputeNode.do?_=1548725379952"
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for node in re_json["data"]:
            if node["strip"] == nodeip:
                return str(node)

    #@配置节点
    def join_node(self,li):
        li = li.split(",")
        nodeip = li[0]
        pool = li[1]
        nodeid = self.query_nodeid(nodeip)
        poolid = self.query(pool)
        data = {
               "uiddomainids[]":nodeid ,
               "uidresourcepoolid": poolid
               }
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/editComputeNodeResourcePool.do"
        self.s.post(url,data=data,cookies=self.cookies)

    #@移除资源池节点
    def del_node(self,li):
        li = li.split(",")
        nodeip = li[0]
        stopvm = li[1]
        nodeid = self.query_nodeid(nodeip)
        data = {
              "uiddomainids[]": nodeid,
              "strips": "",
              "stopAllVM": stopvm
              }
        url = "http://"+self.serverip+"/ark/resourcePool/computeResource/delComputeNode.do"
        self.s.post(url,data=data,cookies=self.cookies)
        
#pool = resourcepool("192.168.60.200")
#pool.del_resourcepool('测试默认资源池')
#pool.edit_resourcepool("测试默认资源池,编辑资源池名称,修改了描述,会话数+cpu+内存")
#re = pool.query_resourcepool("测试默认资源池")
#print(re)
#print(re_param in re)

#pool.add_resourcepool("测试资源池,测试创建,默认")
#pool.add_resourcepool("测试资源池1,测试创建2,会话数+cpu+内存")
#poolid = pool.query("测试资源池")
#print(poolid)
#pool.del_resourcepool("测试资源池,1")
                    
            
