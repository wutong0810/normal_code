# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""



import sys
sys.path.append(r'C:\Users\wutongshu\Desktop\pythonCode')
from allFunc import *




#1.分析车辆统计次数

dataPath=pathGet(path1=r'C:\Users\wutongshu\Desktop\滴滴数据质量评估\0817数据清洗后2.0\0801-0810车牌每天被检测到次数',dataFomat='.csv')
dataFinal=loadData(dataPath)
dataFinal.columns=['year','month','day','car','N']  
#筛选出8月1日至8月9日数据
dataFinal2=dataFinal[(dataFinal.iloc[:,2]>=1)&(dataFinal.iloc[:,2]<=9)&(dataFinal.iloc[:,1]==8)&(dataFinal.iloc[:,0]<=2017)]

#做个排序
dataFinal2=dataFinal2.sort_values(by=["year","month","day","N"],ascending=False)

#统计车牌日均被检测到次数
carDayAvg=dataFinal2.groupby(['car'],as_index=False)['N'].mean()

#按日均被检测到次数拍下序
carTimes=carDayAvg.sort_values(by=["N"],ascending=False)


#得到错误识别车牌
wrongCarNum=carTimes[carTimes.N>600]






#2.评价8月1日的车牌识别次数分布情况
data0801=dataFinal2[(dataFinal2.iloc[:,2]==1)]


#统计每种次数的车牌数量，并做累加
calNum=np.zeros((600,2))
data0801_1=np.array(data0801)
total=0
for i in range(600):
    calNum[i,0]=i
    t=len(data0801_1[data0801_1[:,4]==i])
    total=t+total
    calNum[i,1]=total
    
    
    
    
#绘制检测次数分布图
import matplotlib as mpl
mpl.rc('xtick', labelsize=20) 
mpl.rc('ytick', labelsize=20) 
sns.set_style('white')
sns.set_style("ticks")
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False
fig, ax = plt.subplots(figsize=(19*0.6,9*0.8))
plt.plot(calNum[:,0],calNum[:,1])
plt.xlabel(u'检测次数', fontsize=28)
plt.ylabel(u'累积车辆数', fontsize=28)
ax.set_xscale("log")
plt.savefig(r'd:/deal.jpg',dpi=200)     




#3.统计每天的错误率变化情况
rate=np.zeros((9,2))
for i in range(1,10):
    testMedium=dataFinal2[dataFinal2.iloc[:,2]==i]
    rate[i-1,0]=i
    rate[i-1,1]=len(testMedium)
    num=0
    for j in wrongCarNum:
        tt=testMedium[testMedium.iloc[:,3]==j]['N']
        if len(tt)>0:
            num=num+tt.iloc[0]
    rate[i-1,2]=num
















