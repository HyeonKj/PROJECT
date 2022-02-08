# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:20:11 2022

@author: user
"""

import pymysql 

conn, cur = None, None 
data1, data2, data3, data4 = "","","",""
row=None

#메인 코드
conn=pymysql.connect(host='localhost',user='root',password='1111', \
                     db='shoppingDB', charset='utf8')
cur = conn.cursor()

cur.execute("SELECT*FROM userTable")

print("사용자ID 사용자이름 이메일 출생연도")
print("___________________________________")

while(True):
    row=cur.fetchone()
    if row==None:
        break
    data1=row[0]
    data2=row[1]
    data3=row[2]
    data4=row[3]
    print("%5s %15s %15s %d" % (data1, data2, data3, data4))

conn.close()