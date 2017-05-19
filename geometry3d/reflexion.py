from geometry3D import *

file=open("cubature/data/B.txt",'r')
data=file.readlines()[1:]
pointcloud=PointsCloud()
for i in data:
    element=i.replace("\n","").split(" ")
    pointcloud.addPoint(Point3D(element[0],element[1],element[2]))
pointcloud.saveToFile("reflexion/cloud.csv")

pt1=Point3D(1404636.04,4188873.94,57.33)
pt2=Point3D(1404622.04,4188896.94,42.33)
line=Line3D(pt1,pt2)
directionCloud=PointsCloud()
directionCloud.addPoint(pt1)
directionCloud.addPoint(pt2)
directionCloud.saveToFile("reflexion/direction.csv")

intersection=yuxiangRayCloudIntersection(line,pointcloud)
intersection.saveToFile("reflexion/intersection.csv")

