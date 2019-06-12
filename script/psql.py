#-*-coding:utf-8-*-
import sys
import psycopg2
import psycopg2.extras

class psql(object):
    def __init__(self,serverip):
        self.serverip = serverip
        self.conn=psycopg2.connect(database="cloudbox",user="cloudbox",password="",host=serverip,port="9813",client_encoding="UTF-8")
        self.cur=self.conn.cursor()

    #@查询数据库
    def query_sql(self,strquery):
        strquery = strquery.encode("utf-8")
        
        self.cur.execute(strquery)
        results=self.cur.fetchall()
        self.cur.close()
        self.conn.close()
        return str(results)

