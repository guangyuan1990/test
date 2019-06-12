#coding:utf-8
import requests
import json
import time

class terminaldev(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    def query_devid(self,name):
        data = {'params':'{"searchType":"strdevname","searchValue":"'+name+'"}'}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/query.do'
        re = self.s.post(url,data=data,cookies= self.cookies)
        re_json = json.loads(re.text)
        for dev in re_json["data"]:
            if name == dev["strdevname"]:
                return dev["uidid"]
            
    def query_userid(self,user):
        searchuseurl = 'http://'+self.serverip+'/ark//account/user/query.do?searchParam={"searchType":"realOrUsername","searchValue":"'+user+'"}&_=1543309277410'
        re_use = self.s.get(searchuseurl)
        re_use_json = json.loads(re_use.text)
        useid = re_use_json['data'][0]['uidUserId']
        return useid

    #@查询终端
    def query_terminal(self,li):
        name = li
        data = {'params':'{"searchType":"strdevname","searchValue":"'+name+'"}'}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/query.do'
        re = self.s.post(url,data=data,cookies= self.cookies)
        re_json = json.loads(re.text)
        for dev in re_json["data"]:
            if name == dev["strdevname"]:
                return str(dev)

    #@开机终端
    def start_terminal(self,li):
        name = li
        devid = self.query_devid(name)
        data = {'uidid': devid}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/operateStartup'
        self.s.post(url,data=data)

    #@关机终端
    def stop_terminal(self,li):
        name = li
        devid = self.query_devid(name)
        data = {'uidid': devid}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/operateShutdown'
        self.s.post(url,data=data)
        
    #@断开终端
    def disconnent(self,li):
        name = li
        devid = self.query_devid(name)
        data = {'uidid': devid}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/operateDisconnect'
        self.s.post(url,data=data)
        
    #@绑定用户
    def bind_user(self,li):
        li = li.split(',')
        terminalname = li[0]
        username = li[1]
        userid = self.query_userid(username)
        terminalid = self.query_devid(terminalname)
        data = {'terminalId': terminalid,'userids[]': userid}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/saveAccountbind.do'
        self.s.post(url,data=data)

    #@重命名终端
    def rename_terminal(self,li):
        li = li.split(',')
        oldname = li[0]
        newname = li[1]
        data = {'params':'{"searchType":"strdevname","searchValue":"'+oldname+'"}'}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/query.do'
        re = self.s.post(url,data=data,cookies= self.cookies)
        re_json = json.loads(re.text)
        for dev in re_json["data"]:
            if oldname == dev["strdevname"]:
                devid = dev["uidid"]
                devmac = dev["strmac"]
        rename_data = {"uidid": devid,
                       "strdevname": newname,
                       "strmac": devmac}
        rename_url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/rename.do'
        self.s.post(rename_url,data=rename_data)

    #@删除终端
    def del_terminal(self,li):
        name = li
        devid = self.query_devid(name)
        data = {'uidid': devid}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/operateBatchDelete'
        self.s.post(url,data=data)

    #@终端网络配置
    def net_terminal(self,li):
        li = li.split(",")
        name = li[0]
        net = li[1]
        ip = li[2]
        strsubnetmask = li[3]
        strgateway = li[4]
        dns1 = li[5]
        dns2 = li[6]
        data = {'params':'{"searchType":"strdevname","searchValue":"'+name+'"}'}
        url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/query.do'
        net_data = {
               "uidid": "",
               "idhcp": 1,
               "strmac": "",
               "strip": "",
               "strstartip": "",
               "strendip": "",
               "strsubnetmask": "",
               "strgateway": "",
               "strdns1": "",
               "strdns2":"" }
        re = self.s.post(url,data=data,cookies= self.cookies)
        re_json = json.loads(re.text)
        for dev in re_json["data"]:
            if name == dev["strdevname"]:
                net_data["uidid"] = dev["uidid"]
                net_data["strmac"] = dev["strmac"]
        
        if net == "自动":
            net_data["idhcp"]=1
        else:
            net_data["idhcp"]=0
        net_data["strip"]=ip
        net_data["strsubnetmask"]=strsubnetmask
        net_data["strgateway"]=strgateway
        net_data["strdns1"]=dns1
        net_data["strdns2"]=dns2
        net_url = 'http://'+self.serverip+'/ark//physicalDevice/terminalDev/operateNetsetting.do'
        self.s.post(net_url,data=net_data)

    
        
#dev = terminaldev('192.168.60.200')
#re = dev.query_terminal("linux-dev")
#re = dev.query_userid('test1')
#dev.bind_user("linux-dev,yhg001")
#dev.rename_terminal("linux-dev2,linux-dev")
#dev.net_terminal("kk04,自动,192.168.3.107,255.255.255.0,192.168.3.254,8.8.8.8,114.114.114.114")
#print(re)
    
    
