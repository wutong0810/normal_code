# -*- coding: utf-8 -*-

import numpy as np

import MySQLdb
def writeData(data):
    db = MySQLdb.connect(host='*****',
                         user='******',
                         passwd='******',port=4008
                         db='its')
    data1=np.array(data)
    cursor = db.cursor()
    # print data1
    try:
        for i in range(0,len(data1),10000):
            t=i+10000
            if t>=len(data1):
                t=-1
            dataMedium=data1[i:t,:].tolist()
            print dataMedium
            sqli = "insert into jinan_kakou_status(kakou_id,direction,time,status) values(%s,%s,%s,%s)"
            cursor.executemany(sqli,dataMedium)
    except Exception, e::
        print "Error: unable to insert data"
        print str(e)
    cursor.close()
    db.commit()

    # 关闭数据库连接
    db.close()





