# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""



import sys
# sys.path.append(r'C:\Users\wutongshu\Desktop\pythonCode')
from allFunc import *




dataPath=pathGet(path1=r'C:\Users\wutongshu\Desktop\滴滴数据质量评估\0817数据清洗后2.0\0801-0810车牌每天被检测到次数',dataFomat='.csv')
dataFinal=loadData(dataPath)
dataFinal.columns=['year','month','day','car','N']   
dataFinal=dataFinal[(dataFinal.iloc[:,2]>=1)&(dataFinal.iloc[:,2]<=9)&(dataFinal.iloc[:,1]<=8)&(dataFinal.iloc[:,0]<=2017)]
