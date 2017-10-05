# -*- coding: utf-8 -*-
from src.my_package1.dealData import *
import time
import numpy as np
def getData():
    data1 = loadData(r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经二路与纬一路.csv')
    data2 = loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经一路与纬一路')
    data3 = loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经三路与纬三路')
    data4=loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经二路与纬二路')
    start = time.clock()
    data1_q = dealToq(data1)
    data2_q = dealToq(data2)
    data3_q = dealToq(data3)
    data4_q = dealToq(data4)
    dataFinal=pd.concat([data1_q,data2_q,data3_q,data4_q])
    print time.clock()-start
    return dataFinal

if __name__ == '__main__':
    a=getData()
    # b=pd.pivot_table(a, index=["year", "month",'days','5min'], values=['car'],
    #                columns=["kakou_no",'direction','lane'], aggfunc=[np.mean], fill_value=None).
    # b.to_csv(r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/处理结果/deal.csv')
