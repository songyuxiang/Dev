from numpy import *
from numpy.linalg import svd
def planeFit(points):
    points=array(points).transpose()
    ctr = points.mean(axis=1)
    x = points - ctr[:,None]
    M = dot(x, x.T) # Could also use cov(x) here.
    return ctr, svd(M)[0][:,-1]
def changeListType(list,type):
    def changeType(a,type):
        if type=='s':
            return str(a)
        elif type=='f':
            return float(a)
        elif type=='d':
            return int(a)
    size=len(shape(list))
    if size==0:
        return  changeType(list)
    elif size==1:
        out=[]
        for i in list:
            out.append(changeType(i,type))
        return out
    elif size==2:
        out=[]
        for i in list:
            l = []
            for j in i:
                l.append(changeType(j,type))
            out.append(l)
        return out

pointCloud=[]
with open("cloudpoint.txt",'r') as file:
    data=file.readlines()
for i in data:
    temp=i.replace('\n', "").split(' ')[:3]
    pointCloud.append(temp)
pointCloud=changeListType(pointCloud,'f')
print(planeFit(pointCloud))