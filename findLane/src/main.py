# -*- coding: utf-8 -*-
from allFun.func import *


def main():
    # 加载数据
    dataUp= loadData(path0=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与胜利大街.csv')
    dataDown = loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与纬一路')
    # 处理成5min流量
    dataUpQ=dealToq(dataUp)
    dataDownQ=dealToq(dataDown)
    # 统计各方向的流量
    dataDownDirection=dataDownQ.groupby(by=['year', 'month', 'days', '5min', 'kakou_no', 'direction'])['car'].sum()
    dataDownDirection=dataDownDirection.reset_index()
    # 取出要估计的流量
    dataDownDirection=dataDownDirection[dataDownDirection.iloc[:,5]==2]
    # 将上游流量拼接成一个表
    dataUpQ_deal=pd.pivot_table(dataUpQ,index=["year", "month",'days','5min'],values=['car'],
                  columns=['direction','lane'], aggfunc=[np.mean], fill_value=None)
    dataUpQ_deal.columns = dataUpQ_deal.columns.droplevel([0, 1])
    dataUpQ_deal.columns=[col for col in dataUpQ_deal.columns]
    dataUpQ_deal=dataUpQ_deal.reset_index()
    # 连接两个数据
    dataMerge=pd.merge(dataDownDirection,dataUpQ_deal,on=['year','month','days','5min'])
    # 所有nan填0
    dataMerge=dataMerge.fillna(0)
    # 上游驶入流量统计
    dataMerge['upQ']=dataMerge.iloc[:,7]+dataMerge.iloc[:,10]+dataMerge.iloc[:,11]+dataMerge.iloc[:,12]
    # 排序
    dataMerge=dataMerge.sort_values(by=['year', 'month','days','5min'])
    getPic(data1=dataMerge, start='2017-07-19', end='2017-09-17', path0=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/pic/')
    getResult(data1=dataMerge, start='2017-07-19', end='2017-09-17',path0=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/rmse')


if __name__=='__main__':
    main()






