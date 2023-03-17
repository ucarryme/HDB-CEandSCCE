推荐阅读文献后，自己将峰值应力的本构方程建立再进行本程序操作。

本程序可以建立所有应变点本构方程，应力补偿。

 

 

操作过程在operation manual.docx中

若需应力补偿，跟随下步骤，若只需构建峰值应力的本构方程。直接到step（5）

运行程序前，均需按照步骤下的指引，修改成自己的参数

**删除所有文件夹中的.gitkeep文件**

1、首先得到拟合平滑数据，放入文件夹fitData中，以便找到真应变的数据点的真应力

​    拟合数据要求：以应变速率为单位放入excel，每个excel文件存储为一个应变速率下的所有温度的strain-stress.

​    本文中有4种变形速率，故文件夹下有4个excel文件。每个文件内有6种温度，每种温度列单元为strain-stress，故共有2*6列。

 ![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg)

 

2、运行CE-getStrainPoint**.py系列(运行单个即可)读取/fitData/70%下所有文件，得到设置step = 0.05，maxStrain = 0.95，故每个文件数据点为 0.95/0.05 个。真应变的全部数据点的真应力数据放入/Stress/70%中

故该子程序只需修改读取文件路径，保存路径，步长，总应变（终点应变值），精度（值越小，精度越高）

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

得到的文件：

红框中为得到的文件

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image010.jpg)

若用简洁版程序(CE-getStressPointONLYStress.py)运行，行为0.05差值，故本文为0.05-0.95，共0.95/0.05行，列为每个温度下的应力值，故有6列。顺序未发生变化。

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

3、自行修正数据放入/Stress/70%/fix-rate中

 

修正：因为设置的精度不同，过高的精度会导致数据缺失。

注意：第一行为空，第一列为数据的开始。如图

​    ![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

4、运行split.py,调整/Stress/70%/fix-rate中的文件，按真应变量存储文件放入/Stress/70%/fix-strain中。峰值应力的数据可以自寻寻找，直接放入/Stress/70%/fix-strain该文件夹下。

调整：因为返回的数据仍为应变速率为单位的文件，例：0.01.xlsx存储的是每一行以应变量0.05相差，列是900~1200℃。后续所需文件为不同应变值为单个文件，行为应变速率，列为温度。

故在运行split.py之前，有文件为4（速率，文件个数）* 19(0.95/0.05，行) * 6(温度，列)，如step(2)结果截图所示

现需要文件格式为19(文件个数) * 4（速率，行）* 6(温度，列)，如下图所示。

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

split.py子程序只需要改读取文件路径，保存文件路径，索引和步长

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image020.jpg)

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image022.jpg)

5、如若只需构建峰值应力的本构模型，直接把按下图格式放入/Stress/70%/fix-strain中即可。列为温度，行为速率。第一行是温度顺序，只需自己记住，可写可不写。数据从只会第二行开始读取的。

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image024.jpg)

 

运行CE-buildCE.py建立本构方程。程序读取/Stress/70%/fix-strain所有文件。每一个文件都会得到lnσ-ln𝜀̇的关系(每有一温度便有一种关系)，其中包含数据计算，拟合，画图(已关闭，可自行打开，或者根据保存的数据，去origin自行画图)，得到每斜率、截距。同理后续所有本构方程建立的所有关系一并得到。将数据保存至/CE-build中(存储的斜率和截距已算平均值)。得到最终数据（/CE-build/70%/all values.xlsx）

运行程序只需修改：

path（读取文件的文件夹），pathResult（结果保存在的文件夹），

应变速率(改成自己的应变速率)，rates和temperatures（本文有4种速率，6种温度），temper（改成自己的温度），step步长

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image026.jpg) 

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image028.jpg)

该步骤将在/CE-build生成/Stress/70%/fix-strain下文件个数的文件夹每个文件夹下有8个文件（注意每个文件的名称的含义），是每一个真应变点建立本构方程的所有数据。

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image030.jpg)![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image032.jpg)

**注意：all values.xlsx中行的索引（行头）是根据设置的步长所建立的，如果你也是每个0.05应变量取点，则无需修改。如果不是修改成你的便可。如果你在/Stress/70%/fix-strain中加入了峰值应力数据，峰值应力的行索引是该文件中最后的一行，该行索引无意义，只是自然递增。

 

| **应变** | **n1** | **β** | **α** | **n** | **Q** | **lnA** |
| -------- | ------ | ----- | ----- | ----- | ----- | ------- |
|          |        |       |       |       |       |         |

 

6、处理all values.xlsx，用origin多项式拟合 应变与**α****n****Q****lnA**（/SCCE-build/多项式拟合.opju），得到高次方方多项式（本文用polynomial/poly拟合，9次方），记录系数值（文章要用，非程序），将拟合数据保存到/SCCE-build/origin拟合/polynomialFit中，

​    该数据文件列单元为 应变与**α****n****Q****lnA**的组合，故有2*4列。数据同样从第二行开始读取

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image034.jpg)

origin小技巧：xyyyy拟合，放入4个图层。首先画出散点图在一个图层中，再点击右侧导航框，生成2*2的4个图层，再更改每个图的x和y轴便可

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image036.jpg)

7、运行/backupCode/CE-getStrainPoint**.py系列，读取(/SCCE-build/polynomialFit)中文件，找出step（6）中拟合过程的应变点的应力值，数据放入(/SCCE-build)

得到关于19行，4列的数据。行为应变点0.05，0.1，0.15~0.95。列为**α****n****Q****lnA**

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image038.jpg)

8、调整step(7)中的结果文件，放/SCCE-build/verify/70%/commonData.xlsx中。

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image040.jpg)

9、运行CE-buildSECE.py文件，读取commonData.xlsx，进行应力补偿计算，将结果文件放入/SCCE-build/verify/70%/result中。

图中excel文件为程序计算出的文件。

![img](file:///C:/Users/tron/AppData/Local/Temp/msohtmlclip1/01/clip_image042.jpg)

origin小技巧：画出应力补偿后点线共存图。

参考：[急求！origin中如何做出实线和散点并存的图_originlab吧_百度贴吧 (baidu.com)](https://tieba.baidu.com/p/6105598843)

 

 

 

 
