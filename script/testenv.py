#coding:utf-8
import requests
import json
import time
from requests_toolbelt import MultipartEncoder

import warnings
warnings.simplefilter('ignore', ResourceWarning)

class testenv(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies

    def add_mother(self,li):
        data = li
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
        url = 'http://'+self.serverip+'/ark/cloud/desktop/vmimg/queryVMImgList.do?_=1543218042010'
        self.s.get(url,cookies=self.cookies)

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
                'vmimgfile':(motherboardfile,open(motherboardfile,'rb'),'application/octet-stream')
                },
                boundary = '----WebKitFormBoundaryC2q39TRhaXlUIRyp'
            )
        headers['Content-Type'] = m.content_type
        self.s.post(url,cookies=self.cookies,headers=headers,data=m)

    def creat_vm(self,li):
        li = li.split(",")
        vmname = li[0]
        templatename = li[1]
        usename = li[2]
        searchdata = {'searchType': 'strtemplatename','searchValue': templatename}
        searchurl = 'http://'+self.serverip+'/ark/cloud/desktop/vmtemplate/queryVmTemplateList.do'
        re = self.s.post(searchurl,cookies=self.cookies,data=searchdata)
        re_json = json.loads(re.text)
        tempalteid = re_json['data'][0]['id']
        tempaltestatus = re_json['data'][0]['irunstatus']
        searchuseurl = 'http://'+self.serverip+'/ark//account/user/query.do?searchParam={"searchType":"realOrUsername","searchValue":"'+usename+'"}&_=1543309277410'
        re_use = self.s.get(searchuseurl)
        re_use_json = json.loads(re_use.text)
        useid = re_use_json['data'][0]['uidUserId']
        vmdata = {
        "uidvmid": "",
        "edit_old_uidvmtemplateid":"", 
        "edit_old_strtemplatename": "",
        "irds": 0,
        "strvmname": vmname,
        "strdesc":"脚本创建测试虚拟机", 
        "strgroupid":"", 
        "uidvmpoolid": "",
        "uidcomputeresourcepoolid": "systemdefaultpool",
        "inettype": 1,
        "idhcp": 1,
        "strvmip":"", 
        "strvmmask": "255.255.255.0",
        "strvmgateway": "",
        "dns": 1,
        "strvmdns1": "",
        "strvmdns2": "",
        "basecreate": 1,
        "uidvmtemplateid": tempalteid,
        "basecreatecopyuidid": "",
        "basecreate_copy_strvmname":"", 
        "strosname": "Windows 7",
        "icpunum": 2,
        "imemorycapacity": 2048,
        "field_idiskcapacity": 60,
        "field_idiskcapacity_desc": "60GB",
        "iattachdisk":"", 
        "field_uiduserid": usename,
        "uiduserid": useid,
        "strsoundhwhda": "hda",
        "strsoundhwac97": "ac97",
        "strsoundhw": "all",
        "strnetcard": "virtio",
        "ivlan":"", 
        "strmgtname": "mgt0",
        "strdevtosynrvm":"", 
        "iifvirtio": 1,
        "iuefistart": 2,
        "strsoundhw": "all",
        "strnetcard": "virtio",
        "uidvmtemplateid": tempalteid,
        "uidvmimgid": ""
             }
        addvm_url = 'http://'+self.serverip+'/ark//cloud/desktop/saveVm.do'
        self.s.post(addvm_url,cookies=self.cookies,data=vmdata)

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

    def query(self,li):
        groupname = li
        url = 'http://'+self.serverip+'/ark/account/organization/query.do'
        res = self.s.get(url)
        res_json = json.loads(res.text)
        for group in res_json:
          if group["strOrgName"] == groupname:
                return str(group)
            
    def add_group(self,li):
        li = li.split(",")
        father_group = li[0]
        new_group = li[1]
        group = self.query(father_group).replace('\'','\"').replace('None','0')
        res_json = json.loads(group)
        groupid = res_json['uidOrgId']
        url = 'http://'+self.serverip+'/ark//account/organization/0'
        data = {'text': new_group,'uidOrgParentId': groupid}
        self.s.post(url,data=data,cookies=self.cookies)
    
    def creat_multiuser(self,li):
        li = li.split(",")
        username = li[0]
        password = li[1]
        groupname = li[2]
        privatedisk = li[3]
        startnum = li[4]
        num = li[5]
        group = self.query(groupname).replace('\'','\"').replace('None','0')
        res_json = json.loads(group)
        groupid = res_json['uidOrgId']
        data = {
            'strUserName': username,
            'strPwd': password,
            'strRealName': '',
            'isBatch': 'true',
            'batchStartNumber': startnum,
            'batchCount': num,
            'uidOrgId': groupid,
            'strPosition': '',
            'icreateprivateDisk': 1,
            'iDisklimit': 20,
            'inetfoldertype': 0,
            'strnetfolderpath':'' ,
            'inetfolderauth': 2,
            'strnetfolderuser':'', 
            'strnetfolderpwd': '',
            'striscsiserver': '',
            'striscsitarget':'', 
            'striscsilun': '',
            'ichap': 0,
            'striscsiuser': '',
            'striscsipwd': '',
            'strfcsunlun': 'fibre',
            'dtExpireTime': '',
            'strEmail': '',
            'strMobiePhone': '',
            'strTelePhone': '',
            'strQq':'', 
            'strDesc': ''
            }
        if privatedisk=='0':
            data['icreateprivateDisk'] = 0
            data['iDisklimit'] = 0
        else:
            data['icreateprivateDisk'] = 1
            data['iDisklimit'] = privatedisk
        url = 'http://'+self.serverip+'/ark//account/user/add'
        self.s.post(url,data=data,cookies=self.cookies)

    #@初始化测试环境
    def testenv_start(self,li):
        li = li.split(",")
        mothername = li[0]
        filepath = li[1]
        templatename = li[2]
        vmname = li [3]
        username = li[4]
        password = li[5]
        self.add_mother({"strimgname": mothername})
        self.import_mother(mothername+","+filepath)
        self.creat_template(mothername+","+templatename)
        self.add_group("root,测试分组")
        self.creat_multiuser(usename+","+password+","+"测试分组"+","+'20'+","+"01"+","+"5")
        
