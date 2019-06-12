#coding: utf-8

import xlrd
import xlwt
import configparser
import json
import time
from public.log import Logger
from public.report import *
from public.send_email import *        
class LazyImport(object):
    """
    动态导入模块
    """
    def __init__(self, module_name, module_class):
        """
        :param module_name:
        :param module_class:
        :return: 等同于 form module_name import module_class
        """
        self.module_name = module_name
        self.module_class = module_class
        self.module = None
 
    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name, fromlist=[self.module_class])
        return getattr(self.module, name)

    
def read_excel(casepath,sign):
    testcase={}
    workbook = xlrd.open_workbook(casepath,formatting_info=True)
    sheet = workbook.sheet_by_name('case')
    casename_list = list(sheet.merged_cells)
    casename_list_new = []
    for ls in casename_list:
        if 0 in ls:
            continue
        elif ls[2] == 1:
            ls = (ls[0],ls[1],ls[2]+1,ls[3]+1)
            casename_list_new.append(ls)
    #处理非合并项的用例，即用例只包含一个步骤
    l = len(casename_list_new)-1
    i=0
    while i < l:
        
        if casename_list_new[i][1]==casename_list_new[i+1][0]:
            pass
        else:
            ls = (casename_list_new[i][1],casename_list_new[i][1]+1,2,3)
            casename_list_new.insert(i+1,ls)
            l = l+1
        i = i+1
        
    casename_list_new1 = casename_list_new[:]#列表浅拷贝
   
    for ls in casename_list_new:
        
        casestatus = str(int(sheet.cell_value(ls[0],ls[2]-1)))
        
        if casestatus not in sign:#判断执行标记是否在配置标记列表中，不在则删除该项
            casename_list_new1.remove(ls)
        
    for case in casename_list_new1:
        testcase[sheet.cell_value(case[0],case[3]-1)]=[case[0],case[1]]
    return testcase
    
def case(casepath,casename,steps,logger,temp,rworkbook,worksheet2):
    rworkbook = rworkbook
    worksheet2 = worksheet2
    workbook = xlrd.open_workbook(casepath,formatting_info=True)
    sheet = workbook.sheet_by_name('case')
    case_status='ok'
    casedata["case_name"] = casename
    for i in range(steps[0],steps[1]):
        action=sheet.cell_value(i,3)
        ac_param=sheet.cell_value(i,4)
        waittime=sheet.cell_value(i,5)
        re_param=sheet.cell_value(i,6)
        #print(re_param)
        relation=sheet.cell_value(i,7)
        requery=sheet.cell_value(i,8)
        query_param = sheet.cell_value(i,9)
        resurt = step(action,ac_param,waittime,re_param,relation,requery,query_param)
        if resurt:
            casedata["test_result"]="成功"
            write_detail(worksheet2,temp,casedata,rworkbook)#写执行结果到测试报告
            temp = temp +1
            continue
        else:
            case_status='faild'
            casedata["test_result"]="失败"
            write_detail(worksheet2,temp,casedata,rworkbook)#写执行结果到测试报告
            temp = temp +1
            logger.info(action+"执行失败")
            break
        
        
    if case_status=='ok':
        logger.info(casename+"执行成功!")
        testdata["test_success"] = testdata["test_success"] + 1
    else:
        logger.info(casename+"执行失败!")
        testdata["test_failed"] = testdata["test_failed"] +1

    return temp 
def step(action,ac_param,waittime,re_param,relation,requery,query_param):
    casedata["action"] = action
    casedata["ac_param"] = ac_param
    casedata["re_param"] = re_param
    casedata["relation"] = relation
    casedata["query"] = requery
    casedata["query_param"] = query_param
    '''
    config = configparser.ConfigParser()
    config.read(r"config\ac_dict.config",encoding="utf-8-sig")
    hostlist = config.options("ac_dict")
    ac_dict = json.loads(config.get("ac_dict",hostlist[0]))
    '''
    if action:#如果有执行动作
        fr = open('config\\dict.config', 'r',encoding='UTF-8')
        ac_dict = json.load(fr)
        fr.close()
        clsname = ac_dict[action].split(".")[0]
        method = ac_dict[action].split(".")[1]
        #ac_param = ac_param.split(",")
        importmodule = LazyImport("script."+clsname, clsname)
        classname = getattr(importmodule,clsname)
        config.read(r"config\test.config",encoding="utf-8-sig")
        serverip = config.options("serverip")
        ip = config.get("serverip",serverip[0])
        obj = classname(ip)
        getattr(obj,method)(ac_param)#执行动作
    else:
        logger.info("无动作跳过")
        pass
    
    if waittime=='~':#如果等待时间无无穷将循环检测，直到满足条件
        clsname = ac_dict[requery].split(".")[0]
        method = ac_dict[requery].split(".")[1]
        importmodule = LazyImport("script."+clsname, clsname)
        classname = getattr(importmodule,clsname)
        obj = classname(ip)
        while True:
            time.sleep(30)
            print("等待满足结果")
            re = getattr(obj,method)(query_param)#执行查询函数
            casedata["actual_result"] = re
            if relation=="包含于":
                if (re_param in re):
                    return True
                    break
            elif relation=="等于":
                if (re_param==re):
                    return True
                    break
            elif relation=="不等于":
                if (re_param!=re):
                    return True
                    break
            elif relation=="不包含于":
                if (re_param not in re):
                    return True
                    break
    else:
        try:
            time.sleep(int(waittime))
        except Exception as e:
            time.sleep(1)
        '''
        config.read(r"config\query_dict.config",encoding="utf-8-sig")
        querylist = config.options("query_dict")
        query_dict = json.loads(config.get("query_dict",querylist[0]))
        '''
    if re_param:#如果有结果参数就执行查询动作
        fr = open('config\\dict.config', 'r',encoding='UTF-8')
        ac_dict = json.load(fr)
        fr.close()
        clsname = ac_dict[requery].split(".")[0]
        method = ac_dict[requery].split(".")[1]
        importmodule = LazyImport("script."+clsname, clsname)
        classname = getattr(importmodule,clsname)
        config.read(r"config\test.config",encoding="utf-8-sig")
        serverip = config.options("serverip")
        ip = config.get("serverip",serverip[0])
        obj = classname(ip)
        re = getattr(obj,method)(query_param)#执行查询函数
        casedata["actual_result"] = re
        if re:
            if relation=="包含于":
                return(re_param in re)
            elif relation=="等于":
                return(re_param==re)
            elif relation=="不等于":
                return(re_param!=re)
            elif relation=="不包含于":
                return(re_param not in re)
        else:
            re='None'
            if relation=="包含于":
                return(re_param in re)
            elif relation=="等于":
                return(re_param==re)
            elif relation=="不等于":
                return(re_param!=re)
            elif relation=="不包含于":
                return(re_param not in re)

    else:#没有直接返回成功
        casedata["actual_result"]=""
        logger.info("没有查询动作")
        return True
config = configparser.ConfigParser()
#读取测试用例文件路径
config.read(r"config\test.config",encoding="utf-8-sig")
casepath = config.options("casepath")
path = config.get("casepath",casepath[0])
casefilename = path.split('\\')[1].split('.')[0]
#读取测试平台IP
serverip = config.options("serverip")
ip = config.get("serverip",serverip[0])
#读取执行标记
runsign = config.options("runsign")
sign = config.get("runsign",runsign[0])
#读取测试执行次数
testnum = config.options("testnum")
num = int(config.get("testnum",testnum[0]))
#读取邮件配置信息
email = config.options("email")
receiver = config.get("email",email[3]).split(",")
#print(receiver)
#开始执行测试相关，如果执行多次从这里开始循环
global temp
temp=3
t = time.localtime()
strtime = str(t.tm_year)+str(t.tm_mon).rjust(2,'0')+str(t.tm_mday).rjust(2,'0')+str(t.tm_hour).rjust(2,'0')+str(t.tm_min).rjust(2,'0')+str(t.tm_sec).rjust(2,'0')
logger = Logger(logname='log'+strtime+'.txt',loglevel=1,logger="测试").getlog()
logger.info("测试开始")
testcase=read_excel(path,sign)
logger.info("读取测试用例成功")

#生成测试报告文件
rworkbook,rworksheet,rworksheet2 = report(casefilename,strtime)
testversion = {"test_name": casefilename, "test_version": "V3.7.3", "test_pl": "python", "test_serverip": ip}
testdata = {"test_sum": 0, "test_success": 0, "test_failed": 0, "test_date": str(t.tm_year)+"-"+str(t.tm_mon).rjust(2,'0')+"-"+str(t.tm_mday).rjust(2,'0')+" "+str(t.tm_hour).rjust(2,'0')+":"+str(t.tm_min).rjust(2,'0')}
worksheet2 = test_detail(rworkbook,rworksheet2)
casedata = {"case_name":"","action":"","ac_param":"","re_param":"","relation":"","query":"","query_param":"","test_result":"","actual_result":"test"}
for casename,steps in testcase.items():
    try:
        testdata["test_sum"] = testdata["test_sum"] + 1
   
        temp = case(path,casename,steps,logger,temp,rworkbook,worksheet2)

    
    except Exception as e:
        testdata["test_failed"] = testdata["test_failed"] + 1
        logger.error(str(e))
        logger.info(casename+"执行失败，请检查运行环境和配置信息!")
        continue
    
init(rworkbook,rworksheet,testversion,testdata)
logger.info("测试结束")
rworkbook.close()
if receiver !=['']:#如果收件人不为空，发送邮件
    send_email('report\\'+casefilename+'测试报告'+strtime+'.xlsx')
    logger.info("发送邮件")
else:
    logger.info("收件人为空，不发邮件")
    pass

    
