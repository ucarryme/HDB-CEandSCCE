import pandas as pd
import os
import numpy as np

#读取路径
path = r"E:\learning\VSCode+python\python\hot deform beh\SCCE-build\polynomialFit"
#保存路径
pathResult = r"E:\learning\VSCode+python\python\hot deform beh\SCCE-build"


#步长
step = 0.05
#最大应变
maxStrain = 0.95
#次数
times = round(maxStrain/step,0)
#精度，建议使用高精度，观察哪些空缺，再增加数值补充空缺
precision = 0.00001

#思路：依次读取文件夹下的文件，文件中以strain-stress的形式两列两列的依次存储拟合数据
#程序从


dirs = os.listdir( path )
#文件夹下所以文件
for file in dirs:
   print(file)
#文件循环
for file in dirs:
   #读取文件
   df = pd.read_excel(path+"\\"+file)
   #存储最终数据
   result = pd.DataFrame()
   #列
   j = 0
   #arrData的列
   p = 0
   #列循环
   while j < df.shape[1]:
      #数组
      arrData = np.zeros((int(times),2))
      #赋值步长
      m = step
      #行arrData的行
      q = 0
      #行循环
      for k in range(df.shape[0]):
         #越界判断
         if p >= 2 or q >= (int(times)):
            break
         #找到最近的应变点
         if m <= maxStrain and abs(m-df.iloc[k,j]) <= precision:
            print("{}:".format(m)+"{}".format(df.iloc[k,j])+",{}".format(df.iloc[k,j+1]))
            #将应变点数据存储到arrData
            
            arrData[q][p+0] = df.iloc[k,j]
            arrData[q][p+1]  = df.iloc[k,j+1]
            #维系arrData的行
            q = q +1
            #维系应变量
            m = m+step
            m = round(m,2)
      #重置arrData的列
      p = 0
      #维系整体的列
      j = j+2
      print("j={}".format(j))
      #将一个温度的全部应变点数据放入数组
      #print(arrData)
      result = pd.concat([result,pd.DataFrame(np.array(arrData))],axis=1)
   result.to_excel(pathResult+r"\rate"+file)
   
#chr(ord('A')+j)


