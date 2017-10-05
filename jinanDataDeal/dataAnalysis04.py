# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""

import sys
sys.path.append(r'C:\Users\wutongshu\Desktop\pythonCode')
from allFunc import *


#1.统计每天有数据的卡口数量
#加载数据
dataPath=pathGet(path1=r'C:\Users\wutongshu\Desktop\滴滴数据质量评估\0817数据清洗后2.0\0801-0816流量按照30min组合\job_id=2745139_dir',dataFomat='.csv')
dataFinal=loadData(dataPath)
dataFinal.columns=['year','month','day','30min','kakou_no','direction','clane','flow'] 




#2.获取所有出现过的卡口数量
kakouAll=set()

for j in range(1,17):
    dataMedium=dataFinal[dataFinal.day==j]
    setMedium=set(zip(dataMedium.kakou_no,dataMedium.direction))
    kakouAll=kakouAll|setMedium
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












#3.运用四分位法，评估卡口数据流量，确保数据未出现较大的问题，先画个图看下30min的数据具有的周期性，




random.seed(60)

testData=dataStoreFinal[dataStoreFinal.ix[:,'30min']==34]
testData.loc[:,'ID']=0

import random
#随机取出50个卡口，来看他们的数据情况
choice=set(zip(dataStoreFinal.kakou_no,dataStoreFinal.direction))
choice1=random.sample(choice,50)

dataFinal=[]
for j,i in enumerate(choice1):
    a=testData[(testData['kakou_no']==i[0])&(testData['direction']==i[1])]
    a.loc[:,'ID']=j
    dataFinal.append(a)

testData1=pd.concat(dataFinal,ignore_index=True)
testData2=testData1[testData1.status==0]






import matplotlib as mpl
mpl.rc('xtick', labelsize=12) 
mpl.rc('ytick', labelsize=12) 

#mpl.rc('xlabel', labelsize=13) 
sns.set_style('white')
sns.set_style("ticks")
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False
#planets = sns.load_dataset("planets")
fig, ax = plt.subplots(figsize=(19*0.6,9*0.8))
sns.boxplot(x=testData2.ID,y=testData2.avg,data=testData2,linewidth = 2.5)
plt.xlabel('kakou_no', fontsize=28)
plt.ylabel('avg', fontsize=28)



plt.savefig(r'd:/deal.jpg',dpi=200) 