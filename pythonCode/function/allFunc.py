# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

#读取所有文件路径
def pathGet(path1=r'E:\华为数据\测试',dataFomat='.txt'):
    path2=unicode(path1,"utf8")
    filename_total=[]
    for dirpath, dirnames, filenames in os.walk(path2):
        for filename in filenames:
            if os.path.splitext(filename)[1]==dataFomat:
                filename2=os.path.join(dirpath,filename)
    #            print filename2
                filename_total.append(filename2) 
    return filename_total

#加载数据
def loadData(dataPath):
    dataAll=[]
    for i in dataPath:
            dataMedium=pd.read_csv(i,header=None)
            dataAll.append(dataMedium)
    dataFinal=pd.concat(dataAll, ignore_index=True)
    return dataFinal




def boxFilter(data,Num=6,valueRange=30):
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












