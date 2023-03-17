import math
import numpy as np
import os
import pandas as pd
import os
import matplotlib.pyplot as plt



#读取文件夹
path = r"E:\learning\VSCode+python\python\hot deform beh\Stress\70%\fix-strain"
dirs = os.listdir(path)
#数据保存文件夹
pathResult = r"E:\learning\VSCode+python\python\hot deform beh\CE-build\70%"
#应变速率
𝜀̇ = np.array([0.01,0.1,1,10])

#其实在所读文件中，df.shape[0]就是rates，df.shape[1]就是temperatures
rates = 4
temperatures = 6

A = 10
F = 10
Q = 10
R = 10
T = 10
n = 10
n1 = np.zeros((len(dirs),1))
β = np.zeros((len(dirs),1))
α = np.zeros((len(dirs),1))
σ = 10

# ln𝜀̇ = math.log(A) + n1*math.log(σ) - Q/R*T
# ln𝜀̇ = math.log(A) + β*σ - Q/R*T 
#应变速率对数
ln𝜀̇ = np.log(𝜀̇)
#记录文件个数
fileNum = 0
#打开文件循环
for file in dirs:
    print(file)
    #打开文件
    df = pd.read_excel(path+"\\"+file)
    #保存斜率和截距
    length = int(df.shape[1])
    k1 = np.zeros((length,1))
    b1 = np.zeros((length,1))
    k2 = np.zeros((length,1))
    b2 = np.zeros((length,1))
    #保存对数应力和应力
    arrData1 = np.zeros((rates,temperatures+1))
    arrData2 = np.zeros((rates,temperatures+1))
    #保存对数反三角函数，反三角函数
    arrData3 = np.zeros((rates,temperatures+1))
    arrData4 = np.zeros((rates,temperatures+1))
    arrData1[:,0] = (ln𝜀̇)
    arrData2[:,0] = (ln𝜀̇)
    arrData3[:,0] = (ln𝜀̇)
    arrData4[:,0] = (ln𝜀̇)
    #求出本构方程中的n1,β,α,-----------------------------------------------------------------------------
    #列循环
    for i in range(df.shape[1]):
        
        x = ln𝜀̇ 
        #对数应力
        y1 = np.log(df.iloc[:,i])
        #应力
        y2 = df.iloc[:,i]
        #存储，以便其他或者检验
        arrData1[:,i+1] = y1
        arrData2[:,i+1] = y2

        # 绘制图形
        plt.subplot(1,2,1)
        plt.plot(x, y1, 'o',label="lnσ-ln𝜀̇")
        plt.xlabel("ln𝜀̇") # x轴标签
        plt.ylabel("lnσ") # y轴标签
        # 1. 先拟合获取系数
        z1 = np.polyfit(x, y1,1)
        # 2. 根据系数得到多项式
        p1 = np.poly1d(z1)
        #保存斜率和截距
        k1[i] =  float(str(p1).split('x')[0])
        b1[i] = float(str(p1).split('+')[1])
        print(b1[i])
        print("lnσ-ln𝜀̇:{}".format(p1))
        # 3. 输入变量(单个值或者变量数组)，得到拟合结果(数组)
        yvals=p1(x)
        # 4. 根据结果作图
        plt.plot(x,yvals)
        # 5. 根据原始数据以及拟合数据得到拟合优度
        #rr1 = goodness_of_fit(y_fit_1, y)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(x, y2, 'o', label="σ-ln𝜀̇") # 用虚线绘制
        plt.xlabel("ln𝜀̇") # x轴标签
        plt.ylabel("σ") # y轴标签
        z2 = np.polyfit(x, y2,1) 
        p2 = np.poly1d(z2)
        k2[i] =  float(str(p2).split('x')[0])
        b2[i] = float(str(p2).split('+')[1])
        print("σ-ln𝜀̇:{}".format(p2))
        yvals2 = p2(x)
        plt.plot(x,yvals2)
        plt.legend()


        #作图
        #plt.show()
        
        plt.close('all')
    pd.DataFrame(np.array(arrData1)).to_excel(pathResult+r"\lnrate - lnstress of "+file)
    pd.DataFrame(np.array(arrData2)).to_excel(pathResult+r"\lnrate - stres of "+file)
    
    result = pd.concat([pd.DataFrame(np.array(k1)),pd.DataFrame(np.array(b1)),pd.DataFrame(np.array(k2)),pd.DataFrame(np.array(b2))],axis=1)
    #result = pd.DataFrame(np.array(arrAll))
    result.to_excel(pathResult+r"\k and b of "+file)
    
    #求出本构方程中的n1,β,α,并存储
    n1[fileNum] = 1/np.mean(k1)
    β[fileNum] = 1/np.mean(k2)
    α[fileNum] = β[fileNum]/n1[fileNum]
    # #求出本构方程中的n,Q并存储-----------------------------------------------------------------
    # for i in range(df.shape[1]):
        
    #     x = ln𝜀̇ 
    #     #对数反三角函数应力*α
    #     y1 = np.log(np.sinh(df.iloc[:,i]*α[fileNum]))
    #     #反三角函数应力*α
    #     y2 = np.sinh(df.iloc[:,i]*α[fileNum])
    #     #存储，以便其他或者检验
    #     arrData1[:,i+1] = y1
    #     arrData2[:,i+1] = y2

    #     # 绘制图形
    #     plt.subplot(1,2,1)
    #     plt.plot(x, y1, 'o',label="lnσ-ln𝜀̇")
    #     plt.xlabel("ln𝜀̇") # x轴标签
    #     plt.ylabel("lnσ") # y轴标签
    #     # 1. 先拟合获取系数
    #     z1 = np.polyfit(x, y1,1)
    #     # 2. 根据系数得到多项式
    #     p1 = np.poly1d(z1)
    #     #保存斜率和截距
    #     k1[i] =  float(str(p1).split('x')[0])
    #     b1[i] = float(str(p1).split('+')[1])
    #     print(b1[i])
    #     print("lnσ-ln𝜀̇:{}".format(p1))
    #     # 3. 输入变量(单个值或者变量数组)，得到拟合结果(数组)
    #     yvals=p1(x)
    #     # 4. 根据结果作图
    #     plt.plot(x,yvals)
    #     # 5. 根据原始数据以及拟合数据得到拟合优度
    #     #rr1 = goodness_of_fit(y_fit_1, y)
    #     plt.legend()

    #     plt.subplot(1, 2, 2)
    #     plt.plot(x, y2, 'o', label="σ-ln𝜀̇") # 用虚线绘制
    #     plt.xlabel("ln𝜀̇") # x轴标签
    #     plt.ylabel("σ") # y轴标签
    #     z2 = np.polyfit(x, y2,1) 
    #     p2 = np.poly1d(z2)
    #     k2[i] =  float(str(p2).split('x')[0])
    #     b2[i] = float(str(p2).split('+')[1])
    #     print("σ-ln𝜀̇:{}".format(p2))
    #     yvals2 = p2(x)
    #     plt.plot(x,yvals2)
    #     plt.legend()


    #     #作图
    #     #plt.show()
        
    #     plt.close('all')


    fileNum+=1


    break
