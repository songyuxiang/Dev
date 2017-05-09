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
class GpsBathyData:
    def __init__(self):
        self.gpsTime=None
        self.id=None
        self.bathyTime=None
        self.N=None
        self.E=None
        self.H=None
        self.numberSatelite=None
        self.precision=None
        self.depth=None
    def __str__(self):
        out=str(self.id)+","+str(self.N)+","+str(self.E)+","+str(self.H)+","+str(self.gpsTime)+","+str(self.numberSatelite)+","+str(self.precision)+","+str(self.depth)+","+str(self.bathyTime)
        return out

class DataArray:
    def __init__(self):
        self.data=[]
    def append(self,lineData):
        self.data.append(lineData)
    def __str__(self):
        out="nnnn,xxxxxxx.xx,yyyyyyy.yy,zzz.zz,hh.mm.ss,ss,p.p,h.hh,hh.mm.ss\n"
        for i in self.data:
            out+=str(i)+"\n"
        return  out
    def filterData(self):
        data=[]
        for i in self.data:
            if i.N==None or i.E==None or i.H==None or i.depth==None:
                continue
            data.append(i)
        self.data=data

def formatGpsData(data,format_org="ddmm.mmmmmmm",format_dest="dd.ddddd"):
    data=str(data)
    pointPos=data.find(".")
    d=data[pointPos-4:pointPos-2]
    m=data[pointPos-2:]
    out=int(d)+float(m)/60
    return str(out)

def yuxiangLoadGpsBathyData(filename):
    try:
        with open(filename,'r') as file:
            data=file.readlines()
        dataArray=DataArray()

        for lineNb in range(len(data)):
            lineData=GpsBathyData()
            elements=data[lineNb].replace('\n',"").split(',')
            posM = 1000
            lineData.id = lineNb
            for i in range(len(elements)):
                # print(elements)
                try:

                    lineData.bathyTime=elements[0][9:]
                    if elements[i]=="M":
                        if posM>i:
                            posM=i
                            if elements[posM-1]!="":
                                lineData.H=float(elements[posM-1])
                    if elements[i]=="N":
                        if elements[i - 1] != "":
                            lineData.N=float(formatGpsData(elements[i-1]))
                    if elements[i]=="S":
                        if elements[i - 1] != "":
                            lineData.N=-float(formatGpsData(elements[i-1]))
                    if elements[i]=="W":

                        if elements[i - 1] != "":
                            lineData.E=-float(formatGpsData(elements[i-1]))
                    if elements[i]=="E":
                        if elements[i - 1] != "":
                            lineData.E=float(formatGpsData(elements[i-1]))
                    if elements[i].find("GPGGA")>0:
                        if elements[i + 1] != "":
                            lineData.gpsTime=elements[i+1]

                except:
                    print("can't load data")
            dataArray.append(lineData)
        return dataArray
    except:
        print("could not open this file")
        return []


class mainwindow(QMainWindow,bathypost.Ui_BathyPost):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton_Browser.clicked.connect(self.loadData)
        self.pushButton_Calculate.clicked.connect(self.calculate)
        self.data=DataArray()
    def loadData(self):
        filename,_=QFileDialog.getOpenFileName()
        self.lineEdit_DataBrowser.setText(filename)
        self.data=yuxiangLoadGpsBathyData(filename)
        self.plainTextEdit_RawData.setPlainText(str(self.data))
        self.pushButton_Calculate.setEnabled(True)
    def calculate(self):
        projection=self.comboBox_zone.currentText()[-2:]
        self.gpsData.filterData()
        data=self.data.data
        out=""
        for i in range(len(self.gpsData.data)):
            # self.gpsData.dataCC[i].N,self.gpsData.dataCC[i].W,self.gpsData.dataCC[i].H= yuxiangProjection.WGS84ToCC(self.gpsData.dataWGS[i].N,self.gpsData.dataWGS[i].W,self.gpsData.dataWGS[i].H,self.comboBox_zone.currentText()[-2:])
            # print(self.gpsData.dataWGS[i].N,self.gpsData.dataWGS[i].W,self.gpsData.dataWGS[i].H,self.comboBox_zone.currentText()[-2:])
            x,y,z= yuxiangProjection.WGS84ToCC(self.gpsData.data[i].W,self.gpsData.data[i].N,self.gpsData.data[i].H,projection)
            out+=str(x)+","+str(y)+","+str(z)+"\n"
        self.plainTextEdit_result.setPlainText(out)
if __name__=='__main__':
    app=QApplication(sys.argv)
    form=mainwindow()
    form.show()
    print(formatGpsData("4446.6757598"))
    app.exec_()