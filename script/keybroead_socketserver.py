#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import os
import json
from pynput import mouse,keyboard
import psutil
#from pynput.mouse import Button, Controller
#from pynput.keyboard import Key, Controller

netcard_info = []
info = psutil.net_if_addrs()
for k,v in info.items():
    for item in v:
        if item[0] == 2 and not item[1]=='127.0.0.1':
            netcard_info.append(item[1])
#print(netcard_info)          
ip_port = (netcard_info[0],9999)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)
keyboards = keyboard.Controller()
mouses = mouse.Controller()
Keys = keyboard.Key
Button = mouse.Button

while True:
    conn,addr = sk.accept()
    client_data = conn.recv(1024)
    client_data = client_data.decode(encoding="utf-8", errors="strict")
    
    data_list = client_data.split(",")
    cls = data_list[0]
    print(data_list)
    if cls == "keyboard":
        sign = data_list[1]
        key = data_list[2]
        press = data_list[3]
        if sign == "0":
            ky = getattr(Keys,key)
        else:
            ky = key
        if press == "press":
            keyboards.press(ky)
        else:
            keyboards.release(ky)
    else:
        x = int(data_list[2])
        y = int(data_list[3])
        mouses.position = (x,y)
        if data_list[1]=="left":
            bt = Button.left
        else:
            bt = Button.right
        if data_list[4] == "True":
            mouses.press(bt)
        else:
            mouses.release(bt)
    conn.close()
