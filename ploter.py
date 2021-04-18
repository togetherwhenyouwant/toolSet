import time
import numpy as np
# 服务器上不进行显示
import pandas as pd
import seaborn as sns
import matplotlib as mpl
mpl.use('Agg')
from copy import deepcopy
import matplotlib.pyplot as plt
sns.set()

# 该绘制类是为了在服务器上实时看效果
class Ploter():

    def __init__(self):
        self.__scores = []
        self.__title = None
        self.__xlabel = None
        self.__ylabel = None
        self.__curTime = 0
        self.__gap = 1
        self.__coverFlag = False
        self.__path = None
        self.__curFigureNum = 0
    
    def setTitle(self,title):
        self.__title = title
    
    def setLabel(self,xlabel,ylabel):
        self.__xlabel = xlabel
        self.__ylabel = ylabel
    
    def setSaveGap(self,path,gap=1,coverFlag=True):
        # path:保存路径(包括名字)
        # gap:每隔几次进行保存
        # coverFlag:是否覆盖图像
        # saveDataFlag:是否保存数据（便于后续比较）
        self.__curTime = 0
        self.__gap = gap + 1
        self.__coverFlag = coverFlag
        self.__path = path

    def __saveFigure(self):

        if self.__path == None:return

        if self.__curTime  == 0:
            figureName = deepcopy(self.__path)
            self.__curFigureNum += 1
            # 如果不需要覆盖Figure的话
            if self.__coverFlag is False:
                figureName += str(self.__curFigureNum)
            
            saveDataName = deepcopy(figureName)
            figureName += '.jpg'
            # 进行保存
            self.__plot()
            plt.savefig(figureName)

        self.__curTime = (self.__curTime + 1) % self.__gap
            
    def __plot(self):

        #display.clear_output(wait=True)
        #display.display(plt.gcf())
        plt.clf()
        plt.title(self.__title)
        plt.xlabel(self.__xlabel)
        plt.ylabel(self.__ylabel)
        plt.plot(self.__scores)
        plt.text(len(self.__scores)-1, self.__scores[-1], str(self.__scores[-1]))
        # plt.pause(0.05)
        # plt.show()
    def addScore(self,score):
        self.__scores.append(deepcopy(score))
        self.__saveFigure()



# 该绘制类是为了查看强化学习最后学习效果
class RlPloter():
    def __init__(self):
        self.reset()

    def setTitle(self,title,fontSize = 20):
        self.__title = title
        self.__titleSize = fontSize
    
    def setLabel(self,xlabel,ylabel,fontSize = 15):
        self.__xLabel = xlabel
        self.__yLabel = ylabel
        self.__labelSize = fontSize
    
    def setXScale(self,xScale):
        self.__xScale = xScale
    
    def addLine(self,data,label,linestyle=None):
        self.__linesArr.append(data)
        #self.__colorArr.append(color)
        self.__labelArr.append(label)
        self.__lineStyleArr.append(linestyle)
    
    def reset(self):
        self.__linesArr = []
        self.__colorArr = []
        self.__labelArr = []
        self.__title = None
        self.__xLabel = None
        self.__yLabel = None
        self.__xScale = 1
        self.__titleSize = 20
        self.__labelSize = 15
        self.__lineStyleArr = []

    def saveFigure(self,fileName):
        df=[]
        fig = plt.figure()
        for i,line in enumerate(self.__linesArr):
            line = np.array(line)
            df.append(pd.DataFrame(line).melt(
                var_name=self.__xLabel,value_name=self.__yLabel))
            df[i][self.__xLabel] *= self.__xScale              # 对x轴度量尺度进行缩放
            df[i]['label']= self.__labelArr[i]          # 设置每条线的标签
            df[i]['lineStyle'] = self.__lineStyleArr[i] # 设置每条线的显示风格，可参照该文件末尾有介绍
        df=pd.concat(df)
        
        g = sns.lineplot(x=self.__xLabel, y=self.__yLabel,
            hue='label',style='label',data=df,markers=self.__lineStyleArr)
        g.legend_.set_title(None)
        plt.xlabel(self.__xLabel)
        plt.ylabel(self.__yLabel)
        plt.title(self.__title, fontsize=self.__titleSize)
        # plt.show()
        figureName = deepcopy(fileName)
        figureName += '.jpg'
        plt.savefig(figureName)



if __name__ == '__main__':
    # 第一个类使用方式
    __ploter = Ploter()
    __ploter.setTitle('AlphaZero WinRatio')
    __ploter.setLabel('game Time','WinRatio')
    # gap=1 意思是当add (gap+1) 数据后自动更新图片
    __ploter.setSaveGap('test',gap=0)    

    ## 使用就一个函数：
    for i in range(10):
        __ploter.addScore(i)
        time.sleep(1)

    # 第二个类使用方式
    a = RlPloter()
    a.setTitle('game')
    a.setLabel('time','score')
    basecond = [[18, 20, 19, 18, 13, 4, 1],                
                [20, 17, 12, 9, 3, 0, 0],               
                [20, 20, 20, 12, 5, 3, 0]]    

    cond1 = [[18, 19, 18, 19, 20, 15, 14],             
             [19, 20, 18, 16, 20, 15, 9],             
             [19, 20, 20, 20, 17, 10, 0],             
             [20, 20, 20, 20, 7, 9, 1]]   

    cond2 = [[20, 20, 20, 20, 19, 17, 4],            
             [20, 20, 20, 20, 20, 19, 7],            
             [19, 20, 20, 19, 19, 15, 2]]   

    cond3 = [[20, 20, 20, 20, 19, 17, 12],           
             [18, 20, 19, 18, 13, 4, 1],            
             [20, 19, 18, 17, 13, 2, 0],            
             [19, 18, 20, 20, 15, 6, 0]] 
    a.addLine(basecond,'test0')
    a.addLine(cond1,'test1')
    a.addLine(cond2,'test2')
    a.setXScale(10)         # 将x轴的度量放大十倍
    a.saveFigure('figure')

## 下面是lineStyle

# 'o'	                Circle
# '+'	                Plus sign
# '*'	                Asterisk
# '.'	                Point
# 'x'	                Cross
# '_'	                Horizontal line
# '|'	                Vertical line
# 'square' or 's'	    Square
# 'diamond' or 'd'	    Diamond
# '^'	                Upward-pointing triangle
# 'v'	                Downward-pointing triangle
# '>'	                Right-pointing triangle
# '<'	                Left-pointing triangle
# 'pentagram' or 'p'	Five-pointed star (pentagram)
# 'hexagram' or 'h'	    Six-pointed star (hexagram)
# 'none'	            No markers