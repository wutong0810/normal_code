# -*- coding: utf-8 -*-
import sys

from Parse.parse import *


def main(path1,timeNow,path2):
    # 解析所有数据
    data=parseData(path=path1)
    # 处理成30min
    data=parseTo30min(data)
    # 获取所有出现过的卡口和方向
    kakouId=np.load(path2)
    kakou=getAllKakou(data,kakouId)
    # 对初始数据进行标记
    data2= getLabel(data,kakou)
    # 获取阈值范围
    data3=getDataRange(data2,num1=16,valueRange1=40)
    # 输出前一天的数据
    data4=getToday(timeNow,data3)
    return data4









if __name__=="__main__":
    # data=main(r'/Users/wutongshu/Documents/日常下载/test.0','2017-08-05','/Users/wutongshu/Desktop/kakouInfo2.npy')

    data=main(sys.argv[1],sys.argv[2],sys.argv[3])
    data.to_csv(sys.argv[4],sep='\t',header=None,index=None)
    writeData(data)
