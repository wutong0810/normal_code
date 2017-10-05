from my_package1.dealData import *


def main():
    data1=loadData(r'/Users/wutongshu/Documents/testQdata/kakou3701022131.csv')
    data2=loadDataSum(path1=r'/Users/wutongshu/Documents/testQdata/kakou3701022129')
    data3=loadDataSum(path1=r'/Users/wutongshu/Documents/testQdata/kakou3701022130')
    data1_q=dealToq(data1)
    data2_q=dealToq(data2)
    data3_q=dealToq(data3)


if __name__=='__main__':
