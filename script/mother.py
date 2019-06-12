#coding:utf-8
import requests
import json
import time
from requests_toolbelt import MultipartEncoder
import os
import warnings
warnings.simplefilter('ignore', ResourceWarning)

class mother(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies
        
    #@添加母盘
    def add_mother(self,li):
        data = json.loads(li)
        mother_data={"uidvmimgid":"",
                     "strimgname": "自定义母盘",
                     "strostype": "os_Win7",
                     "strdesc": "脚本创建母盘",
                     "irds": 0,
                     "icpunum": 2,
                     "imemorycapacity": 2048,
                     "idiskcapacity": 30,
                     "iattachdisk": "",
                     "strsoundhw": "all",
                     "icdromisoid": "",
                     "ivlan": 2,
                     "strmgtname": "mgt0",
                     "iifvirtio": 0,
                     "iisoinfoid": "",
                     "iuefistart": 2}
        
        for key in data.keys():
            mother_data[key] = data[key]
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/insertVMImg.do'
        self.s.post(url,data=mother_data,cookies=self.cookies)
        
    #@导入母盘
    def import_mother(self,li):
        li = li.split(",")
        motherboardname = li[0]
        motherboardfile = li[1]
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/queryVMImgList.do?_=1543218042010'
        re = self.s.get(url,cookies=self.cookies)
        re = json.loads(re.text)["data"]
        for vmimg in re:
            if motherboardname == vmimg['strimgname']:
                vmimgid = vmimg['uidvmimgid']
            else:
                continue
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/uploadVMImg'    
        headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                
                 }
        
        m = MultipartEncoder(
            fields={
                'imgid':vmimgid,
                'upload_strimgname':motherboardname,
                'filename':'' ,
                'realfilename':vmimgid+'.img',
                'vmimgfile':(os.path.basename(motherboardfile),open(motherboardfile,'rb'),'application/octet-stream')
                },
                boundary = '----WebKitFormBoundaryC2q39TRhaXlUIRyp'
            )
        headers['Content-Type'] = m.content_type
        self.s.post(url,cookies=self.cookies,headers=headers,data=m)

    #@删除母盘
    def delete_mother(self,li):
        li = li.split(",")
        motherboardname = li[0]
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/queryVMImgList.do?_=1543218042010'
        re = self.s.get(url,cookies=self.cookies)
        re = json.loads(re.text)["data"]
        for vmimg in re:
            if motherboardname == vmimg['strimgname']:
                vmimgid = vmimg['uidvmimgid']
            else:
                continue
        del_motherurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/deleteVMImg.do'
        del_data = {'uidvmimgid':vmimgid}
        self.s.post(del_motherurl,cookies=self.cookies,data=del_data)

    #@查询母盘
    def query_mother(self,li):
        li = li.split(",")
        motherboardname = li[0]
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/queryVMImgList.do?_=1543218042010'
        re = self.s.get(url,cookies=self.cookies)
        re = json.loads(re.text)["data"]
        for vmimg in re:
            if motherboardname == vmimg['strimgname']:
                 return str(vmimg)
        

#mother = mother('192.168.60.200')
#mother.import_mother("测试母盘,files\\1-win7-x64-60G-auto.rar")
#print(re)
