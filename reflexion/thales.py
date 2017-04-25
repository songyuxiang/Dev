from geometry3D import *



# resample101=PointsCloud()
# resample101.loadFromFile("resample101.csv")
#
# pointcloud102=PointsCloud()
# pointcloud102.loadFromFile("cloud102.csv")
# # # pointcloud2=loadcloud("2")
# # # pointcloud2.saveToFile("cloud2")
# # # print(pointcloud2)
# middletTrack=yuxiangFindMiddleTrack(resample101,pointcloud102)
# middletTrack.saveToFile("cloud_middle_101_102")
middleTrack=PointsCloud()
middleTrack.loadFromFile("cloud_middle_101_102.csv")
cloud3=PointsCloud()
cloud3.loadFromFile("cloud3.csv")
out=[]
for i in range(middleTrack.length()):
    vector=Vector3D(1,middleTrack.normal[i],0)
    vector=vector.unify()
    line=Line3D(middleTrack[i],vector=vector)
    out.append(yuxiangNearestLineCloudIntersection(line,cloud3,tolerance=0.01,is3D=False))
print(out)
distancePoint1=PointsCloud()
for i in out:
    if i[0]!=None:
        distancePoint1.addPoint(i[0])
distancePoint1.saveToFile("nearestPt1")
distancePoint2=PointsCloud()
for i in out:
    if i[2] != None:
        distancePoint2.addPoint(i[2])
distancePoint2.saveToFile("nearestPt2")