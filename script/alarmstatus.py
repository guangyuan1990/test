#coding:utf-8
import requests
import json
import time
import execjs

class alarmstatus(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.s = requests.Session()
        data = {"username":"admin","password":"845b23446d1859e819159d95e6e5763a6103032abcc585c9c1c2fd0f75a21d4bdba5dfcd161a8acd8118b799c40443cecc102bdcde7784f28141c9a26fb254a1f1556fa0f8d09475197dac87d2d65e5ce39443d7562830893c973b3a7fb38fc507218920e6f738039c7e90e99c196322fafda7bec2a2734cca58d0ce18f153d6","checkcode":"0000"}
        url = 'http://'+self.serverip+'/ark/login/login.do'
        res = self.s.post(url,data=data)
        self.cookies = res.cookies
        
    def query(self,li):
        creatdate = li
        url = 'http://'+self.serverip+'/ark//dataCenter/general/queryAlarmList.do?ilevels=0,1,2,3&_=1547540131022'
        re = self.s.get(url,cookies = self.cookies)
        re_json = json.loads(re.text)
        for alarm in re_json['data']:
            if creatdate == alarm['dtcreatetime']:
                return alarm
            
    #@查询告警信息
    def query_alarm(self,li):
        creatdate = li
        url = 'http://'+self.serverip+'/ark//dataCenter/general/queryAlarmList.do?ilevels=0,1,2,3&_=1547540131022'
        re = self.s.get(url,cookies = self.cookies)
        re_json = json.loads(re.text)
        for alarm in re_json['data']:
            if creatdate == alarm['dtcreatetime']:
                return str(alarm)

    #@查询告警信息数量
    def query_alarm_num(self,li):
        li = li.split(",")
        ilevels= []
        istatus=1
        data=''
        for param in li:
            if param == '提示':
               ilevels.append("0")
            elif param == '信息':
                ilevels.append("1")
            elif param == '警告':
                ilevels.append("2")
            elif param == '错误':
                ilevels.append("3")
            elif param == '未读':
                istatus = 0
        ilevels.sort()
        for pm in ilevels:
            data = data+pm+','
        data = data[0:-1]
        if istatus==0:
            url = 'http://'+self.serverip+'/ark//dataCenter/general/queryAlarmList.do?ilevels='+data+'&istatus=0&_=1547540131038'
        else:
            url = 'http://'+self.serverip+'/ark//dataCenter/general/queryAlarmList.do?ilevels='+data+'&_=1547540131038'
        re = self.s.get(url)
        re_json = json.loads(re.text)
        return str(len(re_json['data']))

    #@更新告警消息标记
    def update_alarm(self,li):
        li = li.split(",")
        alarm_time = li[0]
        re = self.query(alarm_time)
        alarmid = re['uidalarmid']
        alarm_sign = li[1]
        data = {
            'uidalarmids': alarmid,
            'itype': 1
            }
        url = 'http://'+self.serverip+'/ark//dataCenter/general/updateAlarmStatus.do'
        if alarm_sign=="已读":
            data['itype']=1
        else:
            data['itype']=0
       self.s.post(url,data=data,cookies=self.cookies)

    #@删除告警信息
    def delete_alarm(self,li):
        li = li.split(",")
        month = li[0]
        data ={'month': 1}
        if month == '一个月':
            data['month']=1
        elif month == '三个月':
            data['month']=3
        elif month == '六个月':
            data['month']=6
        url = 'http://'+self.serverip+'/ark//dataCenter/general/deleteAlarms.do'
        self.s.post(url,data=data,cookies=self.cookies)
        
#alarm = alarmstatus('192.168.60.200')
#re = alarm.query_test("错误,提示,警告,错误")
#print(re)
#re=alarm.query_test("警告,未读")
#alarm.update_alarm("2019-01-09 11:46:16,未读")
#print(re)
