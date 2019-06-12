#coding: utf-8    
  
import smtplib    
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText    
from email.mime.image import MIMEImage 
from email.header import Header   
import configparser
import os

def send_email(attach_file):
    #读取邮件配置信息
    config = configparser.ConfigParser()
    config.read(r"config\test.config",encoding="utf-8-sig")
    email = config.options("email")
    smtpserver = config.get("email",email[0])
    username = config.get("email",email[1])
    password = config.get("email",email[2])
    receiver = config.get("email",email[3]).split(",")
    sender = username
    '''
    设置smtplib所需的参数
    下面的发件人，收件人是用于邮件传输的。
    smtpserver = 'smtp.qq.com'
    username = '@qq.com'
    password=''
    sender = username
    receiver=['2@qq.com','6@qq.com']
    '''
    subject = '自动化测试执行结果'
    #通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
    #subject = '中文标题'
    subject=Header(subject, 'utf-8').encode()
    
    #构造邮件对象MIMEMultipart对象
    #下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed') 
    msg['Subject'] = subject
    msg['From'] = 'AutoTest Platform'
    msg['To'] = ";".join(receiver) 
    #构造文字内容   
    text = "测试执行完毕，测试详情请查看附件"    
    text_plain = MIMEText(text,'plain', 'utf-8')    
    msg.attach(text_plain)
    
    '''
    #构造图片链接
    sendimagefile=open(r'D:\pythontest\testimage.png','rb').read()
    image = MIMEImage(sendimagefile)
    image.add_header('Content-ID','<image1>')
    image["Content-Disposition"] = 'attachment; filename="testimage.png"'
    msg.attach(image)

    #构造html
    #发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
    html = """
    <html>  
      <head></head>  
       <body>  
        <p>Hi!<br>  
       How are you?<br>  
       Here is the <a href="http://www.baidu.com">link</a> you wanted.<br> 
     </p> 
     </body>  
     </html>  
     """    
     text_html = MIMEText(html,'html', 'utf-8')
     text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'   
     msg.attach(text_html)    

    '''
    #构造附件
    sendfile = open(attach_file,'rb').read()
    attach_name = os.path.basename(attach_file)
    text_att = MIMEText(sendfile, 'base64', 'utf-8') 
    text_att["Content-Type"] = 'application/octet-stream'  
    text_att.add_header('Content-Disposition', 'attachment', filename=("gbk", "", attach_name))
    msg.attach(text_att)    
       
    #发送邮件
    smtp = smtplib.SMTP()    
    smtp.connect(smtpserver,25)
    #我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    #smtp.set_debuglevel(1)  
    smtp.login(username, password)    
    smtp.sendmail(sender, receiver, msg.as_string())    
    smtp.quit()

#send_email(r'report\case测试报告20181226191755.xlsx')
