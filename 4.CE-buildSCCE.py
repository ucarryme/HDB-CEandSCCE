import os
import numpy as np
import pandas as pd

path = r'SCCE-build\verify\70%\commonData.xlsx'
pathResult = r'SCCE-build\verify\70%\result'


#行索引
rates = [0.01,0.1,1,10]
#列索引
temper = [900,950,1000,1050,1100,1200]
#列单元的列数
cols = 2

R = 8.31
df = pd.read_excel(path)

#行循环
for i in range(len(rates)):
    #申请一个数组，放每一种速率下的每个应力点
    arrData = np.zeros((df.shape[0],len(temper)*cols))
    #数组的列索引
    k = 0
    #行循环
    for j in range(len(temper)):
        #每个列单元的第一列装应力点，0.05，0.1，0.15.....
        arrData[:,k] = df.iloc[:,0]
        #Z值计算
        Z = rates[i]*(np.exp(df.iloc[:,3]*1000/round(R*(temper[j]+273.15),4)))
        #Z除A
        ZdivA = Z/np.exp(df.iloc[:,4])
        part1 = (ZdivA)**(1/df.iloc[:,2])
        part2 = ((ZdivA)**(2/df.iloc[:,2])+1)**(1/2)
        #列单元的第二行装计算值
        arrData[:,k+1] = (1/df.iloc[:,1])*(np.log(part1+part2))
        print(df.iloc[:,3]*1000/(R*(temper[j]+273.15)))
        print(ZdivA)
        print(round(R*(temper[j]+273.15),4))
        #维持数组的列索引
        k +=2
        
    
    
    result = pd.DataFrame(arrData)
    result.to_excel(pathResult+r'\{}'.format(rates[i])+'.xlsx')

    #
    #
    


