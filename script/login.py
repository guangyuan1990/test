#coding:utf-8
import requests
import json
import time
import execjs

class login(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        
    #@登陆管理平台    
    def login_manage(self,li):
        li = li.split(",")
        usename = li[0]
        password = li[1]
        with open("js/password.js") as f:
            jsData = f.read()
        pwcode = execjs.compile(jsData).eval('fnMixstr("admin","0000")')
        strpw = execjs.compile(jsData).eval('fnEncryptText("'+pwcode+'")')
        data = {"username":usename,"password":strpw,"checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        
