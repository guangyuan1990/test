#coding:utf-8
import requests
import json
import time
from requests_toolbelt import MultipartEncoder

import warnings
warnings.simplefilter('ignore', ResourceWarning)

class publicdir(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    #@添加默认共享目录
    def add_publicdir(self,li):
        dirname = li
        data = {'id': '/arkdata/hd0/home/public/','dirName': dirname}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/makeDir.do'
        self.s.post(url,data=data,cookies=self.cookies)

    #@添加模板共享目录
    def add_templatedir(self,li):
        dirname = li
        data = {'id': '/arkdata/hd0/home/template_share/','dirName': dirname}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/makeDir.do'
        self.s.post(url,data=data,cookies=self.cookies)

    #@查询默认共享目录
    def query_publicdir(self,li):
        dirname = li
        data = {'id': '/arkdata/hd0/home/public/','getDir': 'true'}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/queryNode.do'
        re = self.s.post(url,data=data,cookies=self.cookies)
        re_json = json.loads(re.text)
        for pdir in re_json:
            if dirname==pdir["name"]:
                return str(pdir)


    #@查询模板共享目录
    def query_templatedir(self,li):
        dirname = li
        data = {'id': '/arkdata/hd0/home/template_share/','getDir': 'true'}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/queryNode.do'
        re = self.s.post(url,data=data,cookies=self.cookies)
        re_json = json.loads(re.text)
        for pdir in re_json:
            if dirname==pdir["name"]:
                return str(pdir)

    #@查询默认共享目录文件
    def query_pubfile(self,li):
        dirname = li
        data ={'id': '/arkdata/hd0/home/public/','getDir': 'false'}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/queryNode.do'
        if dirname=="默认共享目录":
            re = self.s.post(url,data=data,cookies=self.cookies)
        else:
            data["id"]=data["id"]+dirname+"/"
            re = self.s.post(url,data=data,cookies=self.cookies)
        re_json = json.loads(re.text)
        filedict = {}
        for file in re_json:
            filedict[file["name"]]=file["filesize"]
        return str(filedict)#返回{文件名：文件大小}形式的字典

    def query_templateid(self,li):
        dirname = li
        data = {'id': '/arkdata/hd0/home/template_share/','getDir': 'true'}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/queryNode.do'
        re = self.s.post(url,data=data,cookies=self.cookies)
        re_json = json.loads(re.text)
        for pdir in re_json:
            if dirname==pdir["name"]:
                return pdir["id"]

    #@查询模板共享目录文件
    def query_templatefile(self,li):
        dirname = li
        data ={'id': '/arkdata/hd0/home/template_share/','getDir': 'false'}
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/queryNode.do'
        if dirname=="模板共享目录":
            re = self.s.post(url,data=data,cookies=self.cookies)
        else:
            data["id"]=self.query_templateid(dirname)
            re = self.s.post(url,data=data,cookies=self.cookies)
        re_json = json.loads(re.text)
        filedict = {}
        for file in re_json:
            filedict[file["name"]]=file["filesize"]
        return str(filedict)#返回{文件名：文件大小}形式的字典

    #@上传文件到默认共享目录
    def upfile_public(self,li):
        li = li.split(",")
        dirname = li[0]
        filename = li[1]
        url = "http://"+self.serverip+"/ark/appCenter/fileManager/uploadFile"
        headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                
                 }
        if dirname =="默认共享目录":
            dirname = "/arkdata/hd0/home/public/"
        else:
            dirname = "/arkdata/hd0/home/public/"+dirname+"/"
        m = MultipartEncoder(
            fields={
                'id':dirname,
                'uploadFile':(filename,open("files/"+filename,'rb'),'application/octet-stream')
                },
                boundary = '------WebKitFormBoundaryE2EJB0hZt0jQweej'
            )
        headers['Content-Type'] = m.content_type
        self.s.post(url,cookies=self.cookies,headers=headers,data=m)

    #@上传文件到模板共享目录
    def upfile_templatedir(self,li):
        li = li.split(",")
        dirname = li[0]
        filename = li[1]
        url = "http://"+self.serverip+"/ark/appCenter/fileManager/uploadFile"
        headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                
                 }
        if dirname =="模板共享目录":
            dirname = "/arkdata/hd0/home/template_share/"
        else:
            dirname = self.query_templateid(dirname)
        m = MultipartEncoder(
            fields={
                'id':dirname,
                'uploadFile':(filename,open("files/"+filename,'rb'),'application/octet-stream')
                },
                boundary = '------WebKitFormBoundaryE2EJB0hZt0jQweej'
            )
        headers['Content-Type'] = m.content_type
        self.s.post(url,cookies=self.cookies,headers=headers,data=m)
        
    #@删除默认共享目录文件
    def del_publicfile(self,li):
        li = li.split(",")
        dirname = li[0]
        filename = li[1]
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/deleteDirOrFile.do'
        data={"id": "/arkdata/hd0/home/public/","name": filename}
        if dirname=="默认共享目录":
            data["id"] = data["id"]+filename
        else:
            data["id"] = data["id"]+dirname+"/"+filename
        self.s.post(url,data=data,cookies=self.cookies)

    #@删除模板共享目录文件
    def del_templatefile(self,li):
        li = li.split(",")
        dirname = li[0]
        filename = li[1]
        url = 'http://'+self.serverip+'/ark/appCenter/fileManager/deleteDirOrFile.do'
        data={"id": "/arkdata/hd0/home/template_share/","name": filename}
        if dirname=="模板共享目录":
            data["id"] = data["id"]+filename
        else:
            data["id"] = self.query_templateid(dirname)+filename
        self.s.post(url,data=data,cookies=self.cookies)
        
pd = publicdir("192.168.60.200")
#re = pd.query_pubfile("yhg")
#re = pd.query_pubfile("newDir2")
re = pd.query_templatefile("test")
#pd.upfile_public("yhg,keybroead_socketserver.exe")
#pd.upfile_templatedir("newDir1,keybroead_socketserver.exe")
#pd.del_publicfile("newDir2,base.jpg")
#pd.del_templatefile("newDir1,auto_test.exe")
print(re)
           
