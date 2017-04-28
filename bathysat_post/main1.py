from PyQt5.Qt import *
import sys
import bathypost
import pyproj
class yuxiangProjection:
    def WGS84ToCC(lon,lat,elevation,zone):
        wgs=pyproj.Proj(init='epsg:4326')
        cc=pyproj.Proj(init="epsg:39%s"%(str(zone)))
        x2, y2, z2 = pyproj.transform(wgs, cc, lon, lat, elevation)
        return x2, y2, z2


def yuxiangPrintList(list,dimension="1",spliter=","):
    out=""
    if dimension=="1":
        for i in list:
            out+=str(i)+spliter
        out=out[:-1]
        out+='\n'
        return out
    if dimension=="2":
        for i in list:
            line=""
            for j in i:
                line+=str(j)+spliter
            line=line[:-1]
            line+='\n'
            out+=line
        return out
    else:
        print("invalid dimension number")
class GpsData:
    def __init__(self):
        self.gpsTime=None
        self.id=None
        self.bathyTime=None
        self.N=None
        self.S=None
        self.E=None
        self.W=None
        self.H=None
        self.numberSatelite=None
        self.precision=None
        self.depth=None
        self.header=[]
    def setHeader(self,header):
        self.header=header
    def __str__(self):
        data=[]
        for i in self.header:
            if i=="UTC Time":
                data.append(self.gpsTime)
            if i=="N":
                data.append(self.N)
            if i ==  "S" :
                data.append(self.S)
            if i == "E":
                data.append(self.E)
            if i=="W":
                data.append(self.W)
            if i=="H":
                data.append(self.H)
            if i=="Number of satelites":
                data.append(self.numberSatelite)
            if i=="Precision":
                data.append(self.precision)
            if i=="Depth":
                data.append(self.depth)
            if i=="Bathy Time":
                data.append(self.bathyTime)
        return yuxiangPrintList(data)
    def getHeader(self):
        header = []
        data = []
        if self.gpsTime != None:
            header.append("UTC Time")
            data.append(self.gpsTime)
        if self.N != None:
            header.append("N")
            data.append(self.N)

            data.append(self.N)
        if self.S != None:
            header.append("S")
            data.append(self.S)
        if self.E != None:
            header.append("E")
            data.append(self.E)
        if self.W != None:
            header.append("W")
            data.append(self.W)
        if self.H != None:
            header.append("H")
        if self.numberSatelite != None:
            header.append("Number of satelites")
            data.append(self.numberSatelite)
        if self.precision != None:
            header.append("Precision")
            data.append(self.precision)
        if self.depth != None:
            header.append("Depth")
            data.append(self.depth)
        if self.bathyTime != None:
            header.append("Bathy Time")
            data.append(self.bathyTime)
        self.header=header
        return header
class GpsArray:
    def __init__(self):
        self.data=[]
        self.header=[]
    def append(self,gpsData):
        self.data.append(gpsData)
    def __str__(self,system="WGS"):
        if system=="WGS":
            out=""
            self.updateHeader()
            out+=yuxiangPrintList(self.header)
            for i in self.data:
                i.setHeader(self.header)
                out+=str(i)
            return out

    def updateHeader(self):
        header=[]
        for i in self.data:
            if len(i.getHeader())>len(header):
                header=i.header
        self.header=header
    def filterData(self):
        data=[]
        for i in self.data:
            noNullNumber = 0
            if i.N!=None:
                noNullNumber+=1
            if i.E!=None:
                noNullNumber+=1
            if i.S!=None:
                noNullNumber+=1
            if i.W!=None:
                noNullNumber+=1
            if i.H!=None:
                noNullNumber+=1
            if noNullNumber>=3:
                data.append(i)
        self.data=data
def formatGpsData(data,format_org="ddmm.mmmmmmm",format_dest="dd.ddddd"):
    data=str(data)
    pointPos=data.find(".")
    d=data[pointPos-4:pointPos-2]
    m=data[pointPos-2:]
    out=int(d)+float(m)/60
    return str(out)
def yuxiangLoadGpsRawData(filename):
    try:
        with open(filename,'r') as file:
            data=file.readlines()
        gpsData=GpsArray()

        for line in data:
            gps=GpsData()
            elements=line.replace('\n',"").split(',')
            posM = 1000
            for i in range(len(elements)):
                # print(elements)
                try:

                    gps.bathyTime=elements[0][9:]
                    if elements[i]=="M":
                        if posM>i:
                            posM=i
                            if elements[posM-1]!="":
                                gps.H=elements[posM-1]
                    if elements[i]=="N":
                        if elements[i - 1] != "":
                            gps.N=formatGpsData(elements[i-1])
                    if elements[i]=="S":
                        if elements[i - 1] != "":
                            gps.S=formatGpsData(elements[i-1])
                    if elements[i]=="W":
                        if elements[i - 1] != "":
                            gps.W=formatGpsData(elements[i-1])
                    if elements[i]=="E":
                        if elements[i - 1] != "":
                            gps.E=formatGpsData(elements[i-1])
                    if elements[i].find("GPGGA")>0:
                        if elements[i + 1] != "":
                            gps.gpsTime=elements[i+1]

                except:
                    print("can't load data")
            gpsData.append(gps)
        return gpsData
    except:
        print("could not open this file")
        return []


class mainwindow(QMainWindow,bathypost.Ui_BathyPost):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton_browserGps.clicked.connect(self.loadGps)
        self.pushButton_calculate.clicked.connect(self.calculate)
        self.gpsData=GpsArray()
    def loadGps(self):
        filename,_=QFileDialog.getOpenFileName()
        self.lineEdit_gpsBrowser.setText(filename)
        self.gpsData=yuxiangLoadGpsRawData(filename)
        self.plainTextEdit_gps.setPlainText(str(self.gpsData))
        self.pushButton_calculate.setEnabled(True)
    def calculate(self):
        projection=self.comboBox_zone.currentText()[-2:]
        self.gpsData.filterData()
        data=self.gpsData.data
        out=""
        for i in range(len(self.gpsData.data)):
            # self.gpsData.dataCC[i].N,self.gpsData.dataCC[i].W,self.gpsData.dataCC[i].H= yuxiangProjection.WGS84ToCC(self.gpsData.dataWGS[i].N,self.gpsData.dataWGS[i].W,self.gpsData.dataWGS[i].H,self.comboBox_zone.currentText()[-2:])
            # print(self.gpsData.dataWGS[i].N,self.gpsData.dataWGS[i].W,self.gpsData.dataWGS[i].H,self.comboBox_zone.currentText()[-2:])
            x,y,z= yuxiangProjection.WGS84ToCC(self.gpsData.data[i].N,self.gpsData.data[i].W,self.gpsData.data[i].H,projection)
            out+=str(x)+","+str(y)+","+str(z)+"\n"
        self.plainTextEdit_result.setPlainText(out)
if __name__=='__main__':
    app=QApplication(sys.argv)
    form=mainwindow()
    form.show()
    print(formatGpsData("4446.6757598"))
    app.exec_()