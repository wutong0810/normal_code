# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 12:00:00 2017

@author: wutongshu
"""
# /Users/wutongshu/Documents/spark/testdata2/num/

from src.myPackage.allfun import *


def getWrongNum(path0=r'/Users/wutongshu/Documents/spark/testdata2/num1/sd'):
    dataFinal=pd.read_csv(path0,header=None)
    dataFinal.columns=['year','month','day','car','N']
    # print dataFinal
    #统计车牌日均被检测到次数
    carTimes=dataFinal.groupby(['car'],as_index=False)['N'].mean()
    #得到错误识别车牌
    wrongCarNum=carTimes[carTimes.N>600]
    return list(wrongCarNum.car)



if __name__=='__main__':
    print getWrongNum()

