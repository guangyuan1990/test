#coding:utf-8
import requests
import json
import time
import os
from requests_toolbelt import MultipartEncoder

import warnings
warnings.simplefilter('ignore', ResourceWarning)

class template(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies
        
    #@母盘创建模板
    def creat_template(self,li):
        li = li.split(",")
        motherboardname = li[0]
        templatename = li[1]
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/queryVMImgList.do?_=1543218042010'
        re = self.s.get(url,cookies=self.cookies)
        re = json.loads(re.text)["data"]
        for vmimg in re:
            if motherboardname in str(vmimg):
                vmimgid = vmimg['uidvmimgid']
                strostype = vmimg['strostype']
                strmgtname = vmimg['strmgtname']
                iuefistart = vmimg['iuefistart']
                idiskcapacity = vmimg['idiskcapacity']
                icpunum = vmimg['icpunum']
                imemorycapacity = vmimg['imemorycapacity']
                iifvirtio = vmimg['iifvirtio']
            else:
                continue
        data ={
           'uidvmtemplateid':'', 
           'strtemplatename': templatename,
           'stroskey':strostype,
           'strdesc': '母盘创建模板',
           'icpunum': icpunum,
           'imemorycapacity': imemorycapacity,
           'idiskcapacity': idiskcapacity,
           'iattachdisk': '',
           'strsoundhw': 'all',
           'uidvmimgid': vmimgid,
           'uidbasevmid': '',
           'basecreatecopyuidid': '',
           'ivlan': '',
           'strmgtname': strmgtname,
           'uidcomputeresourcepoolid': 'systemdefaultpool',
           'iifvirtio': iifvirtio,
           'iuefistart': iuefistart,
           'uidfolderid': '',
           'icreatetype': 0,
           'irds': 0
           }
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/saveVmTemplate.do'
        self.s.post(url,cookies=self.cookies,data=data)

    #@查询模板
    def query_template(self,li):
        li = li.split(",")
        templatename = li[0]
        searchdata = {'searchType': 'strtemplatename','searchValue': templatename}
        searchurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/queryVmTemplateList.do'
        re = self.s.post(searchurl,cookies=self.cookies,data=searchdata)
        return re.text

    #@虚拟机创建模板
    def vm_template(self,li):
        li = li.split(",")
        vmname = li[0]
        templatename = li[1]
        searchvmurl = 'http://'+self.serverip+'/ark/cloud/desktop/queryVmList.do?irds=0'
        searchvmdata = {"searchType": "strvmname","searchValue": vmname,"_": "1543313387455"}
        re_vm = self.s.post(searchvmurl,cookies=self.cookies,data=searchvmdata)
        re_vm_json = json.loads(re_vm.text)
        vmid = re_vm_json['data'][0]['id']
        strostype = re_vm_json['data'][0]['stroskey']
        icpunum = re_vm_json['data'][0]['icpunum']
        imemorycapacity = re_vm_json['data'][0]['imemorycapacity']
        idiskcapacity = re_vm_json['data'][0]['idiskcapacity']
        strmgtname = re_vm_json['data'][0]['strmgtname']
        iifvirtio = re_vm_json['data'][0]['iifvirtio']
        iuefistart = re_vm_json['data'][0]['iuefistart']
        data ={
           'uidvmtemplateid':'', 
           'strtemplatename': templatename,
           'stroskey':strostype,
           'strdesc': '虚拟机创建模板',
           'icpunum': icpunum,
           'imemorycapacity': imemorycapacity,
           'idiskcapacity': idiskcapacity,
           'iattachdisk': '',
           'strsoundhw': 'all',
           'uidvmimgid': '',
           'uidbasevmid': vmid,
           'basecreatecopyuidid': '',
           'ivlan': '',
           'strmgtname': strmgtname,
           'uidcomputeresourcepoolid': 'systemdefaultpool',
           'iifvirtio': iifvirtio,
           'iuefistart': iuefistart,
           'uidfolderid': '',
           'icreatetype': 0,
           'irds': 0
           }
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/saveVmTemplate.do'
        self.s.post(url,cookies=self.cookies,data=data)
        
    #@删除模板
    def delete_template(self,li):
        li = li.split(",")
        templatename = li[0]
        searchdata = {'searchType': 'strtemplatename','searchValue': templatename}
        searchurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/queryVmTemplateList.do'
        re = self.s.post(searchurl,cookies=self.cookies,data=searchdata)
        re_json = json.loads(re.text)
        tempalteid = re_json['data'][0]['id']
        del_templateurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/deleteVmTemplate.do'
        del_templatedata = {'uidvmtemplateid':tempalteid }
        self.s.post(del_templateurl,cookies=self.cookies,data=del_templatedata)

    #@复制模板
    def copy_template(self,li):
        li = li.split(",")
        oldname = li[0]
        templatename = li[1]
        searchdata = {'searchType': 'strtemplatename','searchValue': oldname}
        searchurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/queryVmTemplateList.do'
        re = self.s.post(searchurl,cookies=self.cookies,data=searchdata)
        re_json = json.loads(re.text)
        tempalteid = re_json['data'][0]['id']
        strostype = re_json['data'][0]['stroskey']
        icpunum = re_json['data'][0]['icpunum']
        imemorycapacity = re_json['data'][0]['imemorycapacity']
        idiskcapacity = re_json['data'][0]['idiskcapacity']
        strmgtname = re_json['data'][0]['strmgtname']
        iifvirtio = re_json['data'][0]['iifvirtio']
        iuefistart =re_json['data'][0]['iuefistart']
        data ={
           'uidvmtemplateid':'', 
           'strtemplatename': templatename,
           'stroskey':strostype,
           'strdesc': '虚拟机创建模板',
           'icpunum': icpunum,
           'imemorycapacity': imemorycapacity,
           'idiskcapacity': idiskcapacity,
           'iattachdisk': '',
           'strsoundhw': 'all',
           'uidvmimgid': '',
           'uidbasevmid': '',
           'basecreatecopyuidid': tempalteid,
           'ivlan': '',
           'strmgtname': strmgtname,
           'uidcomputeresourcepoolid': 'systemdefaultpool',
           'iifvirtio': iifvirtio,
           'iuefistart': iuefistart,
           'uidfolderid': '',
           'icreatetype': 0,
           'irds': 0
           }
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/saveVmTemplate.do'
        self.s.post(url,cookies=self.cookies,data=data)

    #@维护模板
    def maintaintemplate(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/maintainVMTemplate.do'
        data = {'uidvmtemplateid': templateid}
        self.s.post(url,cookies=self.cookies,data=data)

    #@取消维护模板
    def canceltemplate(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/cancelVmTemplate.do'
        data = {'uidvmtemplateid': templateid}
        self.s.post(url,cookies=self.cookies,data=data)
        
    #@发布模板
    def public_template(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/publishTemplate.do'
        data = {'uidvmtemplateid': templateid,'target': 1,'buildSeedData': 0}
        self.s.post(url,cookies=self.cookies,data=data)

    #@启动模板
    def start_template(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/startVMTemplate.do'
        data = {'uidvmtemplateid': templateid}
        self.s.post(url,cookies=self.cookies,data=data)

    #@停止模板
    def stop_template(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/stopVMTemplate.do'
        data = {'uidvmtemplateid': templateid}
        self.s.post(url,cookies=self.cookies,data=data)

    #@模板做种
    def build_seed(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        templatename = re_json['data'][0]['strtemplatename']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/buildBTSeed.do'
        data = {
            'uidvmtemplateid': templateid,
            'vmtemplatename': templatename,
            'strdiskfilename': templateid+'.img'
               }
        self.s.post(url,cookies=self.cookies,data=data)
        
    #@删除模板种子
    def remove_seed(self,li):
        re = self.query_template(li)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        templatename = re_json['data'][0]['strtemplatename']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/removeBTSeed.do'
        data = {'uidvmtemplateid': templateid,'vmtemplatename': templatename}
        self.s.post(url,cookies=self.cookies,data=data)

    #@文件导入创建模板
    def file_template(self,li):
        data = json.loads(li)
        templatedata ={
           'uidvmtemplateid':'', 
           'strtemplatename': 'win7-x64-60G',
           'stroskey':'os_Win7',
           'strdesc': '文件导入创建模板',
           'icpunum': 2,
           'imemorycapacity': 2048,
           'idiskcapacity': 60,
           'iattachdisk': '',
           'strsoundhw': 'all',
           'uidvmimgid': '',
           'uidbasevmid': '',
           'basecreatecopyuidid': 'win7_x64_60G_auto',
           'ivlan': '',
           'strmgtname': 'mgt0',
           'uidcomputeresourcepoolid': 'systemdefaultpool',
           'iifvirtio': 0,
           'iuefistart': 2,
           'uidfolderid': '',
           'icreatetype': 1,
           'irds': 0
           }
        
        for key in data.keys():
            templatedata[key] = data[key]
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/saveVmTemplate.do'
        self.s.post(url,cookies=self.cookies,data=templatedata)

    #@导入模板
    def import_template(self,li):
        li = li.split(",")
        templatename = li[0]
        templatefile = li[1]
        re = self.query_template(templatename)
        re_json = json.loads(re)
        templateid = re_json['data'][0]['uidvmtemplateid']
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/uploadVMTemplate'
        headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                
                 }
        m = MultipartEncoder(
            fields={
                'uidvmtemplateid':templateid,
                'filename':'' ,
                'realfilename':templateid+'.img',
                'vmimgfile':(os.path.basename(templatefile),open(templatefile,'rb'),'application/octet-stream')
                },
                boundary = '------WebKitFormBoundary6h9JORli593MkwVc'
            )
        headers['Content-Type'] = m.content_type
        self.s.post(url,cookies=self.cookies,headers=headers,data=m)
        
#tm = template("192.168.60.200")
#re = tm.query_template("测试模板")
#print(re)
