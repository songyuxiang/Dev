from yuxiang.geometry import *



def opendrive(cloudFile,maintrackCloud,otherCloudList):
    print("test")


cloud1=PointCloud()
cloud2=PointCloud()
cloud1.loadFromFile("opendrive/cloud1.csv")
cloud2.loadFromFile("opendrive/cloud2.csv")
track=PointCloud()
track.loadFromFile("opendrive/track0.csv")
cloud1.sort(offset=2)
test=PointCloud()

test=yuxiangFindGapPoints2(cloud2)
for i in cloud2.data:
    temp=PointCloud()
    for j in cloud2.data:
        if yuxiangCheckNeighor2D(i,j):
            temp.addPoint(j)
    test.appendCloud(yuxiangCloudFittingInterpolation(temp,interpolateTime=20))
print(len(test.data))
test=yuxiangFindCloudCenterTrack(test)
print("ok1")
test.resample(0.2)
print("ok2")
test.saveToFile("opendrive/test.csv")

# cloud1=yuxiangFindCloudCenterTrack(cloud1)
# cloud2=yuxiangFindCloudCenterTrack(cloud2)
# cloud3=yuxiangFindCloudCenterTrack(cloud3)
# cloud1.resample(0.2)
# cloud2.resample(0.2)
# cloud3.resample(0.2)
# cloud1.saveToFile("opendrive/cloud1.csv")
# cloud2.saveToFile("opendrive/cloud2.csv")
# cloud3.saveToFile("opendrive/cloud3.csv")

