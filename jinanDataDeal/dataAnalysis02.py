# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""



import sys
sys.path.append(r'C:\Users\wutongshu\Desktop\pythonCode')
from allFunc import *







#1.车身颜色

dataPath1=pathGet(path1=r'C:\Users\wutongshu\Desktop\最新数据质量评估报告\0801车身颜色',dataFomat='.csv')

carColor=loadData(dataPath1)

carColor.columns=['year','month','day','car','color','N']
#统计总量
carTotal=carColor.groupby(['car'],as_index=False)['N'].sum()
#统计识别最大概率颜色
carMax=carColor.groupby(['car'],as_index=False)['N'].max()
#计算颜色的识别正确率
rate1=float(np.sum(carMax.N))/np.sum(carTotal.N)





#2.车牌颜色

dataPath2=pathGet(path1=r'C:\Users\wutongshu\Desktop\最新数据质量评估报告\0801车牌颜色识别',dataFomat='.csv')

brandColor=loadData(dataPath2)

brandColor.columns=['year','month','day','car','color','N']
#统计总量
carTotal=brandColor.groupby(['car'],as_index=False)['N'].sum()
#统计识别最大概率颜色
carMax=brandColor.groupby(['car'],as_index=False)['N'].max()
#计算颜色的识别正确率
rate2=float(np.sum(carMax.N))/np.sum(carTotal.N)






#3.车辆品牌

dataPath3=pathGet(path1=r'C:\Users\wutongshu\Desktop\最新数据质量评估报告\0801检测到车辆品牌',dataFomat='.csv')

brand=loadData(dataPath3)

brand.columns=['year','month','day','car','color','N']
#统计总量
carTotal=brand.groupby(['car'],as_index=False)['N'].sum()
#统计识别最大概率颜色
carMax=brand.groupby(['car'],as_index=False)['N'].max()
#计算颜色的识别正确率
rate3=float(np.sum(carMax.N))/np.sum(carTotal.N)