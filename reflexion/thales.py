from geometry3D import *

p1=Point3D(1,2,3)
p2=Point3D(2,3,3)
p3=Point3D(3,4,3)
p4=Point3D(4,5,3)
p5=Point3D(5,1,3)
pointcloud=PointsCloud([p1,p2,p3,p4,p5])
pointcloud.sort()
pointcloud.updateTangents()
print(pointcloud)