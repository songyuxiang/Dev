from geometry3D import *
from PyQt5.Qt import *
import time

thickCenter=PointCloud()

thickCenter.loadFromFile("opendrive/thickcenter.csv")


gapPoints=yuxiangFindGapPoints(thickCenter)
print(gapPoints)
for i in gapPoints:
    temp=yuxiangInterpolateTwoPoints(i[0],i[1])
    thickCenter.appendCloud(temp)
thickCenter.saveToFile("opendrive/thickCenterInterp.csv")