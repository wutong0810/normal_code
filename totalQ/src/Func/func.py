# -*- coding: utf-8 -*-
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime



def loadData(path0):
    data=pd.read_csv(path0,header=None,encoding='gbk')
    data.columns = ['car', 'brand', 'brand_color', 'car_color', 'kakou_no', 'pass_time', 'speed', 'lane', 'direction',
                    'status', 'location', 'camera', 'year', 'month', 'days']
    # data.pass_time=pd.to_datetime(data.pass_time)
    data.pass_time=data.pass_time.apply(timeChange)
    data.pass_time=pd.to_datetime(data.pass_time)
    return data



#加载数据
def loadDataSum(path1=r'E:\华为数据\测试',dataFomat='.csv'):
    path2=unicode(path1,"utf8")
    filename_total=[]
    for dirpath, dirnames, filenames in os.walk(path2):
        for filename in filenames:
            if os.path.splitext(filename)[1]==dataFomat:
                filename2=os.path.join(dirpath,filename)
                # print filename2
                filename_total.append(filename2)
    dataPath=filename_total
    dataAll=[]
    for i in dataPath:
            dataMedium=pd.read_csv(i,header=None,encoding='gbk')
            dataAll.append(dataMedium)
    dataFinal=pd.concat(dataAll, ignore_index=True)
    # print dataFinal
    dataFinal.columns = ['car', 'brand', 'brand_color', 'car_color', 'kakou_no', 'pass_time', 'speed', 'lane', 'direction',
                    'status', 'location', 'camera', 'year', 'month', 'days']
    # data.pass_time=pd.to_datetime(data.pass_time)
    dataFinal.pass_time=dataFinal.pass_time.apply(timeChange)
    dataFinal.pass_time=pd.to_datetime(dataFinal.pass_time)
    return dataFinal


def timeChange(x):
    if len(x)>13:
        x=x[:19]
    return x


def dealToq(data):
    data['5min']=data.pass_time.apply(lambda x:int((60*x.hour+x.minute)/5))
    data1=data.groupby(['year','month','days','5min','kakou_no','direction','lane'])['car'].count()
    data2=data1.reset_index()
    data2 = data2.sort_values(by=['year', 'month','days','5min','direction','lane'])
    return data2




def filterNoNumber(data):
    wrongNum=["baeae222dee2ddfb39061c657894f7e3", "7b7748694da55437c765243fafa6fd86", "ba36fa139b0b504e2daf19f97e20a27d", "1f30103094eb8554f8709f6407e88e11", "ec9b218ee51d5e9d6532c40e01c90ea6", "41d9529c368ca1c78e86dd005c66da0e", "5cb819160f161a39811ee6c825563e0c", "b64a2ffff8d1533a55b52ced11292c22", "83ffc260ca9203488a118e94f09eb74e", "de55f16c88bc1c03cf299554a556cddf", "4e4d227f5bfa46fa62934f1f7be19bd6", "837926f65b113a7d6ece54daf66fa862", "8eeb6fc1d1a2ac93b457f4e6de127ae8", "20a9de14eab1fe808533cd1854e95dba", "4ff052240a84a5a688215277d1444a2b", "7b397938e768f04d32ecb7800e911d6e", "df7887942290de8ef7b43d9904896dda", "8a524c0f84ead9cf792751d4de2d9199", "e42e9ee7558546b87d9ecc7b6de82fc0", "c563b33db3136bcb64394eed22e4310d", "534b3f735a2980d6541c39645664f561", "fbfbb6a8c5c5ed9116191a0f06ab16ea", "10c92094d3975fcf83873b624ec25f76", "03e6d36942e3e23f34d6df7a6489765d", "2cce0d1cf4e74da57bf81b0056eacf24", "3d1403e1c924352c298056f29b0391d3", "6d47eb73ecbf83333be48397ae998e2d", "7424c28d60eade998c3427a015a4164e", "a728c2ee1ca63ee78048cc92edbe4d9a", "cf7c1b9122c6f6eacd44026d7688fbe7", "a84854b03183b1e948d421329d8bb38f", "0fa4d253cd2372f3cc3b5d7a33c93668", "69e51da96d2ad4958346717b8acc3e2f", "571df8148bff40dc81cc0fb0fa1f1500", "e48eb94556a75618a74879d577f37aff"]
    dataFilter=data[~data.iloc[:,0].isin(wrongNum)]
    return dataFilter


def getPic(data1,start,end,path0):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    for i in date_generated:
        data=data1[(data1.iloc[:,0]==i.year)&(data1.iloc[:,1]==i.month)&(data1.iloc[:,2]==i.day)]
        if len(data)>0:
            fig,ax=plt.subplots(figsize=(5,5))
            plt.plot(data.iloc[:,3],data.iloc[:,6],'-',label=u'true')
            plt.plot(data.iloc[:,3], data.iloc[:,-1],'--', label=u'estimate')
            plt.legend()
            path1=path0+str(i.year)+str(i.month)+str(i.day)+'.png'
            plt.savefig(path1)
            plt.close(fig)


def upArrival(data,loadLength,v1,upIn):
    data=data.assign(direction_lane=zip(data.iloc[:,8],data.iloc[:,7]))
    data=data[data.iloc[:,-1].isin(upIn)]
    data.pass_time=data.pass_time+int(loadLength/v1*3.6)*datetime.timedelta(seconds=1)
    data1=data.iloc[:,:-1]
    return data1





def getResult(data1,start,end,path0):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    with open(path0, 'w') as f:
        for i in date_generated:
            data=data1[(data1.iloc[:,0]==i.year)&(data1.iloc[:,1]==i.month)&(data1.iloc[:,2]==i.day)]
            if len(data)>0:
                rmse=np.sqrt(np.sum((data.iloc[:,-1]-data.iloc[:,6])**2)/len(data))
                f.writelines(str(i.year)+','+str(i.month)+','+str(i.day)+','+str(rmse)+'\n')


if __name__=="__main__":
    dataUp= loadData(path0=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与胜利大街.csv')
    dataDown = loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与纬一路')
    # 处理成5min流量
    dataUp1=upArrival(data=dataUp,loadLength=0.236,v1=15,upIn=[(1,1),(2,1),(2,2),(2,3)])
    dataUpQ=dealToq(dataUp1)
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