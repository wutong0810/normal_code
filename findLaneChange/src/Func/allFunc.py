# -*- coding: utf-8 -*-
import pandas as pd
import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

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


def matchData(upLoad, downLoad, maxtime, mintime, downDirection):
    downLoadDirection=downLoad[downLoad.iloc[:,8]==downDirection]
    downLoadDirection=downLoadDirection.iloc[:,[0,5,7,8]]
    downLoadDirection=filterNoNumber(downLoadDirection)
#初始化最终的大矩阵match_du，上游的车牌先进行排序
    downLoadDirectionnp=np.array(downLoadDirection)
    downLoadDirection=downLoadDirection.assign(up_t=np.nan)
    downLoadDirection=downLoadDirection.assign(up_clane=np.nan)
    downLoadDirection=downLoadDirection.assign(up_direct=np.nan)
    downLoadDirection=downLoadDirection.assign(tt=0)
    match_du=np.array(downLoadDirection)
    upLoad=upLoad.sort_values(by=upLoad.columns[5])
    uploadnp=np.array(upLoad)
#    搜索上游在合理时间范围内的车牌数据
    for i in range(len(downLoadDirectionnp)):
        # print downLoadDirectionnp[i,1]
        t_min=downLoadDirectionnp[i,1]-(maxtime*datetime.timedelta(seconds=1))
        t_max=downLoadDirectionnp[i,1]-(mintime*datetime.timedelta(seconds=1))
        up_medium=uploadnp[(uploadnp[:,5]>t_min)&(uploadnp[:,5]<t_max)]
        m=len(up_medium)
#       如果存在，则匹配车牌信息，并计算行程时间，一旦匹配上则跳出循环
        if m>0:
            for j in range(m):
                if (cmp(match_du[i,0],up_medium[j,0])==0):
                    match_du[i,4]=up_medium[j,5]
                    match_du[i,5]=up_medium[j,7]
                    match_du[i,6]=up_medium[j,8]
                    match_du[i,7]=(match_du[i,1]-up_medium[j,5]).total_seconds()
                    break
#    将匹配好的大矩阵按车牌，和下游过程时刻排序，去掉重复匹配的车牌
    match_time=pd.DataFrame(match_du)
    match_time=match_time.sort_values(by=[0,1])
    match_time.index=range(len(match_time))
    match_time1=np.array(match_time)
    indice=[]
# 阈值设置为100s
    for h in range(1,len(match_time1)):
        if (cmp(match_time1[h,0],match_time1[h-1,0])==0)&( (match_time1[h,1]-match_time1[h-1,1]).total_seconds()<100):
            indice.append(h-1)
#给行程时间付上-1来标示行程时间
    for i in indice:
        match_time1[i,-1]=-1
#筛选出正常的数据
    match_time2=match_time1[match_time1[:,-1]>-1]
    match_tt=pd.DataFrame(match_time2)
#重新按下游过车时刻来排序
    match_tt=match_tt.sort_values(by=[1,0])
#    计算下匹配率
    match_final=match_tt[match_tt.iloc[:,-1]>0]
    match_final.columns=['car_num','d_time','d_clane','d_direction','u_time','u_clane','u_direction','tt']
    return match_tt,match_final

def dealToq5min(data,dire,timeR):
    name = str(timeR) + 'min'
    data[name]=data.pass_time.apply(lambda x:int((60*x.hour+x.minute)/timeR))
    data1=data.groupby(['year','month','days',name,'kakou_no','direction','lane'])['car'].count()
    data2=data1.reset_index()
    data2 = data2.sort_values(by=['year', 'month','days',name,'direction','lane'])
    data2 =data2[data2.direction==dire]
    data2=pd.pivot_table(data2,index=["year", "month",'days',name],values=['car'],columns=['lane'], aggfunc=[np.mean], fill_value=0)
    data2=data2.reset_index()
    data2.columns=data2.columns.droplevel([0])
    data2=data2.assign(totalq=(np.sum(data2.iloc[:,-5:],axis=1)))
    data2 = data2.assign(lane1=(data2.iloc[:,4]+data2.iloc[:, 5])/data2.iloc[:,9])
    data2 = data2.assign(lane2=(data2.iloc[:,6]) /data2.iloc[:, 9])
    data2['sameTime'] =data2.iloc[:,3].apply(lambda x:x*(timeR/5))
    # data2['timeFormat']=data2.iloc[:,3].apply(lambda x:((datetime.timedelta(minutes=timeR)*int(x)+datetime.datetime.strptime('00:00:00', '%H:%M:%S')).time()))
    # .strftime("%H:%M")
    # data2 = data2.assign(timeChange=((datetime.timedelta(minutes=timeR)*data2.iloc[:,3]+datetime.datetime.strptime('00:00:00', '%H:%M:%S')).time()).strftime("%H:%M:%S"))
    return data2


def getAllData():
    data1 = loadData(path0=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与胜利大街.csv')
    data2 = loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与纬一路')
    data1_1=dealToq(data1)
    data2_1=dealToq(data2)
    dataFinal=pd.concat([data1_1,data2_1])
    return dataFinal


def filterNoNumber(data):
    wrongNum=["baeae222dee2ddfb39061c657894f7e3", "7b7748694da55437c765243fafa6fd86", "ba36fa139b0b504e2daf19f97e20a27d", "1f30103094eb8554f8709f6407e88e11", "ec9b218ee51d5e9d6532c40e01c90ea6", "41d9529c368ca1c78e86dd005c66da0e", "5cb819160f161a39811ee6c825563e0c", "b64a2ffff8d1533a55b52ced11292c22", "83ffc260ca9203488a118e94f09eb74e", "de55f16c88bc1c03cf299554a556cddf", "4e4d227f5bfa46fa62934f1f7be19bd6", "837926f65b113a7d6ece54daf66fa862", "8eeb6fc1d1a2ac93b457f4e6de127ae8", "20a9de14eab1fe808533cd1854e95dba", "4ff052240a84a5a688215277d1444a2b", "7b397938e768f04d32ecb7800e911d6e", "df7887942290de8ef7b43d9904896dda", "8a524c0f84ead9cf792751d4de2d9199", "e42e9ee7558546b87d9ecc7b6de82fc0", "c563b33db3136bcb64394eed22e4310d", "534b3f735a2980d6541c39645664f561", "fbfbb6a8c5c5ed9116191a0f06ab16ea", "10c92094d3975fcf83873b624ec25f76", "03e6d36942e3e23f34d6df7a6489765d", "2cce0d1cf4e74da57bf81b0056eacf24", "3d1403e1c924352c298056f29b0391d3", "6d47eb73ecbf83333be48397ae998e2d", "7424c28d60eade998c3427a015a4164e", "a728c2ee1ca63ee78048cc92edbe4d9a", "cf7c1b9122c6f6eacd44026d7688fbe7", "a84854b03183b1e948d421329d8bb38f", "0fa4d253cd2372f3cc3b5d7a33c93668", "69e51da96d2ad4958346717b8acc3e2f", "571df8148bff40dc81cc0fb0fa1f1500", "e48eb94556a75618a74879d577f37aff"]
    dataFilter=data[~data.iloc[:,0].isin(wrongNum)]
    return dataFilter



def getPic(data1,data2,data3,start,end,path0):

    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    for i in date_generated:
        data1_1=data1[(data1.iloc[:,0]==i.year)&(data1.iloc[:,1]==i.month)&(data1.iloc[:,2]==i.day)]
        data2_1 = data2[(data2.iloc[:, 0] == i.year) & (data2.iloc[:, 1] == i.month) & (data2.iloc[:, 2] == i.day)]
        data3_1 = data3[(data3.iloc[:, 0] == i.year) & (data3.iloc[:, 1] == i.month) & (data3.iloc[:, 2] == i.day)]
        if len(data1_1)>0:
            fig,ax=plt.subplots(figsize=(15,10))
            plt.plot(data1_1.iloc[:,-1],data1_1.iloc[:,10],'o--',label=u'5min_lane1')
            plt.plot(data1_1.iloc[:,-1], data1_1.iloc[:,11],'-',label=u'5min_lane2')
            plt.plot(data2_1.iloc[:,-1],data2_1.iloc[:,10],'o--',label=u'30min_lane1')
            plt.plot(data2_1.iloc[:,-1], data2_1.iloc[:,11],'-',label=u'30min_lane2')
            plt.plot(data3_1.iloc[:,-1],data3_1.iloc[:,10],'o--',label=u'60min_lane1')
            plt.plot(data3_1.iloc[:,-1], data3_1.iloc[:,11],'-',label=u'60min_lane2')
            plt.legend(loc='lower left')
            path1=path0+str(i.year)+str(i.month)+str(i.day)+'.png'
            # print path1
            plt.xlim(0,288)
            plt.ylim(0,1)
            plt.savefig(path1,dpi=200)
            plt.show()
            plt.close(fig)



def getPic2(data1,data2,data3,start,end,path0):

    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    fig, ax = plt.subplots(figsize=(15, 10))
    for i in date_generated:
        data1_1=data1[(data1.iloc[:,0]==i.year)&(data1.iloc[:,1]==i.month)&(data1.iloc[:,2]==i.day)]
        data2_1 = data2[(data2.iloc[:, 0] == i.year) & (data2.iloc[:, 1] == i.month) & (data2.iloc[:, 2] == i.day)]
        data3_1 = data3[(data3.iloc[:, 0] == i.year) & (data3.iloc[:, 1] == i.month) & (data3.iloc[:, 2] == i.day)]
        label1=str(i.year)+str(i.month)+str(i.day)+'30min_lane1'
        # label2=str(i.year)+str(i.month)+str(i.day)+'30min_lane2'
        if len(data2_1)>0:
            plt.plot(data2_1.iloc[:,-1],data2_1.iloc[:,10],'o--',label=label1)
            # plt.plot(data2_1.iloc[:,-1], data2_1.iloc[:,11],'-',label=label2)
            # plt.plot(data2_1.iloc[:,-1],data2_1.iloc[:,10],'o--',label=u'30min_lane1')
            # plt.plot(data2_1.iloc[:,-1], data2_1.iloc[:,11],'-',label=u'30min_lane2')
            # plt.plot(data3_1.iloc[:,-1],data3_1.iloc[:,10],'o--',label=u'60min_lane1')
            # plt.plot(data3_1.iloc[:,-1], data3_1.iloc[:,11],'-',label=u'60min_lane2')
    plt.legend(loc='lower left')
    path1=path0+str(i.year)+str(i.month)+str(i.day)+'.png'
    # print path1
    plt.xlim(0,288)
    plt.ylim(0,1)
    plt.savefig(path1,dpi=200)
    plt.show()
    plt.close(fig)



if __name__=="__main__":
    downData=loadDataSum(path1=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/查询结果文件/经八路与纬一路')
    downDataQ5min=dealToq5min(downData,dire=2,timeR=5)
    downDataQ30min = dealToq5min(downData, dire=2, timeR=30)
    downDataQ60min = dealToq5min(downData, dire=2, timeR=60)
    getPic2(downDataQ5min,downDataQ30min,downDataQ60min,'2017-08-15','2017-08-23',path0=r'/Users/wutongshu/Desktop/济南市交叉口电警流量补全/转向比变化图历史/')







