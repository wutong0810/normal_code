# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""

import sys
sys.path.append(r'C:\Users\wutongshu\Desktop\pythonCode')
from allFunc import *



#==============================================================================
# 利用四分位法分析数据是否在合理区间，由于当数据量较多时，数据合理区间比较准确
#==============================================================================


#1.统计每天有数据的卡口数量
#加载数据
dataPath=pathGet(path1=r'C:\Users\wutongshu\Desktop\滴滴数据质量评估\0817数据清洗后2.0\0801-0816流量按照30min组合\job_id=2745139_dir',dataFomat='.csv')
dataFinal=loadData(dataPath)
dataFinal.columns=['year','month','day','30min','kakou_no','direction','clane','flow'] 




#2.获取所有出现过的卡口数量
kakouAll=set()

for j in range(1,12):
    dataMedium=dataFinal[dataFinal.day==j]
    setMedium=set(zip(dataMedium.kakou_no,dataMedium.direction))
    kakouAll=kakouAll|setMedium
#构造一个包含所有卡口和方向的举证
a=np.zeros((48*len(kakouAll),1))
for i in range(48):
    a[len(kakouAll)*i:len(kakouAll)*(i+1),0]=i+1
kakouAll2=np.array(list(kakouAll))
kakouAll2=np.tile(kakouAll2,(48,1))
kakouAll2=pd.DataFrame(kakouAll2)
kakouAll2['30min']=a
kakouAll2.columns=['kakou_no','direction','30min']






dataStore=[]

for i in range(1,12):
    dataMedium=dataFinal[dataFinal.day==i]
#    统计得到每个卡口的车道数
    claneTotal=dataMedium.groupby([dataMedium['kakou_no'],dataMedium['direction']])['clane'].nunique()
    claneTotal2=claneTotal.reset_index()

#    统计得到半小时为颗粒度的流量总和
    kakouQ=dataMedium.groupby([dataMedium['kakou_no'],dataMedium['direction'],dataMedium['30min']])['flow'].sum()
    kakouQ=kakouQ.reset_index()
    dataFinal2=pd.merge(kakouQ,claneTotal2,on=['kakou_no','direction'])
#    计算每个卡口点位的平均单车道的流量
    dataFinal2['avg']=dataFinal2['flow']/dataFinal2['clane']
    dataFinal3=pd.merge(kakouAll2,dataFinal2,how='left',on=['kakou_no','direction','30min'])
    dataFinal3.avg=dataFinal3.avg.fillna(0)
#   加一列初始值为0，并且数据偏大为1，取值为0则取2，四分位法得到的异常数据则取3，正常数据取0
    dataFinal3['status']=0
    dataFinal3.loc[dataFinal3.iloc[:,-2]>750,'status']=1
    dataFinal3.loc[dataFinal3.iloc[:,-2]==0,'status']=2
#    dataAbnormal[i-1,0]=len(dataFinal3[dataFinal3.loc[:,'status']==1])
#    dataAbnormal[i-1,1]=len(dataFinal3[(dataFinal3.loc[:,'status']==2)&((dataFinal3.loc[:,'30min']<=12))])
#    dataAbnormal[i-1,2]=len(dataFinal3[(dataFinal3.loc[:,'status']==2)&((dataFinal3.loc[:,'30min']>=12))])
    dataStore.append(dataFinal3)
dataStoreFinal=pd.concat(dataStore, ignore_index=True)



#dataStoreFinal.ix[:,'down']=0
#dataStoreFinal.ix[:,'up']=1000
#确定所有的卡口位置和方向，得到所有的设备和其方向的唯一值
choice=set(zip(dataStoreFinal.kakou_no,dataStoreFinal.direction))



dataFourFilter=[]
for i in choice:
    dataMedium=dataStoreFinal[(dataStoreFinal['kakou_no']==i[0])&(dataStoreFinal['direction']==i[1])]
    for j in range(1,49):
        dataMedium2=dataMedium[dataMedium.ix[:,'30min']==j]
        dataMedium3=dataMedium2[dataMedium2.ix[:,'status']==0]
        valueDown,valueUp=boxFilter(dataMedium3.ix[:,'avg'],Num=6,valueRange=30)
        dataMedium2.loc[((dataMedium2.ix[:,'avg']>valueUp)|(dataMedium2.ix[:,'avg']<valueDown))&(dataMedium2.ix[:,'status']==0),'status']=3
        dataFourFilter.append(dataMedium2)
dataFourFilter2=pd.concat(dataFourFilter, ignore_index=True)













