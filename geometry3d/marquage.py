from geometry3D import *
#

# file=open("opendrive/test.txt")
# data=file.readlines()[:10]
# print(data)

# noise=yuxiangLoadPointCloud("opendrive/german_highway.txt","0",5)

# # thickLine.resample(0.1)
# # thinLine.resample(0.1)
# # continuousLine.resample(0.1)
# # thickLine.sort()
# # thinLine.sort()
# # continuousLine.sort()
# # noise=PointsCloud()

# #
# noise.loadFromFile("opendrive/noise.csv")


# print(thickLine.length(),thinLine.length(),continuousLine.length())


# thickLine=yuxiangLoadPointCloud("opendrive/german_highway.txt","1",5)
# thinLine=yuxiangLoadPointCloud("opendrive/german_highway.txt","2",5)
# continuousLine=yuxiangLoadPointCloud("opendrive/german_highway.txt","3",5)
# thickLine.saveToFile("opendrive/thick.csv")
# thinLine.saveToFile("opendrive/thin.csv")
# continuousLine.saveToFile("opendrive/continuous.csv")

import time
# thickLine=PointsCloud()
# thinLine=PointsCloud()
# continuousLine=PointsCloud()
# thickLine.loadFromFile("opendrive/thick.csv")
# thinLine.loadFromFile("opendrive/thin.csv")
# continuousLine.loadFromFile("opendrive/continuous.csv")
# continuousLine_Sub=PointsCloud(continuousLine.data)
# continuousLine_Sub.resample(0.5)
# continuousLine_Sub.saveToFile("opendrive/continuous_sub.csv")
# print(continuousLine.length(),continuousLine_Sub.length())

# time1=time.time()
# continuousLine_Sub=PointsCloud()
# continuousLine_Sub.loadFromFile("opendrive/continuous_sub.csv")
# groups=yuxiangDevideCloudByDistance(continuousLine,1)
# time2=time.time()
# print(time2-time1)
# for i in range(len(groups)):
#     groups[i].saveToFile("opendrive/continous_sub%d.csv"%i)
#
# time3=time.time()
# print(time3-time2)

cloud1=PointsCloud()
cloud1.loadFromFile("opendrive/continous_sub0.csv")
cloud1.resample(1)
cloud1.sort(offset=100)
cloud1.updateTangents()
cloud1.saveToFile("opendrive/resample1.csv",True)