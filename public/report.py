# -*- coding: utf-8 -*-
import xlsxwriter
import time

def get_format(wd, option={}):
    return wd.add_format(option)
 
# 设置居中
def get_format_center(wd,num=1):
    return wd.add_format({'align': 'center','valign': 'vcenter','border':num})
def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)
 
# 写数据
def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))

def init(workbook,worksheet,testversion,testdata):
 
    # 设置列行的宽高
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 20)
    worksheet.set_column("E:E", 20)
    worksheet.set_column("F:F", 20)
 
    worksheet.set_row(1, 30)
    worksheet.set_row(2, 30)
    worksheet.set_row(3, 30)
    worksheet.set_row(4, 30)
    worksheet.set_row(5, 30)
 
    # worksheet.set_row(0, 200)
 
    define_format_H1 = get_format(workbook, {'bold': True, 'font_size': 18})
    define_format_H2 = get_format(workbook, {'bold': True, 'font_size': 14})
    define_format_H1.set_border(1)
 
    define_format_H2.set_border(1)
    define_format_H1.set_align("center")
    define_format_H2.set_align("center")
    define_format_H2.set_bg_color("blue")
    define_format_H2.set_color("#ffffff")
    # Create a new Chart object.
 
    worksheet.merge_range('A1:F1', '测试报告总概况', define_format_H1)
    worksheet.merge_range('A2:F2', '测试概括', define_format_H2)
    worksheet.merge_range('A3:A6', '这里放图片', get_format_center(workbook))
 
    _write_center(worksheet, "B3", '项目名称', workbook)
    _write_center(worksheet, "B4", '接口版本', workbook)
    _write_center(worksheet, "B5", '脚本语言', workbook)
    _write_center(worksheet, "B6", '测试平台', workbook)
 
 
    #data = {"test_name": "智商", "test_version": "v2.0.8", "test_pl": "python", "test_net": "wifi"}
    data = testversion
    _write_center(worksheet, "C3", data['test_name'], workbook)
    _write_center(worksheet, "C4", data['test_version'], workbook)
    _write_center(worksheet, "C5", data['test_pl'], workbook)
    _write_center(worksheet, "C6", data['test_serverip'], workbook)
 
    _write_center(worksheet, "D3", "用例总数", workbook)
    _write_center(worksheet, "D4", "通过总数", workbook)
    _write_center(worksheet, "D5", "失败总数", workbook)
    _write_center(worksheet, "D6", "测试日期", workbook)
 
 
    data1 = testdata
    #data1 = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
    _write_center(worksheet, "E3", data1['test_sum'], workbook)
    _write_center(worksheet, "E4", data1['test_success'], workbook)
    _write_center(worksheet, "E5", data1['test_failed'], workbook)
    _write_center(worksheet, "E6", data1['test_date'], workbook)
 
    _write_center(worksheet, "F3", "备注", workbook)
 
 
    worksheet.merge_range('F4:F6', '', get_format_center(workbook))
 
    pie(workbook, worksheet)
 
 # 生成饼形图
def pie(workbook, worksheet):
    chart1 = workbook.add_chart({'type': 'pie'})
    chart1.add_series({
    'name':       '接口测试统计',
    'categories':'=测试总况!$D$4:$D$5',
   'values':    '=测试总况!$E$4:$E$5',
    })
    chart1.set_title({'name': '接口测试统计'})
    chart1.set_style(10)
    worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})
 
def test_detail(workbook,worksheet):
 
    # 设置列行的宽高
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 20)
    worksheet.set_column("D:D", 20)
    worksheet.set_column("E:E", 20)
    worksheet.set_column("F:F", 20)
    worksheet.set_column("G:G", 20)
    worksheet.set_column("H:H", 20)
    worksheet.set_column("I:I", 120)

    worksheet.set_row(0, 30)
    worksheet.set_row(1, 30)
    worksheet.set_row(2, 30)
    #worksheet.set_row(3, 30)
    #worksheet.set_row(4, 30)
   # worksheet.set_row(5, 30)
    #worksheet.set_row(6, 30)
    #worksheet.set_row(7, 30)
    #worksheet.set_row(8, 30)

    #设置表格头
    worksheet.merge_range('A1:I1', '测试详情', get_format(workbook, {'bold': True, 'font_size': 18 ,'align': 'center','valign': 'vcenter','bg_color': 'blue', 'font_color': '#ffffff'}))
    _write_center(worksheet, "A2", '用例名称', workbook)
    _write_center(worksheet, "B2", '执行动作', workbook)
    _write_center(worksheet, "C2", '执行参数', workbook)
    _write_center(worksheet, "D2", '结果参数', workbook)
    _write_center(worksheet, "E2", '关系', workbook)
    _write_center(worksheet, "F2", '结果查询', workbook)
    _write_center(worksheet, "G2", '查询参数', workbook)
    _write_center(worksheet, "H2", '测试结果', workbook)
    _write_center(worksheet, "I2", '实际结果', workbook)
    
    return worksheet

    
def report(filename,strtime):
    t = time.localtime()
    strtime = strtime
    workbook = xlsxwriter.Workbook('report\\'+filename+'测试报告'+strtime+'.xlsx')
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    return workbook,worksheet,worksheet2

def write_detail(worksheet,temp,casedata,workbook):
    worksheet.set_row(temp, 30)
    _write_center(worksheet, "A"+str(temp), casedata["case_name"], workbook)
    _write_center(worksheet, "B"+str(temp), casedata["action"], workbook)
    _write_center(worksheet, "C"+str(temp), casedata["ac_param"], workbook)
    _write_center(worksheet, "D"+str(temp), casedata["re_param"], workbook)
    _write_center(worksheet, "E"+str(temp), casedata["relation"], workbook)
    _write_center(worksheet, "F"+str(temp), casedata["query"], workbook)
    _write_center(worksheet, "G"+str(temp), casedata["query_param"], workbook)
    _write_center(worksheet, "H"+str(temp), casedata["test_result"], workbook)
    _write_center(worksheet, "I"+str(temp), casedata["actual_result"], workbook)

#workbook,worksheet,worksheet2 = report("登陆测试")
#testversion = {"test_name": "智商", "test_version": "v2.0.8", "test_pl": "python", "test_serverip": "wifi"}
#testdata = {"test_sum": 100, "test_success": 80, "test_failed": 20, "test_date": "2018-10-10 12:10"}
#casedata = {"case_name":"登陆测试","action":"使用用户名登陆","ac_param":"yhg","re_param":"success","relation":"包含","query":"登陆状态查询","query_param":"名字","test_result":"成功","actual_result":"test[faild]"}
#temp=3
#init(worksheet,testversion,testdata)

#worksheet2 = test_detail(worksheet2)
#write_detail(worksheet2,temp,casedata,workbook)
#workbook.close()

