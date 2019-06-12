#coding:utf-8
import requests
import json
import time
import execjs

class node(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    #@查询服务器节点
    def query_node(self,li):
        serverip = li
        url = 'http://'+self.serverip+'/ark//dataCenter/general/queryNodes.do?_=1547535957353'
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for node in re_json['data']:
            if serverip == node["strip"]:
                return str(node)

    def jquery_node(self,li):
        serverip = li
        url = 'http://'+self.serverip+'/ark//dataCenter/general/queryNodes.do?_=1547535957353'
        re = self.s.get(url)
        re_json = json.loads(re.text)
        for node in re_json['data']:
            if serverip == node["strip"]:
                return node

    #@编辑服务器节点
    def edit_node(self,li):
        li = li.split(",")
        serverip = li[0]
        ibackup = li[1]
        istoredec = li[2]
        istore = li[3]
        icompute = li[4]
        idatabackup = li[5]
        node = jquery_node(serverip)
        nodeid = node["uiddomainid"]
        data = {
            'uiddomainid': nodeid,
            'ibackup': ibackup,
            'istoredcs':istoredcs ,
            'istore':istore ,
            'icompute': icompute,
            'idatabackup': idatabackup
               }
        url = 'http://'+self.serverip+'/ark//dataCenter/general/editNode.do'
        self.s.post(url,data=data,cookies=cookies)

  
#node =node('192.168.60.200')
#re = node.query_node("192.168.60.201")
#print(re)
