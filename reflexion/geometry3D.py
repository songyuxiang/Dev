import numpy as np
from numpy.linalg import svd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.pyplot as plt

def yuxiangDistanceTwoPts(pt1,pt2):
    return np.sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2+(pt1.z - pt2.z) ** 2)
def yuxiangIntersectPlaneVector(plane,line,tolerance=10e-6):
    normal=plane.normal.toArray()
    planePoint=plane.center.toArray()
    direction=line.direction.toArray()
    startPoint=line.startPoint.toArray()
    ndotu = normal.dot(direction)
    if abs(ndotu) < tolerance:
        print("no intersection or line is within plane")
    w = startPoint - planePoint
    si = -normal.dot(w) / ndotu
    Psi = w + si * direction + planePoint
    return Point3D(Psi[0],Psi[1],Psi[2])
def yuxiangCartesian2Spheric(x,y,z):
    phi=np.sqrt(x**2+y**2+z**2)
    omiga=np.arccos(z/phi)
    if y>=0:
        delta=np.arccos((x/np.sqrt(x**2+y**2)))
        return phi,omiga,delta
    else:
        delta = 2*np.pi-np.arccos((x / np.sqrt(x ** 2 + y ** 2)))
        return phi, omiga, delta
def yuxiangSpheric2Cartesian(ro,phi,theta):
    x=ro*np.sin(phi)*np.cos(theta)
    y = ro * np.sin(phi) * np.sin(theta)
    z = ro * np.cos(phi)
    return x,y,z
def yuxiangAxeMirror(vector,axe):
    dPhi=axe.phi-vector.phi
    dTheta=axe.theta-vector.theta
    x,y,z=vector.rotate(2*dPhi,2*dTheta)
    return Vector3D(x,y,z)

class Geometry3D:
    def __init__(self):
        self.id=0

class Point3D(Geometry3D):
    def __init__(self,x,y,z=0):
        self.x=x
        self.y=y
        self.z=z

    def __add__(self, other):
        x=self.x+other.x
        y=self.y+other.y
        z=self.z+other.z
        return Point3D(x,y,z)
    def searchNeighborPoints(self,pointscloud,searchDistance=0.1):
        neighborPts = []
        distances = []
        for i in pointscloud:
            d = yuxiangDistanceTwoPts(self, i)
            if d < searchDistance:
                neighborPts.append(i)
                distances.append(d)
        return neighborPts, distances
    def toArray(self):
        return np.array([self.x,self.y,self.z])
    def __str__(self):
        return "3D POINT (x:%f, y:%f, z:%f)"%(self.x,self.y,self.z)
class Vector3D(Geometry3D):
    def __init__(self,x,y,z=0):
        self.x=x
        self.y=y
        self.z=z
        self.length, self.phi, self.theta = yuxiangCartesian2Spheric(x, y, z)
    def __truediv__(self, other):
        x=self.x/other
        y=self.y/other
        z=self.z/other
        return Vector3D(x,y,z)
    def unify(self):
        return self/self.length
    def toArray(self):
        return np.array([self.x,self.y,self.z])
    def __str__(self):
        return "3D VECTOR (x:%f, y:%f, z:%f) ; (ro:%f, phi:%f, theta:%f)"%(self.x,self.y,self.z,self.length, self.phi, self.theta )
    def rotate(self,phi,theta):
        phi=self.phi+phi
        theta=self.theta+theta
        x,y,z=yuxiangSpheric2Cartesian(self.length,phi,theta)
        return x,y,z


class Line3D(Geometry3D):
    def __init__(self,point1,point2):
        self.startPoint=point1
        self.endPoint=point2
        self.direction=Point3D(point2.x-point1.x,point2.y-point1.y,point2.z-point1.z)
    def toVector(self):
        return Vector3D(self.endPoint.x-self.startPoint.x,self.endPoint.y-self.startPoint.y,self.endPoint.z-self.startPoint.z)
class PointsCloud:
    def __init__(self,list):

        self.data=[]
        for i in list:
            self.data.append((i))
        # self.length = len(list)

    def toList(self):
        list=[]
        for i in self.data:
            pt=[ i.x,i.y,i.z]
            list.append(pt)
        return list
    def toArray(self):
        return np.array(self.toList())
    def addPoint(self,point):
        self.data.append(point)
class Plane3D(Geometry3D):
    def __init__(self):
        self.center=None
        self.normal=None
    def pointFitting(self,pointsCloud):
        pointsArray=pointsCloud.toArray()
        points=np.array(pointsArray).transpose()
        ctr = points.mean(axis=1)
        x = points - ctr[:,None]
        M = np.dot(x, x.T) # Could also use cov(x) here.
        self.center=Point3D(ctr[0],ctr[1],ctr[2])
        temp=svd(M)[0][:,-1]
        self.normal=Vector3D(temp[0],temp[1],temp[2])
        return self.center, self.normal



p1=Point3D(1,2,3)
p2=Point3D(2,3,4)
p3=Point3D(3,4,4)
pointcloud=PointsCloud([p1,p2,p3])
line=Line3D(Point3D(2,2,2),Point3D(3,6,8))
plane=Plane3D()
plane.pointFitting(pointcloud)

vector=line.toVector()
print(vector)
print(plane.normal)
result=yuxiangAxeMirror(vector,plane.normal)
print(result)
result2=yuxiangAxeMirror(result,plane.normal)
print(result2)
fig=plt.figure()
ax=fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z)
# ax.legend()

plt.show()