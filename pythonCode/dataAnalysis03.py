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

#加载完数据统计每天有数据的卡口数量
kakouN=np.zeros((16,2))
for i in range(1,17):
    dataMedium=dataFinal[dataFinal.day==i]
    kakouN[i-1,0]=i
    kakouN[i-1,1]=len(dataMedium.kakou_no.unique())
    
#统计出现过的卡口id，并建一个所有出现过卡口的DataFrame
kakouAll=set()
for i in range(1,17):
    dataMedium=dataFinal[dataFinal.day==i]
    kakouAll=kakouAll|(set(dataMedium.kakou_no.unique()))


kakouAll1=np.array(list(kakouAll))
kakouAll2=np.tile(kakouAll1,48)

kakouAll2=pd.DataFrame(kakouAll2)
kakouAll2['30min']=np.tile(range(1,49),len(kakouAll1))

kakouAll2.columns=['kakou_no','30min']



    
    
#2.统计下多天数据变化情况图，因为各个卡口车道数量不一致，因此需归一化数据，即计算每个设备点各车道的平均流量。
#并且将数据保存在dataStore这个list里面
for i in range(1,12):
    dataMedium=dataFinal[dataFinal.day==i]
#    统计得到每个卡口的车道数
    claneTotal=dataMedium.groupby([dataMedium['kakou_no'],dataMedium['direction']])['clane'].nunique()
    claneTotal2=claneTotal.reset_index()
    claneTotal3=claneTotal2.groupby([claneTotal2['kakou_no']])['clane'].sum()
    claneTotal3=claneTotal3.reset_index()
#    统计得到半小时为颗粒度的流量总和
    kakouQ=dataMedium.groupby([dataMedium['kakou_no'],dataMedium['30min']])['flow'].sum()
    kakouQ=kakouQ.reset_index()
    dataFinal2=pd.merge(kakouQ,claneTotal3,on='kakou_no')
#    计算每个卡口点位的平均单车道的流量
    dataFinal2['avg']=dataFinal2['flow']/dataFinal2['clane']
    dataFinal3=pd.merge(kakouAll2,dataFinal2,how='left',on=['kakou_no','30min'])
#    绘制流量热力图
    import matplotlib as mpl
    mpl.rc('xtick', labelsize=13) 
    mpl.rc('ytick', labelsize=13) 

    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False
    cmap=sns.light_palette("navy",as_cmap = True)
    #cmap=sns.cubehelix_palette(rot=-.0)
    #cmap=sns.color_palette("Blues",as_cmap = True)
    aa=dataFinal3.pivot('kakou_no', "30min", 'avg')
    aa.index=range(len(aa))
    aa.columns=[x/2 for x in range(48)]
    
    f, ax = plt.subplots(figsize=(16, 9))
    sns.heatmap(aa, annot=False, fmt="d", cmap='rainbow',ax=ax,vmax=700,vmin=0,yticklabels=40,xticklabels=2)
    ax.set_xlabel(u'时间（单位：小时）')
    ax.set_ylabel(u'卡口点位')
    path1=r'D:/didiScript/picture/'+str(800+i)+'.jpg'
    plt.savefig(path1,dpi=200) 




#3.分析数据中异常成分，为了更为精细化地评估各交叉口各点位的实际情况，因此这里采取分方向来分析
#统计出现过的卡口id，并建一个所有出现过卡口和方向的DataFrame
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












#创造一个array,记录数据的异常数据分布情况,第1列是较大的值得个数，第2列是数据为0的个数（6点前的），第3列是数据为0的个数，且为6点后的
dataAbnormal=np.zeros((11,3))

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
#    将超过最大通行能力的值取1,
    dataFinal3.loc[dataFinal3.iloc[:,-2]>750,'status']=1
#    将数据为0的数据处理为状态值取2
    dataFinal3.loc[dataFinal3.iloc[:,-2]==0,'status']=2
#    统计有多少个异常大的值
    dataAbnormal[i-1,0]=len(dataFinal3[dataFinal3.loc[:,'status']==1])
#    统计有多少个为空值的时间段，因为数据为空，可能是由于凌晨导致没车，而不是未上传数据，因此分时段统计下，分为6点前和6点后
    dataAbnormal[i-1,1]=len(dataFinal3[(dataFinal3.loc[:,'status']==2)&((dataFinal3.loc[:,'30min']<=12))])
    dataAbnormal[i-1,2]=len(dataFinal3[(dataFinal3.loc[:,'status']==2)&((dataFinal3.loc[:,'30min']>=12))])
    dataStore.append(dataFinal3)
dataStoreFinal=pd.concat(dataStore, ignore_index=True)
    
    
#统计各个卡口的设备状况,统计数据
kakouStatus=dataStoreFinal.groupby(['kakou_no','direction','30min'])['status'].value_counts()    
kakouStatus2=pd.DataFrame(kakouStatus)
kakouStatus2.columns=['N']  
kakouStatus2=kakouStatus2.reset_index()   



#分析各个卡口的具体状态，统计8月1日-8月11日，卡口正常的百分比率
kakouStatusSum=kakouStatus2.groupby(by=['kakou_no','direction','status'],as_index=False)['N'].sum()
kakouStatusSum['statusTotal']=48*11
kakouStatusSum['statusRate']=kakouStatusSum['N']/kakouStatusSum['statusTotal']


#取出所有的可能取值，防止后面由于没有这个值聚合时，导致数据计算平均不准确
kakouDirection=kakouStatusSum.ix[:,['kakou_no','direction']].drop_duplicates()

kakouDirection1=pd.concat([kakouDirection]*4,ignore_index=True)
kakouDirection1['status']=0
for i in range(4):
    kakouDirection1.iloc[len(kakouDirection)*i:len(kakouDirection)*(i+1),-1]=i

#左连接所有可能取值
kakouStatusSum2=pd.merge(kakouDirection1,kakouStatusSum,on=['kakou_no','direction','status'],how='left')
#对结果进行排序，对将nan值填0
kakouStatusSum2=kakouStatusSum2.sort_values(by=['kakou_no','direction','status'])
kakouStatusSum2.statusRate=kakouStatusSum2.statusRate.fillna(0)

#提取每个卡口的状态，这里直接将各方向的正常率取平均
kakouStatusSum3=kakouStatusSum2.groupby(by=['kakou_no','status'],as_index=False)['statusRate'].mean()

#得到卡口正常状态下的比例
kakouStatusSum4=kakouStatusSum3[kakouStatusSum3.ix[:,'status']==0]


kakouLongLat=pd.read_csv(r'C:\Users\wutongshu\Desktop\pythonCode\kakou_longlat.csv')




kakouStatusSum5=pd.merge(kakouStatusSum4,kakouLongLat,on='kakou_no',how='left')


kakouStatusSum6=kakouStatusSum5[kakouStatusSum5.X>0]




kakouStatusSum6.to_csv(r'C:\Users\wutongshu\Desktop\pythonCode\kakou_sum.csv')




#分析下各卡口，全天的总流量，这里以8月1号单独分析




















