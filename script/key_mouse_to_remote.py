from tkinter import *
from tkinter import ttk
from pynput.mouse import Button, Controller
import time
from pynput import mouse
from pynput import keyboard
import socket
import os
import threading
import inspect
import ctypes


def on_press(key):
   
    try:
        action = "keyboard"+","+"0"+","+key.name + ","+"press"
    except:
        action = "keyboard"+","+"1"+","+key.char + ","+"press"
    ip = t.get("1.0", "end")
    ip_list = ip.split("\n")
    if b1['text']=='结束映射':
        for ip in ip_list[0:-1]:
            ip_port = (ip,9999)
            sk = socket.socket()
            sk.connect(ip_port)
            sk.sendall(bytes(action,encoding='utf-8'))

def on_release(key):
    try:
        action = "keyboard"+","+"0"+","+key.name + ","+"repress"
    except:
        action = "keyboard"+","+"1"+","+key.char + ","+"repress"
    ip = t.get("1.0", "end")
    ip_list = ip.split("\n")
    if b1['text']=='结束映射':
        for ip in ip_list[0:-1]:
            ip_port = (ip,9999)
            sk = socket.socket()
            sk.connect(ip_port)
            sk.sendall(bytes(action,encoding='utf-8'))

def key_fun():
    
    while True:
        with keyboard.Listener(
            on_press = on_press,
            on_release = on_release) as listener:
            listener.join()
        

def on_click(x, y , button, pressed):
    action = "mouse"+","+button.name+","+str(x)+","+str(y)+","+str(pressed)
   # print(action)
    ip = t.get("1.0", "end")
    ip_list = ip.split("\n")
    if b1['text']=='结束映射':
        for ip in ip_list[0:-1]:
            ip_port = (ip,9999)
            sk = socket.socket()
            sk.connect(ip_port)
            sk.sendall(bytes(action,encoding='utf-8'))
    

def on_scroll(x, y ,dx, dy):
    print('scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

def mouse_fun():
    
    while True:
        with mouse.Listener( on_click = on_click,on_scroll = on_scroll) as listener:
            listener.join()
            
root = Tk()
root.geometry('400x400')
root.title("键鼠事件映射工具")
lf = ttk.LabelFrame(root, text="需要映射虚拟机IP")
lf.pack(fill=X, padx=15, pady=8)
top_frame = Frame(lf)
top_frame.pack(fill=X,expand=YES,side=TOP,padx=15,pady=8)
L1 = ttk.Label(top_frame, text="IP地址：",width=10)
L1.pack(side=LEFT,expand=YES,fill=Y)
t = Text(top_frame,height=20,width = 30)     #这里设置文本框高，可以容纳两行
t.pack(side = LEFT,padx=10)

threads = []
t1 = threading.Thread(target= mouse_fun)
threads.append(t1)
t2 = threading.Thread(target= key_fun)
threads.append(t2)
t1.setDaemon(True)
t2.setDaemon(True)
for th in threads:
    th.start()
def show():
    if b1['text']=='开始映射':
        b1['text']='结束映射'
          
    else:
        b1['text']='开始映射'
    
b1 = ttk.Button(root,text='开始映射',width=20,command=show)
b1.pack()
root.mainloop()

