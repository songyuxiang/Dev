from geometry3D import *
from PyQt5.Qt import *

roadMarker=PointCloud()
roadMarker.loadFromFile("opendrive/continuous1.csv")
centerTrack=PointCloud()
centerTrack.loadFromFile("opendrive/center.csv")
for i in range(len(centerTrack.data)-2):
    print(yuxiangCurvature3Points(centerTrack.data[i],centerTrack.data[i+1],centerTrack.data[i+2]))
# centerTrack.resample(0.01)
# centerTrack.sort()
# centerTrack.updateTangents()
# centerTrack.saveToFile("opendrive/center.csv")
# result1=PointCloud()
# result2=PointCloud()
# normal=PointCloud()
# for i in range(len(centerTrack.data)):
#     line=Line3D(startPt=centerTrack.data[i],vector=Vector3D(1,centerTrack.normal[i],0).unify())
#     out=yuxiangFarestLineCloudIntersection(line,roadMarker)
#     normal.appendCloud(line.toPointCloud())
#     if out[0]!=None and out[2]!=None:
#         result1.addPoint(out[0])
#         result2.addPoint(out[2])
# normal.saveToFile("opendrive/normal.csv")
# result1.saveToFile("opendrive/result1.csv")
# result2.saveToFile("opendrive/result2.csv")
# cloud=PointCloud()
# cloud.loadFromFile("opendrive/continous_sub0.csv")
# # center=yuxiangFindCloudCenterTrack(cloud)
# # center.resample(0.1)
# # center.sort(offset=10)
# # center.updateTangents()
# # center.saveToFile()
# center=PointCloud()
# center.loadFromFile("opendrive/test.csv")
# center.sort(10)
# center.updateTangents()
# test1=PointCloud()
# test2=PointCloud()
# for i in range(len(center.data)):
#     vector=Vector3D(1,center.normal[i],0)
#     vector.unify()
#     # line=Line3D(startPt=center.data[i],vector=vector)
#     # print(yuxiangLineCloudIntersection(line,cloud))
#     try:
#         test1.addPoint(yuxiangFarestLineCloudIntersection(center.data[i],vector,cloud)[0])
#         test2.addPoint(yuxiangFarestLineCloudIntersection(center.data[i], vector, cloud)[2])
#     except:
#         print("none")
#
# test1.saveToFile("opendrive/test1.csv")
# test2.saveToFile("opendrive/test2.csv")
#
#
# center=PointCloud()
# center.loadFromFile("opendrive/test.csv")
# center.updateTangents()
# print(center)
# center.saveToFile("opendrive/test.csv",True)