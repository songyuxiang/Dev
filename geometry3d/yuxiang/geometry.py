import numpy as np
from numpy.linalg import svd
from enum import Enum
from yuxiang.convert import *
class Yuxiang(Enum):
    FittingMode_Line=0

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
    def toArray(self):
        return np.array([self.x, self.y, self.z])
    def setType(self,type):
        self.type=type
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point3D(x, y, z)
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector3D(x,y,z)
    def __truediv__(self, other):
        try:
            other=float(other)
            x=self.x/other
            y=self.y/other
            z=self.z/other
            return Point3D(x,y,z)
        except TypeError:
            print("error : divisor has to be a number")
    def __str__(self):
        if self==None:
            return "None"
        else:
            return "3D POINT (x:%f, y:%f, z:%f)" % (self.x, self.y, self.z)


class Vector3D(Geometry3D):
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.length, self.phi, self.theta = yuxiangConvert.yuxiangCartesian2Spheric(x, y, z)
    def unify(self):
        return self / self.length
    def rotate(self, phi, theta):
        phi = self.phi + phi
        theta = self.theta + theta
        x, y, z = yuxiangConvert.yuxiangSpheric2Cartesian(self.length, phi, theta)
        return x, y, z
    def toArray(self):
        return np.array([self.x, self.y, self.z])
    def getNorm(self):
        return np.sqrt(self.x**2+self.y**2+self.z**2)
    def __truediv__(self, other):
        x = self.x / other
        y = self.y / other
        z = self.z / other
        return Vector3D(x, y, z)
    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        z = self.z * other
        return Vector3D(x, y, z)
    def __str__(self):
        return "3D VECTOR (x:%f, y:%f, z:%f) ; (ro:%f, phi:%f, theta:%f)" % (
        self.x, self.y, self.z, self.length, self.phi, self.theta)


class Plane3D(Geometry3D):
    def __init__(self,center=None,normal=None):
        self.center = center
        self.normal = normal

    def pointFitting(self, pointCloud):
        pointsArray = pointCloud.toArray()
        points = np.array(pointsArray).transpose()
        ctr = points.mean(axis=1)
        x = points - ctr[:, None]
        M = np.dot(x, x.T)  # Could also use cov(x) here.
        self.center = Point3D(ctr[0], ctr[1], ctr[2])
        temp = svd(M)[0][:, -1]
        self.normal = Vector3D(temp[0], temp[1], temp[2])
        return self.center, self.normal
    def __str__(self):
        out="center : "+str(self.center)+" ; normal : " + str(self.normal)
        return out

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
    def toPointCloud(self,nb=20):
        pointcloud=PointCloud()
        gap=1/20
        for i in range(nb):
            pointcloud.addPoint(self.startPoint+self.direction*gap*i)
        return pointcloud
class PointCloud(Geometry3D):
    def __init__(self, list=[],filename=None):
        self.data = []
        for i in list:
            self.data.append((i))
            # self.length = len(list)
        self.tangent=[]
        self.normal=[]
        self.slope=[]
        self.cap=[]
        self.sortType=None
    def addPoint(self, point):
        self.data.append(point)
    def appendCloud(self,cloud):
        for i in cloud.data:
            self.data.append(i)
    def length(self):
        return len(self.data)
    def __getitem__(self, item):
        return self.data[item]
    def resample(self,radius=3):
        data = self.data
        size=len(data)
        i=0
        while i < size:
            j=i+1
            while j < size:
                if yuxiangDistanceTwoPts(data[i], data[j]) < radius:
                    data.pop(j)
                    size -= 1
                else:
                    j += 1
            i +=1
        self.data=data
        return data
    def sort(self,clockwise=True,offset=0):
        Xc = 0
        Yc = 0
        Zc = 0
        size = len(self.data)
        for i in self.data:
            Xc += i.x
            Yc += i.y
            Zc += i.z
        center=Point3D(Xc / size-offset, Yc / size-offset, Zc / size-offset)
        cap = []
        for i in self.data:
            cap.append(yuxiangGetCap(center, i))
        cap=yuxiangCorrectCap(cap)
        order = np.argsort(cap)
        newData = []
        for i in order:
            newData.append(self.data[i])
        if not clockwise:
            tempData=[]

            for i in range(size):
                tempData.append(newData[size-i-1])
            newData=tempData
            self.sortType="counter-clockwise"
        else:
            self.sortType="clockwise"
        self.data=newData
    def updateTangents(self,searchNeighbor=2):
        if self.sortType==None:
            print("you have to sort first the cloud!")
        else:
            print("sort order is  :  "+self.sortType)
            self.tangent=[]
            self.normal=[]
            self.slope=[]
            self.cap=[]
            for i in range(self.length()):
                temp = []
                if i < searchNeighbor-1:
                    temp=self.data[:i+searchNeighbor]
                elif i>self.length()-searchNeighbor:
                    temp=self.data[(i-searchNeighbor+1):]
                else:
                    temp=self.data[i-searchNeighbor+1:i+searchNeighbor]
                tan=yuxiangGetTangent(temp)
                self.tangent.append(tan)
                self.normal.append(-1/(tan))
                para2=yuxiangLineFitting(temp,mode="z")
                self.slope.append(para2[1])
                pt1=temp[0]
                pt2=temp[-1]
                cap=yuxiangGetCap(pt1,pt2)
                self.cap.append(cap)

    def setType(self,type):
        for i in self.data:
            i.setType(type)
    def __str__(self):
        out=""
        for i in self.data:
            if i.type==None:
                out+=str([i.x,i.y,i.z])+"\n"
            else:
                out += str([i.x, i.y, i.z,i.type]) + "\n"
        return out


    def saveToFile(self,filename,hasId=False):
        file =open(filename,'w')
        for i in range(self.length()):
            if hasId:
                file.write(str(i)+',')
            try:
                file.write("%.8f"%self.data[i].x+',')
                file.write("%.8f"%self.data[i].y+',')
                file.write("%.8f"%self.data[i].z+',')
                if self.data[i].type!=None:
                    file.write(str(self.data[i].type) + ',')
                else:
                    file.write("None" + ',')
                try:
                    file.write("%.8f"%self.cap[i]+',')
                except:
                    file.write("None"+',')
                try:
                    file.write("%.8f"%self.normal[i]+',')
                except:
                    file.write("None"+',')
                try:
                    file.write("%.8f"%self.slope[i]+'\n')
                except:
                    file.write("None"+'\n')
            except:
                print("a point leaps")
        print("saved")
    def loadFromFile(self,filename,spliter=","):
        file = open(filename, 'r')
        lines=file.readlines()
        self.data=[]
        self.tangent=[]
        self.normal=[]
        self.slope=[]
        for i in lines:
            i=i.replace('\n','')
            data=i.split(spliter)
            point=Point3D(data[0],data[1],data[2],type=data[3])
            self.data.append(point)
            try:
                if data[4]!="None":
                    self.cap.append(data[4])
                else:
                    self.cap.append(None)
            except IndexError:
                self.cap.append(None)
            try:
                if data[5]!="None":
                    self.normal.append(data[5])
                else:
                    self.normal.append(None)
            except IndexError:
                self.normal.append(None)
            try:
                if data[6]!="None":
                    self.slope.append(data[6])
                else:
                    self.slope.append(None)
            except IndexError:
                self.slope.append(None)
        print("loaded")
    def toList(self):
        list = []
        for i in self.data:
            pt = [i.x, i.y, i.z]
            list.append(pt)
        return list
    def toArray(self):
        return np.array(self.toList())

class Cercle:
    def __init__(self,center=None,radius=None,threePts=None):
        if center!=None:
            self.center=center
        if radius!=None:
            self.radius=radius
        if threePts!=None and len(threePts)==3:
            A=threePts[0]
            B=threePts[1]
            C=threePts[2]
            a = (C - B).getNorm()
            b = (C - A).getNorm()
            c = (B - A).getNorm()
            s = (a + b + c) / 2
            R = a * b * c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
            b1 = a * a * (b * b + c * c - a * a)
            b2 = b * b * (a * a + c * c - b * b)
            b3 = c * c * (a * a + b * b - c * c)
            P = np.array([[A.x, B.x, C.x], [A.y, B.y, C.y], [A.z, B.z, C.z]]).dot(np.hstack((b1, b2, b3)))
            P /= b1 + b2 + b3
            self.center = Point3D(P[0], P[1], P[2])
            self.radius=R
    def __str__(self):
        return "Center : "+str(self.center)+" ; Radius : "+str(self.radius)+"\n"








####
###------------GeoMeter3D---------------###
####


# in : each file in fileList represent a pointcloud
# return : list [[name,surface,volume],..,..]
def yuxiangGetAllVolumes(fileList):
    result=[]
    file=open("result.txt",'w')
    for i in fileList:
        file=open(i,'r')
        data=file.readlines()[1:]
        pointcloud=PointCloud()
        for j in data:
            elements=j.replace('\n','').split(' ')
            pointcloud.addPoint(Point3D(elements[0],elements[1],elements[2]))
        temp=yuxiangGetVolume(pointcloud)
        name=i.split("/")[-1].split(".")[0]
        result.append([name,temp[0],temp[1]])
    for i in result:
        for j in i:
            file.write(j+"\t")
        file.write("\n")
    file.close()
    return result

# in : capList between 0 and 2PI
# out : capList continuous
def yuxiangCorrectCap(capList):
    order=np.argsort(capList)
    newCapList=[]
    for i in order:
        newCapList.append(capList[i])
    maxGap=0
    newMax=0
    for i in range(1,len(capList)):
        gap=newCapList[i-1]-newCapList[i]
        if gap>maxGap and gap>0.785:
            newMax=newCapList[i-1]
            print("Find new extremite : ",newMax)
    if newMax!=0:
        for i in capList:
            if i <=newMax:
                i+=np.pi*2
    return capList


# in : point cloud
# out : list of point gap paire
def yuxiangFindGapPoints(cloud,gap=0.5):
    out=[]
    for i in range(len(cloud.data)-1):
        if yuxiangDistanceTwoPts(cloud.data[i],cloud.data[i+1])>gap:
            out.append([cloud.data[i],cloud.data[i+1]])
    return out

def yuxiangFindGapPoints2(cloud,window=1):
    gapCloud = PointCloud()
    for i in cloud.data:
        out=0
        for j in cloud.data:
            if yuxiangCheckNeighor(i,j,window):
                out+=1
        print(out)
        if out<6:
            gapCloud.addPoint(i)
    return gapCloud

# in : separated two points
# out : point cloud with two original points and interpolated points
def yuxiangInterpolateTwoPoints(point1,point2,interMod="linear",gap=0.01):
    if interMod=="linear":
        out=PointCloud()
        vector=(point2-point1).unify()*gap
        nb=int(yuxiangDistanceTwoPts(point2,point1)//gap)
        out.addPoint(point1)
        for i in range(1,nb):
            out.addPoint(point1+vector*i)
        out.addPoint(point2)
    return out

# out : tangent between first and last point
def yuxiangGetTangent(pointList):
    startPt=pointList[0]
    endPt=pointList[-1]
    if (endPt.x-startPt.x)!=0:
        return (endPt.y-startPt.y)/(endPt.x-startPt.x)
    else:
        return 999999999

# seperate point cloud
# in : total cloud
# out : separated cloud in list
def yuxiangDevideCloudByDistance(pointcloud,threshold=1):
    out=[]
    data=pointcloud.data
    size=len(data)
    i=0
    while i <size:
        group = []
        group.append(data[i])
        data.pop(i)
        size-=1

        hasNeignor=False
        while not hasNeignor:
            hasNeignor = False
            for element in group:
                j = 0
                while j<size:
                    if yuxiangCheckNeighor(element,data[j],threshold):

                        group.append(data[j])
                        data.pop(j)
                        size -= 1
                        hasNeignor=True
                    else:
                        j += 1
        out.append(group)
        i += 1
    pointcloudList=[]
    for i in out:
        pc=PointCloud(i)
        pointcloudList.append(pc)
    return pointcloudList

# check if point1 and point2 are neigbors
def yuxiangCheckNeighor(point1,point2,threshold=0.3):
    if abs(point1.x-point2.x)<threshold and abs(point1.y-point2.y)<threshold and abs(point1.z-point2.z)<threshold:
        return True
    else:
        return False

def yuxiangCheckNeighor2D(point1, point2, threshold=0.3):
    if abs(point1.x - point2.x) < threshold and abs(point1.y - point2.y) < threshold:
        return True
    else:
        return False
# get the cap value from startPt to endPt
def yuxiangGetCap(startPt,endPt):
    deltaX=endPt.x-startPt.x
    deltaY=endPt.y-startPt.y
    a=None

    if deltaX>0 and deltaY>0:
        a=np.arctan(deltaX/deltaY)
    elif deltaX==0 and deltaY>0:
        a=0
    elif deltaX==0 and deltaY==0:
        a=None
    elif deltaX>0 and deltaY==0:
        a=np.pi/2
    elif deltaX>0 and deltaY<0:
        a=np.pi/2+np.abs(np.arctan(deltaY/deltaX))
    elif deltaX==0 and deltaY<0:
        a=np.pi
    elif deltaX<0 and deltaY < 0:
        a = np.pi+np.abs(np.arctan(deltaX/deltaY))
    elif deltaX < 0 and deltaY == 0:
        a=3*np.pi/2
    elif deltaX < 0 and deltaY >0:
        a = 3 * np.pi / 2+np.abs(np.arctan(deltaY/deltaX))
    return a

# in : point cloud in order
# out : surface of polygon
def yuxiangGetPolygonSurface(pointcloud):
    size=len(pointcloud.data)
    result=0
    data=pointcloud.data
    for i in range(-1,size-1):
        result+=data[i].x*data[i+1].y-data[i].y*data[i+1].x
    return np.abs(result/2)

# get a cloud volume
def yuxiangGetVolume(pointcloud,reference="min",mode="level_point"):
    outline = yuxiangFindOutLine(pointcloud, 16)
    outline.resample(1)
    newOutline = yuxiangSortPointCloud(outline)
    surface=yuxiangGetPolygonSurface(newOutline)
    data=pointcloud.data
    if reference=="min":
        zmin=outline.data[0].z
        for i in outline.data:
            if i.z<zmin:
                zmin=i.z
        zRef=zmin
    if reference=="mean":
        zmean=0
        for i in outline.data:
            zmean=zmean+i.z
        zmean=zmean/len(outline.data)
        zRef=zmean
    if reference=="meanf":
        zmin = outline.data[0].z
        for i in outline.data:
            if i.z < zmin:
                zmin = i.z
        zmean=0
        for i in outline.data:
            zmean=zmean+i.z
        zmean=zmean/len(outline.data)
        zRef=(zmean+4*zmin)/5
    zUp=[]
    zDown=[]
    for i in data:
        if i.z>zRef:
            zUp.append(i.z)
        else:
            zDown.append(i.z)
    ratio=len(zUp)/(len(zUp)+len(zDown))
    z_mean=0
    for i in zUp:
        z_mean += i - zRef
    z_mean=z_mean/len(zUp)
    surface=surface*ratio
    if mode=="fitting_plan":
        plane=yuxiangPlaneFitting(outline)
        cosz=plane.normal.z
        surface=surface*cosz
        volume=surface*z_mean*cosz**2
    elif mode=="level_point":
        volume = surface * z_mean
    return surface,volume

def yuxiangSortPointCloud(cloud,clockwise = True, offset = 0):
    Xc = 0
    Yc = 0
    Zc = 0
    size = len(cloud.data)
    for i in cloud.data:
        Xc += i.x
    Yc += i.y
    Zc += i.z
    center = Point3D(Xc / size - offset, Yc / size - offset, Zc / size - offset)
    cap = []
    for i in cloud.data:
        cap.append(yuxiangGetCap(center, i))
    cap = yuxiangCorrectCap(cap)
    order = np.argsort(cap)
    newData = []
    for i in order:
        newData.append(cloud.data[i])
    if not clockwise:
        tempData = []
    for i in range(size):
        tempData.append(newData[size - i - 1])
    newData = tempData
    return newData
# point  cloud plane fitting
def yuxiangPlaneFitting(pointcloud):
    points=[]
    for i in pointcloud.data:
        points.append([i.x,i.y,i.z])
    points = np.array(points).transpose()
    ctr = points.mean(axis=1)
    x = points - ctr[:, None]
    M = np.dot(x, x.T)  # Could also use cov(x) here.
    center, normal=ctr, svd(M)[0][:, -1]
    return Plane3D(Point3D(center[0],center[1],center[2]),Vector3D(normal[0],normal[1],normal[2]))

# Get the center track of a point cloud
def yuxiangFindCloudCenterTrack(pointcloud,researchZone=0.5):
    out=PointCloud()
    for i in pointcloud.data:
        temp = PointCloud()
        for j in pointcloud.data:
            if yuxiangCheckNeighor(i, j, researchZone):
                temp.addPoint(j)
        centerPt = yuxiangGetPointCloudCenter(temp)
        out.addPoint(centerPt)
    return out
def yuxiangCloudFittingInterpolation(cloud,fittingMode=Yuxiang.FittingMode_Line,interpolateTime=5):
    x=[]
    y=[]
    z_mean=0
    for i in cloud.data:
        x.append(i.x)
        y.append(i.y)
        z_mean+=i.z
    size=len(cloud.data)
    z_mean=z_mean/size
    xMax=max(x)
    xMin=min(x)
    interval=xMax-xMin
    newX=np.linspace(xMin-interpolateTime*interval,xMax+interpolateTime*interval,(2*interpolateTime+1)*size)
    if fittingMode==Yuxiang.FittingMode_Line:
        z=np.polyfit(x,y,1)
    p=np.poly1d(z)
    newCloud=PointCloud()
    for i in newX:
        newCloud.addPoint(Point3D(i,p(i),z_mean))
    return newCloud
# get the center of a cloud
def yuxiangGetPointCloudCenter(pointcloud):
    Xc=0
    Yc=0
    Zc=0
    size=len(pointcloud.data)
    for i in pointcloud.data:
        Xc+=i.x
        Yc+=i.y
        Zc+=i.z
    return Point3D(Xc/size,Yc/size,Zc/size)

# load point cloud from a file
def yuxiangLoadPointCloud(filename,type,typeCol=3,spliter=",",header=True,sort=False,autosave=False):
    file=open(filename,'r')
    if header==True:
        data=file.readlines()[1:]
    else:
        data=file.readlines()
    pointcloud=PointCloud()
    for i in data:
        i=i.replace("\n","").split(spliter)

        if str(i[typeCol])==type or float(i[typeCol])==float(type):
            point=Point3D(i[0],i[1],i[2],type=i[typeCol])

            pointcloud.addPoint(point)
    if sort==True:
        pointcloud.sort()
    if autosave==True:
        pointcloud.saveToFile("autosave_cloudRaw"+str(type)+".csv")
    return pointcloud

# find the contour outline of a isolated pointcloud
def yuxiangFindOutLine(pointcloud,directionNumber=8):
    outline = []
    outlineCloud = PointCloud()
    for i in pointcloud.data:
        direction = np.zeros((directionNumber,1))
        for j in pointcloud.data:
            pos = yuxiangGetCap(i, j)
            if pos != None:
                pos = int(pos // (2*np.pi / directionNumber))
                direction[pos] = 1
        if np.sum(direction) == directionNumber:
            outline.append(0)
        else:
            outline.append(1)
            outlineCloud.addPoint(i)
    return outlineCloud

# get distance of two 3D points
def yuxiangDistanceTwoPts(pt1, pt2,is3D=True):
    if is3D:
        return np.sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2 + (pt1.z - pt2.z) ** 2)
    else:
        return np.sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2)


# get line cloud intersection
# in : line with start point and direction
# out : intersection point list of two sides
def yuxiangLineCloudIntersection(line,pointcloud,tolerance=0.02,is3D=True):
    pt1 = line.startPoint
    pt2=pt1+line.direction
    out1=[]
    out2=[]
    for i in pointcloud.data:
        d1=yuxiangDistanceTwoPts(pt1,i,is3D)
        d2=yuxiangDistanceTwoPts(pt2,i,is3D)
        if d1>d2:
            if np.abs(d1-d2-1)<tolerance/d1:
                out1.append([i,d1])
        else:
            if np.abs(d2-d1-1)<tolerance/d1:
                out2.append([i, d1])
    return out1,out2

# in : line with start point and direction
# out : intersection point of line direction
def yuxiangRayCloudIntersection(line,pointcloud,toleranceIntersection=0.01,toleranceThickness=0.05,is3D=True):
    pt1=line.startPoint
    pt2=pt1+line.direction
    intersectionCloud=PointCloud()
    for i in pointcloud.data:
        d1=yuxiangDistanceTwoPts(pt1,i,is3D)
        d2=yuxiangDistanceTwoPts(pt2,i,is3D)
        if np.abs(d1-d2-1)<toleranceIntersection/d1:
            intersectionCloud.addPoint(i)
    return intersectionCloud

# find overlap of point and cloud
def yuxiangPointCloudOverlap(point, pointcloud, tolerance=0.15,is3D=False):
    overlap=False
    for i in pointcloud:
        if is3D==False:
            if yuxiangDistanceTwoPts(point,i,is3D)<tolerance:
                overlap=True
                return overlap
    return overlap


def yuxiangGetNearestPoints(referenceCloud,objectCloud): # return out : [ leftcloud, leftdistance, rightcloud, rightdistance]
    out=[]
    for i in range(referenceCloud.length()):
        vector=Vector3D(1,referenceCloud.normal[i],0)
        vector=vector.unify()
        line=Line3D(referenceCloud[i],vector=vector)
        out.append(yuxiangNearestLineCloudIntersection(line,objectCloud,tolerance=0.001,is3D=False))
    return out

def yuxiangFarestLineCloudIntersection(line,pointcloud,tolerance=0.01,is3D=False):
    point2=line.startPoint+line.direction
    dm1=0
    pm1=None
    dm2=0
    pm2=None

    for i in pointcloud.data:
        d1 = yuxiangDistanceTwoPts(line.startPoint, i, is3D)
        d2 = yuxiangDistanceTwoPts(point2, i, is3D)
        if np.abs(d1+d2-1)<tolerance:
            if d1 > dm1:
                dm1 = d1
                pm1 = i
        if np.abs(d2-d1-1)<tolerance:
            if d2 > dm2:
                dm2=d2
                pm2 = i
    return [pm1,dm1,pm2,dm2]
def yuxiangNearestLineCloudIntersection(line, pointcloud, tolerance=0.05,is3D=False):
    pt1 = line.startPoint
    pt2 = pt1 + line.direction
    nearestPt1=None
    nearestPt2=None
    nearestH1 = None
    nearestH2 = None
    nearestD1 = 10000
    nearestD2 = 10000

    highestPt1 = None
    highestPt2 = None
    highestH1=0
    highestH2=0
    highestD1=None
    highestD2=None
    zRef=pt1.z
    for i in pointcloud.data:
        d1 = yuxiangDistanceTwoPts(pt1, i,is3D)
        d2 = yuxiangDistanceTwoPts(pt2, i,is3D)

        if d1 > d2:
            if np.abs(d1 - d2 - 1) < tolerance:
                if d1<nearestD1:
                    nearestPt1=i
                    nearestD1=d1
                    nearestH1=i.z-zRef
                if i.z-zRef>highestH1:
                    highestPt1=i
                    highestH1= i.z-zRef
                    highestD1=d1
        else:
            if np.abs(d2 - d1 - 1) < tolerance:
                if d1<nearestD2:
                    nearestPt2=i
                    nearestD2=d1
                    nearestH2=i.z-zRef
                if i.z-zRef>highestH2:
                    highestPt2=i
                    highestH2= i.z-zRef
                    highestD2=d1
    if nearestPt1==None:
        nearestH1=None
        nearestD1=None
    if nearestPt2==None:
        nearestH2=None
        nearestD2=None
    if highestPt1==None:
        highestH1=None
        highestD1=None
    if highestPt2==None:
        highestH2=None
        highestD2=None
    return nearestPt1, nearestD1, nearestH1,highestPt1, highestD1, highestH1, nearestPt2, nearestD2, nearestH2, highestPt2, highestD2, highestH2

# find the middle track between two cloud
def yuxiangFindMiddleTrack(pointcloud1,pointcloud2):
    newpointcloud = PointCloud()
    crossfall=[]
    for i in range(pointcloud1.length()):
        min=10000
        index=0
        for j in range(pointcloud2.length()):
            d=yuxiangDistanceTwoPts(pointcloud1[i],pointcloud2[j])
            if d<min:
                min=d
                index=j
        newpointcloud.addPoint((pointcloud1[i]+pointcloud2[index])/2)
        x1=pointcloud1[i].x
        y1 = pointcloud1[i].y
        z1 = pointcloud1[i].z
        x2 = pointcloud2[index].x
        y2 = pointcloud2[index].y
        z2 = pointcloud2[index].z
        angle=(z2-z1)/np.sqrt((y2-y1)**2+(x2-x1)**2)
        crossfall.append(angle)
    return newpointcloud,crossfall


# 2D lind fitting by point list
def yuxiangLineFitting(point3dList,mode="xy"):
    x=[]
    y=[]
    z=[]
    para1=None
    if mode == "xy":
        for i in point3dList:
            x.append(i.x)
            y.append(i.y)
            # z.append(i.z)
        para1=np.polyfit(x,y,1)
    elif mode=="z":
        if len(point3dList)==3:
            x1=point3dList[1].x
            y1=point3dList[1].y
            z1 = point3dList[1].z
            x2 = point3dList[2].x
            y2 = point3dList[2].y
            z2 = point3dList[2].z
            para1=[0,(z2-z1)/(np.sqrt((x1-x2)**2+(y1-y2)**2))]
        if len(point3dList)==2:
            x1 = point3dList[0].x
            y1 = point3dList[0].y
            z1 = point3dList[0].z
            x2 = point3dList[1].x
            y2 = point3dList[1].y
            z2 = point3dList[1].z
            para1 =[0,(z2 - z1) / (np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))]
        if len(point3dList)>3:
            print("line fitting out of range")
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


def yuxiangCloudPolygonFittingInterpolation(cloud,degree=3,interpolateTime=10):
    x=[]
    y=[]
    z_mean=0
    for i in cloud.data:
        x.append(i.x)
        y.append(i.y)
        z_mean+=i.z
    size=len(cloud.data)
    z_mean=z_mean/size
    xMax=max(x)
    xMin=min(x)
    interval=xMax-xMin
    newX=np.linspace(xMin-interpolateTime*interval,xMax+interpolateTime*interval,(2*interpolateTime+1)*size)
    z=np.polyfit(x,y,degree)
    p=np.poly1d(z)
    newCloud=PointCloud()
    for i in newX:
        newCloud.addPoint(Point3D(i,p(i),z_mean))
    return newCloud


# find mirror of a vector
def yuxiangAxeMirror(vector, axe):
    dPhi = axe.phi - vector.phi
    dTheta = axe.theta - vector.theta
    x, y, z = vector.rotate(2 * dPhi, 2 * dTheta)
    return Vector3D(x, y, z)

def yuxiangCercle3Points(A,B,C):
    a = (C - B).getNorm()
    b = (C - A).getNorm()
    c = (B - A).getNorm()
    s = (a + b + c) / 2
    R = a * b * c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
    b1 = a * a * (b * b + c * c - a * a)
    b2 = b * b * (a * a + c * c - b * b)
    b3 = c * c * (a * a + b * b - c * c)
    # P=np.array([[A.x,B.x,C.x],[A.y,B.y,C.y],[A.z,B.z,C.z]]).dot(np.hstack((b1, b2, b3)))
    P=np.array([[A.x,B.x,C.x],[A.y,B.y,C.y],[A.z,B.z,C.z]]).dot(np.hstack((b1, b2, b3)))
    P /= b1 + b2 + b3
    center=Point3D(P[0],P[1],P[2])
    return Cercle(center,R)

def yuxiangCurvature3Points(A,B,C):
    a = (C - B).getNorm()
    b = (C - A).getNorm()
    c = (B - A).getNorm()
    s = (a + b + c) / 2
    R = a * b * c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
    return 1/R

