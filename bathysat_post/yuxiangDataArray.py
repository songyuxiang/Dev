import numpy as np
def loadBathyData(filename):
    try:
        with open(filename,'r') as file:
            data=file.readlines()
        allInfo=DataArray()
        for line in data:
            info=BathyData()
            temp=line.split(',')
            for i in range(len(temp)):

                if temp[i]=='M':
                    info.setDepth(temp[i-1])
                if temp[i]=='A':
                    info.setA(temp[i-1])
                if temp[i]=='N':
                    info.setN(temp[i-1])
                if temp[i]=='E':
                    info.setE(temp[i-1])
                if temp[i]=='S':
                    info.setS(temp[i-1])
                if temp[i]=='W':
                    info.setW(temp[i-1])
                if temp[i].find("DateTime")>0 and i==0:
                    info.setTime(temp[i][9:])
                    info.setDate(temp[i+1][:10])
            allInfo.append(info)
        return allInfo
    except IOError:
        print("could not open file")
        return None

def loadGpsData(filename,headerIndex=0,dataStartIndex=1,spliter=','):
    try:
        with open(filename,'r') as file:
            data=file.readlines()
        header=data[headerIndex].split(spliter)
        x=header.index("End Time")
        data=data[dataStartIndex:]
        allInfo=DataArray()
        for line in data:
            info=GpsData()
            temp=line.split(',')
            for i in range(len(header)):
                if header[i] == 'Point':
                    info.setID(temp[i])
                if header[i]=='North':
                    info.setN(temp[i])
                if header[i]=='East':
                    info.setE(temp[i])
                if header[i] == 'Elev':
                    info.setElev(temp[i])
                if header[i] == 'End Time':
                    info.setTime(temp[i])
                if header[i] == 'End Date':
                    info.setDate(temp[i])
            allInfo.append(info)

        return allInfo
    except:
        print("could not open this file")
        return None

def linkDataArray(arrayBathy,indexBathy,arrayGps,indexGps,hDiff):
    newArray=DataArray()

    for i in range(indexGps,arrayGps.size()):
        if indexBathy+i<arrayBathy.size():
            newData = GpsData(ID=arrayGps.at(i).ID,N=arrayGps.at(i).N,E=arrayGps.at(i).E,W=arrayGps.at(i).W,S=arrayGps.at(i).S,Elev=arrayGps.at(i).Elev,Date=arrayGps.at(i).Date,Time=arrayGps.at(i).Time)
            linkBathyGps(arrayBathy.at(indexBathy+i),newData)
            if newData.Elev!=None and arrayBathy.at(indexBathy+i).Depth!=None:
                newData.setElev(str(float(newData.Elev)-float(hDiff)-float(arrayBathy.at(indexBathy+i).Depth)))
            newArray.append(newData)
    return newArray
def linkBathyGps(dataBathy,dataGps):
    dataGps.setDepth(dataBathy.Depth)
    return dataGps

class BathyData:
    def __init__(self,Date=None,Time=None,Depth=None,A=None,N=None,W=None,S=None,E=None):
        self.Date=Date
        self.Time=Time
        self.Depth=Depth
        self.A=A
        self.N=N
        self.W=W
        self.S = S
        self.E = E
    def setDate(self,Date):
        self.Date=Date
    def setTime(self,Time):
        self.Time=Time
    def setDepth(self,Depth):
        self.Depth=Depth
    def setA(self,A):
        self.A=A
    def setE(self, E):
        self.E = E
    def setS(self, S):
        self.S = S
    def setN(self,N):
        self.N=N
    def setW(self,W):
        self.W=W
    def __str__(self):
        out=""
        if self.Date!=None:
            out+="Date:"+self.Date+" || "
        if self.Time!=None:
            out+="Time:"+self.Time+" || "
        if self.Depth!=None:
            out+="Depth:"+self.Depth+"m"+" || "
        if self.A!=None:
            out+="A:"+self.A+" || "
        if self.N!=None:
            out+="N:"+self.N+" || "
        if self.W!=None:
            out+="W:"+self.W+" || "
        if self.S!=None:
            out+="S:"+self.S+" || "
        if self.E!=None:
            out+="E:"+self.E+" || "
        return out
class GpsData:
    def __init__(self,ID=None,N=None,E=None,W=None,S=None,Elev=None,Date=None,Time=None):
        self.Date = Date
        self.Time = Time
        self.Elev = Elev
        self.E = E
        self.W = W
        self.N = N
        self.S = S
        self.ID=ID
        self.Depth=None
    def setDate(self,Date):
        self.Date=Date
    def setTime(self,Time):
        self.Time=Time
    def setElev(self,Elev):
        self.Elev=Elev
    def setN(self,N):
        self.N=N
    def setW(self,W):
        self.W=W
    def setE(self,E):
        self.E=E
    def setDepth(self,Depth):
        self.Depth=Depth
    def setID(self,id):
        self.ID=id
    def __str__(self):
        out=""
        if self.ID!=None:
            out+="ID:"+self.ID+" || "
        if self.Date!=None:
            out+="Date:"+self.Date+" || "
        if self.Time!=None:
            out+="Time:"+self.Time+" || "
        if self.N!=None:
            out+="N:"+self.N+" || "
        if self.E!=None:
            out+="E:"+self.E+" || "
        if self.S!=None:
            out+="S:"+self.S+" || "
        if self.W!=None:
            out+="W:"+self.W+" || "
        if self.Elev!=None:
            out+="Elevation:"+self.Elev+" || "
        if self.Depth!=None:
            out+="Depth:"+self.Depth+" || "
        return out
class DataArray:
    def __init__(self):
        self.dataArray=[]
    def append(self,data):
        self.dataArray.append(data)
    def at(self,i):
        return self.dataArray[i]
    def size(self):
        return len(self.dataArray)
    def checkStatic(self,i,parametersList):
        if i<1:
            print("index has to be greater than 1")
        elif len(self.dataArray)<2:
            print("length of data array needs to be greater than 2")
        else:
            out={}
            trueNumber=0
            isStatic=False
            if "Depth" in parametersList and self.dataArray[i].Depth!=None and self.dataArray[i-1].Depth!=None:
                depth0=self.dataArray[i].Depth
                depth1 = self.dataArray[i-1].Depth
                if np.abs(float(depth1)-float(depth0))<0.01:

                    out["Depth"]=True
                else:
                    out["Depth"]=False
            if "A" in parametersList and self.dataArray[i].A!=None and self.dataArray[i-1].A!=None:
                A0 = self.dataArray[i].A
                A1 = self.dataArray[i - 1].A
                if np.abs(float(A1) - float(A0)) <0.01:
                    out["A"] = True
                else:
                    out["A"] = False
            if "N" in parametersList and self.dataArray[i].N!=None and self.dataArray[i-1].N!=None:
                N0 = self.dataArray[i].N
                N1 = self.dataArray[i - 1].N
                if np.abs(float(N1) - float(N0))<0.05:
                    out["N"] = True
                else:
                    out["N"] = False
            if "E" in parametersList and self.dataArray[i].E!=None and self.dataArray[i-1].E!=None:
                E0 = self.dataArray[i].E
                E1 = self.dataArray[i - 1].E
                if np.abs(float(E1) - float(E0)) <0.05:
                    out["E"] = True
                else:
                    out["E"] = False
            if "Elev" in parametersList and self.dataArray[i].Elev!=None and self.dataArray[i-1].Elev!=None:
                Elev0 = self.dataArray[i].Elev
                Elev1 = self.dataArray[i - 1].Elev
                if np.abs(float(Elev1) - float(Elev0)) <0.05:
                    out["Elev"] = True
                else:
                    out["Elev"] = False
            if "W" in parametersList and self.dataArray[i].W!=None and self.dataArray[i-1].W!=None:
                W0 = self.dataArray[i].W
                W1 = self.dataArray[i - 1].W
                if np.abs(float(W1) - float(W0)) <0.05:
                    out["W"] = True
                else:
                    out["W"] = False
            if "S" in parametersList and self.dataArray[i].S!=None and self.dataArray[i-1].S!=None:
                S0 = self.dataArray[i].S
                S1 = self.dataArray[i - 1].S
                if np.abs(float(S1) - float(S0)) <0.01:
                    out["S"] = True
                else:
                    out["S"] = False
            for i in out.values():
                if i==True:
                    trueNumber+=1
            # print(out,len(parametersList),trueNumber)
            if len(parametersList)==trueNumber:
                isStatic=True
            return out,isStatic
    def checkAllStatics(self,parametersList):
        staticList=[]
        restartPoint=[]
        beginStatic=False
        for i in range(1,len(self.dataArray)):
            out,isStatic=self.checkStatic(i,parametersList)
            if isStatic==True:
                staticList.append(i)
        for i in range(1,len(staticList)-1):
            if staticList[i]-staticList[i-1]<10 and staticList[i+1]-staticList[i]<10:
                beginStatic=True
            while beginStatic==True:
                if staticList[i + 1] - staticList[i] > 10:
                    beginStatic=False
                    restartPoint.append(staticList[i])
                else:
                    break
        return restartPoint
    def __str__(self):
        out=""
        for i in self.dataArray:
            out+=str(i)+'\n'
        return out
