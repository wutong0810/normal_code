
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
# #读取所有文件路径
# def pathGet(path1):
#     path2=unicode(path1,"utf8")
#     filename_total=[]
#     for dirpath, dirnames, filenames in os.walk(path2):
#         for filename in filenames:
#
#             filename2=os.path.join(dirpath,filename)
#     #            print filename2
#             filename_total.append(filename2)
#     return filename_total

# #加载数据
# def loadData(dataPath):
#     dataAll=[]
#     for i in dataPath:
#             data_medium=pd.read_csv(i,header=None)
#             dataAll.append(data_medium)
#     dataFinal=pd.concat(dataAll, ignore_index=True)
#     return dataFinal




def boxFilter(data,Num=15,valueRange=30):
#    数据量太少就不处理，直接返回一个较大的范围
    if len(data)<Num:
        valueDown=0
        valueUp=1000
    else :
        fourDown=np.percentile(data,25)
        fourUp=np.percentile(data,75)
        R=1.5*(fourUp-fourDown)
        tt=max(valueRange,R)
        valueDown=fourDown-tt
        valueUp=fourUp+tt
    return valueDown,valueUp

def wrongNumTotal(data,wrongCarNum):
    num = 0
    for j in wrongCarNum:
        tt0 = data[data.iloc[:, 3] == j]
        tt=tt0.iloc[:,4]
        if len(tt) > 0:
            num = num + tt.iloc[0]
    return num


def dataRange(path0=r'/Users/wutongshu/Documents/spark/testdata2/num/part-00000'):
    data=pd.read_csv(path0,header=None)
    # print data
    data.columns = ['year', 'month', 'day', '30min', 'kakou_no', 'direction', 'clane', 'flow']
    kakouAll=set()
    setMedium=set(zip(data.kakou_no,data.direction))
    kakouAll=kakouAll|setMedium
    #构造一个包含所有卡口和方向的矩阵
    a=np.zeros((48*len(kakouAll),1))
    for i in range(48):
        a[len(kakouAll)*i:len(kakouAll)*(i+1),0]=i+1
    kakouAll2=np.array(list(kakouAll))
    kakouAll2=np.tile(kakouAll2,(48,1))
    kakouAll2=pd.DataFrame(kakouAll2)
    kakouAll2['30min']=a
    kakouAll2.columns=['kakou_no','direction','30min']
    return kakouAll2



def getLabel(path0=r'/Users/wutongshu/Documents/spark/testdata2/num/part-00000'):
    data = pd.read_csv(path0, header=None)
#    统计得到每个卡口的车道数
    data.columns = ['year', 'month', 'day', '30min', 'kakou_no', 'direction', 'clane', 'flow']
    claneTotal=data.groupby([data['year'],data['month'],data['day'],data['kakou_no'],data['direction']])['clane'].nunique()
    claneTotal2=claneTotal.reset_index()
#    统计得到半小时为颗粒度的流量总和
    kakouQ=data.groupby([data['year'],data['month'],data['day'],data['kakou_no'],data['30min'],data['direction']])['flow'].sum()
    kakouQ=kakouQ.reset_index()
    dataFinal2=pd.merge(kakouQ,claneTotal2,on=['year','month','day','kakou_no','direction'])
#    计算每个卡口点位的平均单车道的流量
    dataFinal2['avg']=dataFinal2['flow']/dataFinal2['clane']
    kakouAll2=dataRange(path0=path0)
    dataFinal3=pd.merge(kakouAll2,dataFinal2,how='left',on=['kakou_no','direction','30min'])
    dataFinal3.avg=dataFinal3.avg.fillna(0)
#   加一列初始值为0，并且数据偏大为1，取值为0则取2，四分位法得到的异常数据则取3，正常数据取0
    dataFinal3['status']=0
    dataFinal3.loc[dataFinal3.iloc[:,-2]>750,'status']=1
    dataFinal3.loc[dataFinal3.iloc[:,-2]==0,'status']=2
    return dataFinal3





if __name__=='__main__':
    print getLabel(path0=r'/Users/wutongshu/Documents/spark/testdata2/num/part-00000')