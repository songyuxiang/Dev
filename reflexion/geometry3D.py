import numpy as np
from numpy.linalg import svd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.pyplot as plt


# get distance of two 3D points
def yuxiangDistanceTwoPts(pt1, pt2):
    return np.sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2 + (pt1.z - pt2.z) ** 2)

def yuxiangLineCloudIntersection(line,pointcloud):
    pt1=line.startPoint
    pt2=pt1+line.direction
    for i in pointcloud.data:
        d1=yuxiangDistanceTwoPts(pt1,i)
        d2=yuxiangDistanceTwoPts(pt2,i)
        if d1-d2<0.05:
            return i,d1
    print("no intersection!")
    return None


def yuxiangFindMiddleTrack(pointcloud1,pointcloud2):
    pointcloud1.sort()
    for i in pointcloud1.data():
        max=0
        index=0
        newpointcloud=PointsCloud()
        for j in pointcloud2.data():
            d=yuxiangDistanceTwoPts(i,j)
            if d>max:
                max=d
                index=j
        newpointcloud.addPoint((pointcloud1[i]+pointcloud2[index])/2)
    return newpointcloud
def yuxiangLineFitting(point3dList):
    x=[]
    y=[]
    z=[]
    for i in point3dList:
        x.append(i.x)
        y.append(i.y)
        z.append(i.z)
    para1=np.polyfit(x,y,1)
    return para1
# get intersection of a plane and vector with a tolerance default 10e-6
def yuxiangIntersectPlaneVector(plane, line, tolerance=10e-6):
    normal = plane.normal.toArray()
    planePoint = plane.center.toArray()
    direction = line.direction.toArray()
    startPoint = line.startPoint.toArray()
    ndotu = normal.dot(direction)
    if abs(ndotu) < tolerance:
        print("no intersection or line is within plane")
    w = startPoint - planePoint
    si = -normal.dot(w) / ndotu
    Psi = w + si * direction + planePoint
    return Point3D(Psi[0], Psi[1], Psi[2])


# convert coordinates from cartesian to spheric
def yuxiangCartesian2Spheric(x, y, z):
    phi = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    omiga = np.arccos(z / phi)
    if y >= 0:
        delta = np.arccos((x / np.sqrt(x ** 2 + y ** 2)))
        return phi, omiga, delta
    else:
        delta = 2 * np.pi - np.arccos((x / np.sqrt(x ** 2 + y ** 2)))
        return phi, omiga, delta


# convert coordinates from spheric to cartesian
def yuxiangSpheric2Cartesian(ro, phi, theta):
    x = ro * np.sin(phi) * np.cos(theta)
    y = ro * np.sin(phi) * np.sin(theta)
    z = ro * np.cos(phi)
    return x, y, z


# find mirror of a vector
def yuxiangAxeMirror(vector, axe):
    dPhi = axe.phi - vector.phi
    dTheta = axe.theta - vector.theta
    x, y, z = vector.rotate(2 * dPhi, 2 * dTheta)
    return Vector3D(x, y, z)


class Geometry3D:
    def __init__(self):
        self.id = 0
        self.type = 0

    def setType(self, type):
        self.type = type


class Point3D(Geometry3D):
    def __init__(self, x, y, z=0,id=None):
        self.x = x
        self.y = y
        self.z = z
        self.id=id

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point3D(x, y, z)
    def __truediv__(self, other):
        try:
            other=float(other)
            x=self.x/other
            y=self.y/other
            z=self.z/other
            return Point3D(x,y,z)
        except TypeError:
            print("error : divisor has to be a number")
    def searchNeighborPoints(self, pointscloud, searchDistance=0.1):
        neighborPts = []
        distances = []
        for i in pointscloud:
            d = yuxiangDistanceTwoPts(self, i)
            if d < searchDistance:
                neighborPts.append(i)
                distances.append(d)
        return neighborPts, distances

    def toArray(self):
        return np.array([self.x, self.y, self.z])

    def __str__(self):
        return "3D POINT (x:%f, y:%f, z:%f)" % (self.x, self.y, self.z)


class Vector3D(Geometry3D):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.length, self.phi, self.theta = yuxiangCartesian2Spheric(x, y, z)

    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        z = self.z / other
        return Vector3D(x, y, z)

    def unify(self):
        return self / self.length

    def toArray(self):
        return np.array([self.x, self.y, self.z])

    def __str__(self):
        return "3D VECTOR (x:%f, y:%f, z:%f) ; (ro:%f, phi:%f, theta:%f)" % (
        self.x, self.y, self.z, self.length, self.phi, self.theta)

    def rotate(self, phi, theta):
        phi = self.phi + phi
        theta = self.theta + theta
        x, y, z = yuxiangSpheric2Cartesian(self.length, phi, theta)
        return x, y, z


class Line3D(Geometry3D):
    def __init__(self, point1, point2):
        self.startPoint = point1
        self.endPoint = point2
        self.direction = Vector3D(point2.x - point1.x, point2.y - point1.y, point2.z - point1.z).unify()

    def toVector(self):
        return Vector3D(self.endPoint.x - self.startPoint.x, self.endPoint.y - self.startPoint.y,
                        self.endPoint.z - self.startPoint.z)


class PointsCloud:
    def __init__(self, list=[]):

        self.data = []
        for i in list:
            self.data.append((i))
            # self.length = len(list)
        self.tangent=[]
        self.normal=[]
    def toList(self):
        list = []
        for i in self.data:
            pt = [i.x, i.y, i.z]
            list.append(pt)
        return list

    def toArray(self):
        return np.array(self.toList())
    def seperateXYZ(self):
        x=[]
        y=[]
        z=[]
        for i in self.data:
            x.append(i.x)
            y.append(i.y)
            z.append(i.z)
        return x,y,z
    def addPoint(self, point):
        self.data.append(point)
    def length(self):
        return len(self.data)
    def __getitem__(self, item):
        return self.data[item]
    def sort(self):
        Max=0
        maxIndex=0
        for i in range(self.length()):
            max=0
            for j in range(self.length()):
                d=yuxiangDistanceTwoPts(self.data[i],self.data[j])
                if d>max:
                    max=d
            if max>Max:
                Max=max
                maxIndex=i
        firstPt=maxIndex
        distance=[]
        for i in range(self.length()):

            d=yuxiangDistanceTwoPts(self.data[firstPt],self.data[i])
            distance.append(d)
        order=np.argsort(distance)
        newCloud=PointsCloud()
        for i in order:
            newCloud.addPoint(self.data[i])
        self.data=newCloud.data
    def updateTangents(self,radius=3):
        self.sort()

        for i in range(self.length()):
            temp = []
            if i < radius-1:
                temp=self.data[:i+radius]
            elif i>self.length()-radius:
                temp=self.data[(i-radius+1):]
            else:
                temp=self.data[i-radius+1:i+radius]

            para=yuxiangLineFitting(temp)
            self.tangent.append(para[1])
            self.normal.append(-1/(para[1]))
    def __str__(self):
        out=""
        for i in self.data:
            out+=str([i.x,i.y,i.z])+"\n"
        return out
    def resample(self,radius=5):
        pointcloud=PointsCloud()
        pointcloud.addPoint(self.data[0])
        newPt=self.data[0]
        i=0
        while i<self.length():
            for j in range(i+1,self.length()):
                d=yuxiangDistanceTwoPts(newPt,self.data[j])
                if d>radius-0.1 and d<radius+0.1:
                    newPt=self.data[j]
                    pointcloud.addPoint(newPt)
                    i=j
                    break
            break
        return pointcloud
class Plane3D(Geometry3D):
    def __init__(self):
        self.center = None
        self.normal = None

    def pointFitting(self, pointsCloud):
        pointsArray = pointsCloud.toArray()
        points = np.array(pointsArray).transpose()
        ctr = points.mean(axis=1)
        x = points - ctr[:, None]
        M = np.dot(x, x.T)  # Could also use cov(x) here.
        self.center = Point3D(ctr[0], ctr[1], ctr[2])
        temp = svd(M)[0][:, -1]
        self.normal = Vector3D(temp[0], temp[1], temp[2])
        return self.center, self.normal


