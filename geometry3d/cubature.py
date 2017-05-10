from geometry3D import *
file=open("cubature/B.txt",'r')
data=file.readlines()
pointcloud=PointsCloud()
for i in data:
    elements=i.replace('\n','').split(' ')
    pointcloud.addPoint(Point3D(elements[0],elements[1],elements[2]))

def yuxiangPlaneFitting(pointcloud):
    points=[]
    for i in pointcloud.data:
        points.append([i.x,i.y,i.z])
    points = np.array(points).transpose()
    ctr = points.mean(axis=1)
    x = points - ctr[:, None]
    M = np.dot(x, x.T)  # Could also use cov(x) here.
    center, normal=ctr, svd(M)[0][:, -1]
    return Plane3D(center,normal)






# outline=PointsCloud()
# outline.loadFromFile("cubature/outline.csv")


print(yuxiangGetVolume(pointcloud))