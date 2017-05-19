from geometry3D import *
from PyQt5.Qt import *

cloud=PointCloud()
cloud.loadFromFile("opendrive/continous_sub0.csv")
# center=yuxiangFindCloudCenterTrack(cloud)
# center.resample(0.1)
# center.sort(offset=10)
# center.updateTangents()
# center.saveToFile()
center=PointCloud()
center.loadFromFile("opendrive/test.csv")
center.sort(10)
center.updateTangents()
test1=PointCloud()
test2=PointCloud()
for i in range(len(center.data)):
    vector=Vector3D(1,center.normal[i],0)
    vector.unify()
    # line=Line3D(startPt=center.data[i],vector=vector)
    # print(yuxiangLineCloudIntersection(line,cloud))
    try:
        test1.addPoint(yuxiangFarestLineCloudIntersection(center.data[i],vector,cloud)[0])
        test2.addPoint(yuxiangFarestLineCloudIntersection(center.data[i], vector, cloud)[2])
    except:
        print("none")

test1.saveToFile("opendrive/test1.csv")
test2.saveToFile("opendrive/test2.csv")
#
#
# center=PointCloud()
# center.loadFromFile("opendrive/test.csv")
# center.updateTangents()
# print(center)
# center.saveToFile("opendrive/test.csv",True)