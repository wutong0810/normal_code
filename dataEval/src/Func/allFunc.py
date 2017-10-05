# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time
import datetime
# hell

def boxFilter(data,Num=15,valueRange=30):
#    数据量太少就不处理，直接返回一个较大的范围
    if len(data)<Num:
        valueDown=0
        valueUp=10000
    else :
        fourDown=np.percentile(data,25)
        fourUp=np.percentile(data,75)
        R=1.5*(fourUp-fourDown)
        tt=max(valueRange,R)
        valueDown=fourDown-tt
        valueUp=fourUp+tt
    return valueDown,valueUp



# data为数组，kakouTotal为np.array
def getAllKakou(data,kakouTotal):
    # 获取所有出现过的天数
    timeAll=set(zip(data.year, data.month,data.day))
    timeAll2 = np.array(list(timeAll))
    kakouAll=set(zip(data.kakou_no,data.direction))
    #构造一个包含所有卡口和方向的矩阵

    kakouAll2=np.array(list(kakouAll))
    kakouElse=np.setdiff1d(kakouTotal,kakouAll2)
    # 对于部分从没有出现过的卡口数据，将其方向标为-1
    kakouElse2=np.zeros((len(kakouElse),2))
    kakouElse2[:,0]=kakouElse
    kakouElse2[:,1]=-1
    kakouAll3=np.vstack((kakouAll2,kakouElse2))
    #构造一个包含所有卡口和方向的矩阵
    a=np.zeros((48*len(kakouAll3),1))
    for i in range(48):
        a[len(kakouAll3)*i:len(kakouAll3)*(i+1),0]=i
    kakouAll3=np.tile(kakouAll3,(48,1))
    kakouAll3=pd.DataFrame(kakouAll3)
    kakouAll3['30min']=a
    # kakouAll3=kakouAll3.astype(np.int64)
    kakouFinalAll=np.zeros((len(kakouAll3)*len(timeAll2),6))
    kakouFinalAll[:,3:]=np.tile(kakouAll3,(len(timeAll2),1))
    for j in range(len(timeAll2)):
        kakouFinalAll[len(kakouAll3)*j:len(kakouAll3)*(j+1),0]=timeAll2[j,0]
        kakouFinalAll[len(kakouAll3)*j:len(kakouAll3)*(j+1),1]=timeAll2[j,1]
        kakouFinalAll[len(kakouAll3)*j:len(kakouAll3)*(j+1),2]=timeAll2[j,2]
    kakouFinalAll=kakouFinalAll.astype(np.int64)
    kakouFinalAll=pd.DataFrame(kakouFinalAll)
    kakouFinalAll.columns=['year','month','day','kakou_no','direction','30min']
    # kakouFinalAll.sort_values(by=['year','month','day','kakou_no','kakou_no','direction','30min'])
    return kakouFinalAll



def getLabel(data,kakouAll2):
#    统计得到每个卡口的车道数
    claneTotal=data.groupby([data['year'],data['month'],data['day'],data['kakou_no'],data['direction']])['lane'].nunique()
    claneTotal2=claneTotal.reset_index()
#    统计得到半小时为颗粒度的流量总和
    kakouQ=data.groupby([data['year'],data['month'],data['day'],data['kakou_no'],data['30min'],data['direction']])['count'].sum()
    kakouQ=kakouQ.reset_index()
    dataFinal2=pd.merge(kakouQ,claneTotal2,on=['year','month','day','kakou_no','direction'])
#    计算每个卡口点位的平均单车道的流量
    dataFinal2['avg']=dataFinal2['count']/dataFinal2['lane']
    dataFinal3=pd.merge(kakouAll2,dataFinal2,how='left',on=['year','month','day','kakou_no','direction','30min'])
    dataFinal3.avg=dataFinal3.avg.fillna(0)
#   加一列初始值为0，并且数据偏大为1，取值为0则取2，四分位法得到的取值区间正常的取0，低于区间下界的则取3，超过区间上届的取4
    dataFinal3['status']=0
    dataFinal3.loc[dataFinal3.iloc[:,-2]>750,'status']=1
    dataFinal3.loc[dataFinal3.iloc[:,-2]==0,'status']=2
    return dataFinal3




def getDataRange(data,num1,valueRange1):
    # 确定所有的卡口位置和方向，得到所有的设备和其方向的唯一值
    data['down']=0
    data['up']=9999
    # 给所有的卡口（各方向流量）标定阈值区间
    choice = set(zip(data.kakou_no, data.direction))
    timeAll = set(zip(data.year, data.month, data.day))
    data2 = np.array(data)
    dataFourFilter = np.zeros((len(data2), 12))
    for j, i in enumerate(choice):
        dataMedium = data2[(data2[:, 3] == i[0]) & (data2[:, 4] == i[1])]
        print 'finished'+' '+str(format((float(j)/len(choice)), '3.2%'))
        for t in range(48):
            dataMedium2 = dataMedium[dataMedium[:, 5] == t]
            dataMedium3 = dataMedium2[dataMedium2[:, -3] == 0]
            valueDown, valueUp = boxFilter(dataMedium3[:, -4], Num=num1, valueRange=valueRange1)
            dataMedium2[:, -2] = valueDown
            dataMedium2[:, -1] = valueUp
            timelong=len(timeAll)
            dataFourFilter[(j * 48 * timelong + t * timelong):(j * 48 * timelong + (t+1) * timelong), :] = dataMedium2
    dataFourFilter2 = pd.DataFrame(dataFourFilter)
    dataFourFilter2.columns = ['year','month','day','kakou_no', 'direction', '30min', 'count','lane', 'avg', 'status', 'downValue', 'upValue']
    return dataFourFilter2



def getToday(timeNow1,data):
    timeNow2=time.strptime(timeNow1,"%Y/%m/%d")
    year1=timeNow2.tm_year
    month1=timeNow2.tm_mon
    day1=timeNow2.tm_mday
    # 取出当天评估的数据
    data2=data[(data.iloc[:,0]==year1)&(data.iloc[:,1]==month1)&(data.iloc[:,2]==day1)]
    # print data2
    data3=np.array(data2)
    data3[np.where((data3[:,-3]==0)&(data3[:,-4]<data3[:,-2])),:]=3
    data3[np.where((data3[:,-3] == 0) & (data3[:,-4] > data3[:,-1])),:]=4
    data2=pd.DataFrame(data3)
    data2.columns = ['year','month','day','kakou_no', 'direction', '30min', 'count','lane', 'avg', 'status', 'downValue', 'upValue']
    # data2.loc[((data2.loc[:, 'avg'] < data2.loc[:, 'downValue'])&(data2.loc[:, 'status'] == 0)),'status']=3
    # data2.loc[((data2.loc[:, 'avg'] > data2.loc[:, 'upValue']) & (data2.loc[:, 'status'] == 0)), 'status'] = 4
    time_1=str(year1)+'-'+str(month1)+'-'+str(day1)+' '+'00:00:00'
    data2['30min']=data2.loc[:,'30min'].apply(lambda x:datetime.timedelta(minutes=30)*int(x)+datetime.datetime.strptime(time_1, '%Y-%m-%d %H:%M:%S'))
    data2=data2.loc[:,['kakou_no','direction','30min','status']]
    return data2


















