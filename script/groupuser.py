#coding:utf-8
import requests
import json
import time
import execjs

class groupuser(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies
        
    #@用户分组查询
    def query(self,li):
        groupname = li
        url = 'http://'+self.serverip+'/ark/account/organization/query.do'
        res = self.s.get(url)
        res_json = json.loads(res.text)
        for group in res_json:
          if group["strOrgName"] == groupname:
                return str(group)


    #@添加用户分组
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
        
    #@修改用户分组
    def replace_group(self,li):
        li = li.split(",")
        old_group = li[0]
        father_group = li[1]
        new_group = li[2]
        group = self.query(old_group).replace('\'','\"').replace('None','0')
        res_json = json.loads(group)
        old_groupid = res_json['uidOrgId']
        url = 'http://'+self.serverip+'/ark//account/organization/'+old_groupid
        group = self.query(father_group).replace('\'','\"').replace('None','0')
        res_json = json.loads(group)
        father_groupid = res_json['uidOrgId']
        data = {'_method':'PUT','text': new_group,'uidOrgParentId': father_groupid}
        #print(data)
        #print(url)
        self.s.put(url,data=data,cookies=self.cookies)

    #@删除用户分组
    def delete_group(self,li):
        li = li.split(",")
        groupname = li[0]
        group = self.query(groupname).replace('\'','\"').replace('None','0')
        res_json = json.loads(group)
        groupid = res_json['uidOrgId']
        url = 'http://'+self.serverip+'/ark//account/organization/'+groupid
        data = {'_method': 'DELETE'}
        self.s.delete(url,data=data,cookies=self.cookies)

    #@创建单个用户
    def creat_singleuser(self,li):
        li = li.split(",")
        username = li[0]
        password = li[1]
        groupname = li[2]
        privatedisk = li[3]
        group = self.query(groupname).replace('\'','\"').replace('None','0')
        res_json = json.loads(group)
        groupid = res_json['uidOrgId']
        data = {
            'strUserName': username,
            'strPwd': password,
            'strRealName': '',
            'batchStartNumber': 1,
            'batchCount': 8,
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

    #@创建多个用户
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

    #@查询用户
    def query_user(self,li):
        li = li.split(",")
        username = li[0]
        data = 'searchParam=%7B%22searchType%22:%22realOrUsername%22,%22searchValue%22:%22'+username+'%22%7D'
        url = 'http://'+self.serverip+'/ark//account/user/query.do?'+data+'&_=1547199716573'
        re = self.s.get(url)
        return(re.text)


    #@停用用户
    def disable_user(self,li):
        data = {'uidUserId': ''}
        if "," in li:
            for use in li.split(","):
                re = self.query_user(use)
                re_json = json.loads(re)
                url = 'http://'+self.serverip+'/ark//account/user/disable.do'
                for user in re_json['data']:
                    userid = user['uidUserId']
                    data['uidUserId'] = userid
                    self.s.post(url,data=data,cookies=self.cookies)
        else:
            re = self.query_user(li)
            re_json = json.loads(re)
            url = 'http://'+self.serverip+'/ark//account/user/disable.do'
            for user in re_json['data']:
                userid = user['uidUserId']
                data['uidUserId'] = userid
                self.s.post(url,data=data,cookies=self.cookies)

    #@启用用户
    def enable_user(self,li):
        data = {'uidUserId': ''}
        re = self.query_user(li)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/enable.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)

    #@删除用户
    def delete_user(self,li):
        data = {'uidUserId': ''}
        if "," in li:
            for use in li.split(","):
                re = self.query_user(use)
                re_json = json.loads(re)
                url = 'http://'+self.serverip+'/ark//account/user/delUsers.do'
                for user in re_json['data']:
                    userid = user['uidUserId']
                    data['uidUserId'] = userid
                    self.s.post(url,data=data,cookies=self.cookies)
        else:
            re = self.query_user(li)
            re_json = json.loads(re)
            url = 'http://'+self.serverip+'/ark//account/user/delUsers.do'
            for user in re_json['data']:
                userid = user['uidUserId']
                data['uidUserId'] = userid
                self.s.post(url,data=data,cookies=self.cookies)

    #@锁定用户
    def lock_user(self,li):
        data = {'uidUserId': ''}
        re = self.query_user(li)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/lock.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)

    #@解锁用户
    def unlock_user(self,li):
        data = {'uidUserId': ''}
        re = self.query_user(li)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/unlock.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)

    #@删除用户私有盘
    def del_pridisk(self,li):
        data = {'uidUserId': ''}
        re = self.query_user(li)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/deletePridisk.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)

    #@创建用户私有盘
    def creat_pridisk(self,li):
        li = li.split(",")
        username = li[0]
        disklimit = li[1]
        data = {'uidUserId': '','iDisklimit':disklimit}
        re = self.query_user(username)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/creatPridisk.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)


    #@重置用户私有盘
    def reset_pridisk(self,li):
        data = {'uidUserId': ''}
        re = self.query_user(li)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/resetPriDisk.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)

    #@修复用户私有盘
    def repair_pridisk(self,li):
        data = {'uidUserId': ''}
        re = self.query_user(li)
        re_json = json.loads(re)
        url = 'http://'+self.serverip+'/ark//account/user/repairPriDisk.do'
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)

    #@重置用户密码
    def reset_userpw(self,li):
        data = {'uidUserId': '','resetNewPwd':''}
        li = li.split(",")
        username = li[0]
        passwd = li[1]
        url = 'http://'+self.serverip+'/ark//account/user/resetUserPwd.do'
        with open("/js/password.js") as f:
            jsData = f.read()
        pwcode = execjs.compile(jsData).eval('fnEncryptText("'+passwd+'")')
        data['resetNewPwd'] = pwcode
        re = self.query_user(li)
        re_json = json.loads(re)
        for user in re_json['data']:
            userid = user['uidUserId']
            data['uidUserId'] = userid
            self.s.post(url,data=data,cookies=self.cookies)
        
    #@不启用外部认证
    def disable_auth(self,li):
        data = {'SrvType':'disable','radiusServerAddress':''}
        url = 'http://'+self.serverip+'/ark//account/authCfg/saveAuthCfg'
        self.s.post(url,data=data,cookies=self.cookies)

    #@启用邮件服务器验证
    def email_auth(self,li):
        li = li.split(",")
        mailaddress = li[0]
        userpwurl = li[1]
        data = {
            'SrvType': 'mail',
            'mailServerAddress': mailaddress,
            'modifyUserPwdUrl': userpwurl,
            'radiusServerAddress': ''
            }
        url = 'http://'+self.serverip+'/ark//account/authCfg/saveAuthCfg'
        self.s.post(url,data=data,cookies=self.cookies)

    #@启用AD/LDAP服务器验证
    def ad_auth(self,li):
        li = li.split(",")
        ip = li[0]
        dn = li[1]
        resetpwurl = li[2]
        data = {
            'SrvType': 'ldap',
            'mailServerAddress': ip,
            'dnFormat':dn,
            'modifyUserPwdUrl': reseturl,
            'radiusServerAddress': ''
            }
        url = 'http://'+self.serverip+'/ark//account/authCfg/saveAuthCfg'
        self.s.post(url,data=data,cookies=self.cookies)

    #@查询用户认证配置
    def query_userauth(self,li):
        url = 'http://'+self.serverip+'/ark//account/authCfg/queryAuthCfg.do'
        data = {}
        re = self.s.post(url,data=data,cookies=self.cookies)
        return re.text
    
#group = groupuser('192.168.60.200')
#re = group.query('testgroup')
#print(re)
#group.replace_group('testgroup,root,newgroup')
#group.add_group("Root,测试分组")
#re = group.query_userauth("无")
#print(re)
#print(re)
#group.creat_singleuser("yhgtest,123456,yhg1,0")
#group.creat_singleuser("yhgtest1,123456,yhg1,40")
#group.creat_multiuser("testuser,123456,testgroup,20,01,5")

#group.creat_pridisk("yhgtest1,40")

