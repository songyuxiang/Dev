import numpy as np
from numpy.linalg import svd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def yuxiangLoadPointCloud(type,filename="data.csv",header=True,sort=False):
    text=TextEditor(filename,header=header)
    pointcloud=PointsCloud()
    for i in text.data:
        if i[3]=='nan':
            point=Point3D(i[0],i[1],i[2],type=i[4])
        else:
            point = Point3D(i[0], i[1], i[2], type=i[3])
        if point.type==type:
            pointcloud.addPoint(point)
    if sort==True:
        pointcloud.updateTangents()
    pointcloud.saveToFile("cloud"+str(type))
    return pointcloud

# get distance of two 3D points
def yuxiangDistanceTwoPts(pt1, pt2,is3D=True):
    if is3D:
        return np.sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2 + (pt1.z - pt2.z) ** 2)
    else:
        return np.sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2)
def yuxiangLineCloudIntersection(line,pointcloud,tolerance=0.05,is3D=True):
    pt1=line.startPoint
    pt2=pt1+line.direction
    out1=[]
    out2=[]
    for i in pointcloud.data:
        d1=yuxiangDistanceTwoPts(pt1,i,is3D)
        d2=yuxiangDistanceTwoPts(pt2,i,is3D)
        if d1>d2:
            if np.abs(d1-d2-1)<tolerance:
                out1.append([i,d1])
        else:
            if np.abs(d2-d1-1)<tolerance:
                out2.append([i, d1])
    return out1,out2


def yuxiangNearestLineCloudIntersection(line, pointcloud, tolerance=0.05,is3D=True):
    pt1 = line.startPoint
    pt2 = pt1 + line.direction
    point1=PointsCloud()
    point2=PointsCloud()
    lMin1=10000
    lMin2=10000
    for i in pointcloud.data:
        d1 = yuxiangDistanceTwoPts(pt1, i,is3D)
        d2 = yuxiangDistanceTwoPts(pt2, i,is3D)

        if d1 > d2:
            if np.abs(d1 - d2 - 1) < tolerance:
                if d1<lMin1:
                    point1=i
                    lMin1=d1
        else:
            if np.abs(d2 - d1 - 1) < tolerance:
                if d1<lMin2:
                    point2=i
                    lMin2=d1
    if lMin1==10000:
        point1=None
        lMin1=None
    if lMin2==10000:
        point2=None
        lMin2=None
    return point1,lMin1,point2,lMin2

def yuxiangFindMiddleTrack(pointcloud1,pointcloud2):
    newpointcloud = PointsCloud()
    for i in range(pointcloud1.length()):
        min=10000
        index=0
        for j in range(pointcloud2.length()):
            d=yuxiangDistanceTwoPts(pointcloud1[i],pointcloud2[j])
            if d<min:
                min=d
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
    x=float(x)
    y=float(y)
    z=float(z)
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


class TextEditor:
    def __init__(self,filename,openmode='r',spliter=',',header=False):
        file=open(filename,openmode)
        self.data=[]
        if header==False:
            self.lines=file.readlines()

        else:
            lines=file.readlines()
            self.lines=lines[1:]
            self.header=lines[0]
        for i in self.lines:
            i=i.replace("\n","")
            element=i.split(spliter)
            self.data.append(element)

class Geometry3D:
    def __init__(self):
        self.id = 0
        self.type = 0

    def setType(self, type):
        self.type = type


class Point3D(Geometry3D):
    def __init__(self, x, y, z=0,id=None,type=None):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.id=id
        self.type=type
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
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
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
    def __init__(self, startPt=None, endPt=None,vector=None):
        if startPt!=None and endPt!=None:
            self.startPoint = startPt
            self.endPoint = endPt
            self.direction = Vector3D(endPt.x - startPt.x, endPt.y - startPt.y, endPt.z - startPt.z).unify()
        elif startPt!=None and vector!=None:
            self.startPoint = startPt
            self.endPoint = startPt+vector
            self.direction = vector.unify()
        else:
            print("error : wrong input for Line3D!")
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
    def clonefrom(self,cloud):
        self.data=cloud.data
        self.tangent=cloud.tangent
        self.normal=cloud.normal
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
    def updateTangents(self,searchNeighbor=2):
        self.sort()
        self.tangent=[]
        self.normal=[]
        for i in range(self.length()):
            temp = []
            if i < searchNeighbor-1:
                temp=self.data[:i+searchNeighbor]
            elif i>self.length()-searchNeighbor:
                temp=self.data[(i-searchNeighbor+1):]
            else:
                temp=self.data[i-searchNeighbor+1:i+searchNeighbor]

            para=yuxiangLineFitting(temp)
            self.tangent.append(para[1])
            self.normal.append(-1/(para[1]))
    def __str__(self):
        out=""
        for i in self.data:
            if i.type==None:
                out+=str([i.x,i.y,i.z])+"\n"
            else:
                out += str([i.x, i.y, i.z,i.type]) + "\n"
        return out
    def resample(self,radius=5):
        data=self.data
        size=len(data)
        deletenumber=0
        for i in range(size-1):
            j=1
            while j<size-i-1-deletenumber:
                if yuxiangDistanceTwoPts(data[i],data[j])<radius:
                    data.pop(j)
                    deletenumber+=1
                print(j, len(data), size - i - 1 - deletenumber)
                j+=1
        return data

    def saveToFile(self,filename):
        file =open(filename+".csv",'w')
        for i in range(self.length()):
            file.write(str(self.data[i].x)+',')
            file.write(str(self.data[i].y)+',')
            file.write(str(self.data[i].z)+',')
            if self.data[i].type!=None:
                file.write(str(self.data[i].type) + ',')
            else:
                file.write("None" + ',')
            try:
                file.write(str(self.tangent[i])+',')
            except IndexError:
                file.write("None"+',')
            try:
                file.write(str(self.normal[i])+'\n')
            except IndexError:
                file.write("None"+'\n')
        print("saved")
    def loadFromFile(self,filename):
        file = open(filename, 'r')
        lines=file.readlines()
        self.data=[]
        self.tangent=[]
        self.normal=[]

        for i in lines:
            i=i.replace('\n','')
            data=i.split(',')
            point=Point3D(data[0],data[1],data[2],type=data[3])
            self.data.append(point)
            if i[4]!="None":
                self.tangent.append(i[4])
            if i[5]!="None":
                self.normal.append(i[5])
        print("loaded")
    def show(self):
        x=[]
        y=[]
        z=[]
        for i in range(self.length()):
            x.append(self.data[i].x)
            y.append(self.data[i].y)
            z.append(self.data[i].z)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(np.array(x),np.array(y),np.array(z))
        plt.show()

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


