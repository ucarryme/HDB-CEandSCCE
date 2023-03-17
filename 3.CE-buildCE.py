import math
import numpy as np
import os
import pandas as pd
import os
import matplotlib.pyplot as plt

#创建文件夹函数
def mkdir(path):

	folder = os.path.exists(path)

	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("---  new folder...  ---")
		print("---  OK  ---")



	else:
		print("---  There is this folder!  ---")

#读取文件夹
path = r"Stress\70%\fix-strain"
dirs = os.listdir(path)
#数据保存文件夹
pathResult = r"CE-build\70%"
#应变速率
𝜀̇ = np.array([0.01,0.1,1,10])

#其实在所读文件中，df.shape[0]就是rates，df.shape[1]就是temperatures
rates = 4
temperatures = 6
#10000倍温度倒数集合
temper = np.array([900,950,1000,1050,1100,1200])
temperX = 10000/(temper+273.15)

#单位J/mol⋅K
R = 8.31

index1 = 𝜀̇
column1 = np.append(-1,temper)

column2 = np.append(-1,𝜀̇)
index2 = temper

column3 = ['k','b','k','b']
index3 = temper
#步长，all values.xlsx文件 行索引命名所用
step = 0.05



n1 = np.zeros((len(dirs),1))
β = np.zeros((len(dirs),1))
α = np.zeros((len(dirs),1))
n = np.zeros((len(dirs),1))
Q = np.zeros((len(dirs),1))
lnA = np.zeros((len(dirs),1))


# ln𝜀̇ = math.log(A) + n1*math.log(σ) - Q/R*T
# ln𝜀̇ = math.log(A) + β*σ - Q/R*T 
#应变速率对数
ln𝜀̇ = np.log(𝜀̇)
#记录文件个数
fileNum = 0
#打开文件循环
for file in dirs:
    print(file)
    nfolder = pathResult+'\\'+file.split('.')[0]+'.'+file.split('.')[1]
    mkdir(nfolder)
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

    arrData1[:,0] = (ln𝜀̇)
    arrData2[:,0] = (ln𝜀̇)

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
    #pd.DataFrame(np.array(arrData1)).to_excel(nfolder+r"\1 lnrate - lnstress from "+file)
    result = pd.DataFrame(np.array(arrData1))
    result.index = index1
    result.columns = column1
    result.to_excel(nfolder+r"\1 lnrate - lnstress of "+file)

    #pd.DataFrame(np.array(arrData2)).to_excel(nfolder+r"\2 lnrate - stres from "+file)
    result = pd.DataFrame(np.array(arrData2))
    result.index = index1
    result.columns = column1
    result.to_excel(nfolder+r"\2 lnrate - stress of "+file)

    result = pd.concat([pd.DataFrame(np.array(k1)),pd.DataFrame(np.array(b1)),pd.DataFrame(np.array(k2)),pd.DataFrame(np.array(b2))],axis=1)
    result.index = index3
    result.columns = column3
    result.to_excel(nfolder+r"\3 k and b from "+file)
    
    #求出本构方程中的n1,β,α,并存储
    n1[fileNum] = 1/np.mean(k1)
    β[fileNum] = 1/np.mean(k2)
    α[fileNum] = β[fileNum]/n1[fileNum]

    #求出本构方程中的n并存储-----------------------------------------------------------------
    #保存对数反三角函数，反三角函数
    arrData3 = np.zeros((rates,temperatures+1))
    arrData3[:,0] = (ln𝜀̇)
     #保存斜率和截距
    length = int(df.shape[1])
    k3 = np.zeros((length,1))
    b3 = np.zeros((length,1))
    for i in range(df.shape[1]):
        
        x1 = ln𝜀̇ 
        #对数反三角函数应力*α
        y = np.log(np.sinh(df.iloc[:,i]*α[fileNum]))

        #存储，以便其他或者检验
        arrData3[:,i+1] = y
        

        # 绘制图形
        
        plt.plot(x1, y, 'o',label="lnsinh⁡(ασ)-ln𝜀̇")
        plt.xlabel("ln𝜀̇") # x轴标签
        plt.ylabel("lnsinh⁡(ασ)") # y轴标签
        # 1. 先拟合获取系数
        z3 = np.polyfit(x1, y,1)
        # 2. 根据系数得到多项式
        p3 = np.poly1d(z3)
        #保存斜率和截距
        print("lnsinh⁡(ασ)-ln𝜀̇{}".format(str(p3)))
        k3[i] =  float(str(p3).split('x')[0])
        strb = str(p3).split('+')[-1]
        strb = str(strb.split('-')[-1])
        b3[i] = float(strb)
        print(b3[i])
        print("lnσ-ln𝜀̇:{}".format(p3))
        # 3. 输入变量(单个值或者变量数组)，得到拟合结果(数组)
        yvals=p3(x1)
        # 4. 根据结果作图
        plt.plot(x1,yvals)
        # 5. 根据原始数据以及拟合数据得到拟合优度
        #rr1 = goodness_of_fit(y_fit_1, y)
        plt.legend()

       

        #作图
        #plt.show()
        
        plt.close('all')
    #计算n
    n[fileNum] = 1/np.mean(k3)

    #pd.DataFrame(np.array(arrData3)).to_excel(nfolder+r"\4 lnrate - lnsinh(stress) from "+file)
    result = pd.DataFrame(np.array(arrData3))
    result.index = index1
    result.columns = column1
    result.to_excel(nfolder+r"\4 lnrate - lnsinh(stress x a) of "+file)

    result = pd.concat([pd.DataFrame(np.array(k3)),pd.DataFrame(np.array(b3))],axis=1)

    result.to_excel(nfolder+r"\5 value n of k and b from "+file)

    #求出本构方程中的Q并存储-----------------------------------------------------------------
    
    arrData4 = np.zeros((temperatures,rates+1))
    arrData4[:,0] = (temperX)
    k4 = np.zeros((rates,1))
    b4 = np.zeros((rates,1))
    for i in range(df.shape[0]) :
        x2 = temperX
        #对数反三角函数应力*α
        y = np.log(np.sinh(df.iloc[i]*α[fileNum]))

        #存储，以便其他或者检验
        arrData4[:,i+1] = y


        plt.plot(x2, y, 'o', label="lnsinh⁡(ασ)-10000/T") # 用虚线绘制
        plt.xlabel("lnsinh⁡(ασ)") # x轴标签
        plt.ylabel("10000/T") # y轴标签
        z4 = np.polyfit(x2, y,1) 
        p4 = np.poly1d(z4)
        k4[i] =  float(str(p4).split('x')[0])
        strb = str(p4).split('+')[-1]
        strb = str(strb.split('-')[-1])
        b4[i] = float(strb)
        print("lnsinh⁡(ασ)-10000/T:{}".format(p4))
        yvals2 = p4(x2)
        plt.plot(x2,yvals2)
        plt.legend()

        #作图
        #plt.show()
    #计算Q,单位kj/mol
    Q[fileNum] = np.mean(k4)*R*n[fileNum]*10*1000
    
    #pd.DataFrame(np.array(arrData4)).to_excel(nfolder+r"\6 lnT-1 - lnsinh(stress) of "+file)
    result = pd.DataFrame(np.array(arrData4))
    result.index = index2
    result.columns = column2
    result.to_excel(nfolder+r"\6 10000T-1 - lnsinh(stress x a) of "+file)
    result = pd.concat([pd.DataFrame(np.array(k4)),pd.DataFrame(np.array(b4))],axis=1)

    result.to_excel(nfolder+r"\7 value Rn needs of k and b from "+file)


    print('α[fileNum])')
    print(float(α[fileNum]))
    #计算lnA-------------------------------------------------------------
    #存储lnA
    arrData5 = np.array([])
    Z = np.array([])
    x = np.array([])
    #列循环
    for i in range(df.shape[1]):
        #一种温度的Z值
        Ztemp = 𝜀̇*np.exp(Q[fileNum]/round(R*(temper[i]+273.15),6))
        #一种温度的横坐标值
        xtemp = np.log(np.sinh(df.iloc[:,i]*α[fileNum]))
        #放入总的数组中
        Z = np.append(Z,Ztemp)
        x = np.append(x,xtemp)
    
    y = np.log(Z)
    #存储
    arrData5 = np.append(arrData5,x)
    arrData5 = np.vstack((arrData5,y))
    print(x,y)
    z4 = np.polyfit(x, y,1) 
    p4 = np.poly1d(z4)
    # k4[i] =  float(str(p4).split('x')[0])
    strb = str(p4).split('+')[-1]
    strb = str(strb.split('-')[-1])
    lnA[fileNum] = float(strb)
    print("lnZ-lnsinh(aσ):{}".format(p4))
    yvals = p4(x)
    plt.plot(x,yvals)
    plt.legend()
    
    result = pd.DataFrame(np.array(arrData5))

    result.to_excel(nfolder+r"\8 lnsinh(stress x a) - lnZ -  from "+file)
    
    # if fileNum is 20:
    #     break
    fileNum+=1
    

result = pd.concat([pd.DataFrame(n1),pd.DataFrame(β),pd.DataFrame(α),pd.DataFrame(n),pd.DataFrame(Q/1000),pd.DataFrame(lnA)],axis= 1)
result.index = [round((x+1)*step,2) for x in range(len(dirs))]
result.columns =['n1','β','α','n','Q(kj/mol)','lnA']
result.to_excel(pathResult+r"\all values.xlsx")
