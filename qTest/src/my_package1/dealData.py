# -*- coding: utf-8 -*-
import pandas as pd
import os


def loadData(path0):
    data=pd.read_csv(path0,header=None,encoding='gbk')
    data.columns = ['car', 'brand', 'brand_color', 'car_color', 'kakou_no', 'pass_time', 'speed', 'lane', 'direction',
                    'status', 'location', 'camera', 'year', 'month', 'days']
    # data.pass_time=pd.to_datetime(data.pass_time)
    data.pass_time=data.pass_time.apply(timeChange)
    data.pass_time=pd.to_datetime(data.pass_time)
    return data



#加载数据
def loadDataSum(path1=r'E:\华为数据\测试',dataFomat='.csv'):
    path2=unicode(path1,"utf8")
    filename_total=[]
    for dirpath, dirnames, filenames in os.walk(path2):
        for filename in filenames:
            if os.path.splitext(filename)[1]==dataFomat:
                filename2=os.path.join(dirpath,filename)
                # print filename2
                filename_total.append(filename2)
    dataPath=filename_total
    dataAll=[]
    for i in dataPath:
            dataMedium=pd.read_csv(i,header=None,encoding='gbk')
            dataAll.append(dataMedium)
    dataFinal=pd.concat(dataAll, ignore_index=True)
    # print dataFinal
    dataFinal.columns = ['car', 'brand', 'brand_color', 'car_color', 'kakou_no', 'pass_time', 'speed', 'lane', 'direction',
                    'status', 'location', 'camera', 'year', 'month', 'days']
    # data.pass_time=pd.to_datetime(data.pass_time)
    dataFinal.pass_time=dataFinal.pass_time.apply(timeChange)
    dataFinal.pass_time=pd.to_datetime(dataFinal.pass_time)

    return dataFinal


def timeChange(x):
    if len(x)>13:
        x=x[:19]
    return x

def dealToq(data):
    data['5min']=data.pass_time.apply(lambda x:int((60*x.hour+x.minute)/5))
    data1=data.groupby(['year','month','days','5min','kakou_no','direction','lane'])['car'].count()
    data2=data1.reset_index()
    data2 = data2.sort_values(by=['year', 'month','days','5min','direction','lane'])
    return data2




if __name__=='__main__':
    # data=loadData(r'/Users/wutongshu/Documents/testQdata/kakou3701022131.csv')
    # data2=loadDataSum(path1=r'/Users/wutongshu/Documents/testQdata/kakou3701022129')
    # data_q=dealToq(data)
    data2 = loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/结果文件/经二路与纬二路')
