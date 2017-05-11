from geometry3D import *
from fileManager import *


files=yuxiangGetFiles("/home/song/shares/cubature/" ,keyword=".txt")
print(yuxiangGetAllVolumes(files))

#
# file=open("cubature/data/B.txt",'r')
# data=file.readlines()[1:]
# pointcloud=PointsCloud()
# for i in data:
#     element=i.replace("\n","").split(" ")
#     pointcloud.addPoint(Point3D(element[0],element[1],element[2]))
# outline=yuxiangFindOutLine(pointcloud)
# outline.saveToFile("cubature/outline.csv")
# plane=yuxiangPlaneFitting(outline)
# test=PointsCloud()
# pt0=Point3D(1.40462341e+06,4.18889635e+06,4.47040741e+01)
# vector=Vector3D(0.00825784,0.00401612,0.99995784)
# pt1=pt0+vector
# pt2=pt1+vector
# pt3=pt2+vector
# test.data=[pt0,pt1,pt2,pt3]
# test.saveToFile("cubature/normal.txt")
# print(str(plane))


