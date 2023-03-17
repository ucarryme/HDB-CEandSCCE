import numpy as np
import pandas as pd
import os

#读取的文件夹
path = r'Stress\70%\fix-rate'
#保存文件的文件夹
pathResult = r'Stress\70%\fix-strain'

files = os.listdir(path)

#文件个数，，行，列，均无需修改
filenum = -1
rows = -1
cols = -1
arrData = pd.DataFrame()

#索引
index = [0.01,0.1,1,10]
columns = [900,950,1000,1050,1100,1200]
#步长，结果文件命名所用
step = 0.05


i = 0
#将所有文件中的值按文件为单元，列合并-------------------------------------------
for file in files :
    df = pd.read_excel(path+r'\\'+file)
    filenum = len(files)
    rows = df.shape[0]
    cols = df.shape[1]
    arrData = pd.concat([arrData,df],axis=1)
    i +=1
#将合并的放入数组中，每完成一个数组，就生成一个文件---------------------------
#合并数据的行循环
for j in range(rows):
    #缓存数组
    tempData = np.zeros((filenum,cols))
    #缓存数组的行
    m = -1
    #合并数据的列循环
    for k in range(filenum*cols):
        #每当有6列了，缓存数组的行加一
        if k%cols is 0:
            m +=1
        tempData[m,k%cols] = arrData.iloc[j,k]
    Result = pd.DataFrame(tempData)
    Result.index = index
    Result.columns = columns

    Result.to_excel(pathResult+r'\\{}.xlsx'.format(round(step*(j+1),2)),index=False)
    



