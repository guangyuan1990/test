import os
import json

def to_name(fun_name,fun):
    fun_name = fun_name.split("@")[1].replace("\n", "").replace(" ","")
    fun = fun.split("(")[0].split(" ")[-1]
    return fun_name,fun

relation_dict = {}

flist = os.listdir('script\\')
for fpy in flist:
    fpy = os.path.join('script\\',fpy)
    if os.path.isfile(fpy):
        f = open(fpy,"r",encoding='UTF-8')
        filename = os.path.basename(fpy).replace('.py','')
        line = f.readline()
        while line:
            if "#@" in line:
                fun_name = line
                fun = f.readline()
                fun_name,fun = to_name(fun_name,fun)
                relation_dict[fun_name] = filename+'.'+fun
            line = f.readline()
        f.close()
fw = open('config\\dict.config', 'w',encoding='UTF-8')
json.dump(relation_dict,fw)
fw.close()

