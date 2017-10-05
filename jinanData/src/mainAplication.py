
from myPackage.range import *
from myPackage.allfun import *

def wrongRate(path0=r'/Users/wutongshu/Documents/spark/testdata2/num1/sd',path1=r'/Users/wutongshu/Documents/spark/testdata2/num1/sd'):
    wrongNum=getWrongNum(path0=path0)
    # print wrongNum
    data=pd.read_csv(path1,header=None)
    allNum=np.sum(data.iloc[:,4])
    # print allNum
    wrongNum=wrongNumTotal(data=data,wrongCarNum=wrongNum)
    return float(wrongNum)/allNum








def main():
    a=wrongRate()
    print a


if __name__=='__main__':
    main()

