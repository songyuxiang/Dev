from geometry3D import *

file=open("cubature/data/B.txt",'r')
data=file.readlines()[1:]
pointcloud=PointsCloud()
for i in data:
    element=i.replace("\n","").split(" ")
    pointcloud.addPoint(Point3D(element[0],element[1],element[2]))
pointcloud.saveToFile("reflexion/cloud.csv")

pt1=Point3D(1404626.375,4188824,50.419998)
pt2=Point3D(1404626.375,4188894,47.419998)
line=Line3D(Point3D(1404626.375,4188824,50.419998),Point3D(1404626.375,4188894,47.419998))
directionCloud=PointsCloud()
directionCloud.addPoint(pt1)
directionCloud.addPoint(pt2)
directionCloud.saveToFile("reflexion/direction.csv")

intersection=yuxiangRayCloudIntersection(line,pointcloud)
intersection.saveToFile("reflexion/intersection.csv")

