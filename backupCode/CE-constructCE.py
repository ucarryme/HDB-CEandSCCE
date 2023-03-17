import math
import numpy as np
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg') 


path = r"E:\learning\VSCode+python\python\hot deform beh\Stress\70%\fix-strain"
dirs = os.listdir(path)

𝜀̇ = np.array([0.01,0.1,1,10])
A = 10
F = 10
Q = 10
R = 10
T = 10
n = 10
n1 = 10
α = 10
β = 10
σ = 10

# ln𝜀̇ = math.log(A) + n1*math.log(σ) - Q/R*T
# ln𝜀̇ = math.log(A) + β*σ - Q/R*T 

ln𝜀̇ = np.log(𝜀̇)
for file in dirs:
    print(file)
    df = pd.read_excel(path+"\\"+file)
    for i in range(df.shape[1]):
        # x = np.arange(0, 6, 0.1)
        # y = np.sin(x)
        # x1 = np.log(df.iloc[:,i])
        # print(type(y))
        # # z1 = np.polyfit(x1, y,1) # 用4次多项式拟合
        # # p1 = np.poly1d(z1)
        # # print(p1) # 在屏幕上打印拟合多项式
        # # yvals=p1(x1) # 也可以使用yvals=np.polyval(z1,x)
       
        # plt.plot(x,y,label="sin")
        # plt.xlabel("x") # x轴标签
        # plt.ylabel("y") # y轴标签
        # #plt.plot(x1,yvals)
        # #plt.legend()
        # plt.show
        x = ln𝜀̇ # 以0.1为单位，生成0到6的数据
        y1 = np.log(df.iloc[:,i])
        y2 = df.iloc[:,i]
        # 绘制图形
        plt.plot(x, y1, label="sin")
        plt.plot(x, y2, linestyle = "--", label="cos") # 用虚线绘制
        plt.xlabel("x") # x轴标签
        plt.ylabel("y") # y轴标签
        plt.title('sin & cos') # 标题
        plt.legend()
        plt.show()
        break
    break
