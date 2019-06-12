from selenium import webdriver
import time
import os
import shutil    


class web(object):
    def __init__(self,serverip):
        shutil.copy("driver\chromedriver.exe",os.getcwd())
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.serverip = serverip
        time.sleep(10)
        
    #@登陆管理平台
    def login(self,data):
        data = data.split(",")
        ip = data[0]
        user = data[1]
        password = data[2]
        self.driver.get("http://"+ip+"/ark/main/index.do")
        time.sleep(5)
        self.driver.find_element_by_id("form_login_username").send_keys(user)
        self.driver.find_element_by_id("form_login_password").send_keys(password)
        self.driver.find_element_by_id("button_loginSubmit").click()
        
    
    
