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
        self.Ncc=None
        self.Ecc=None
        self.Hcc=None
        self.numberSatelite=None
        self.precision=None
        self.depth=None
        self.gpsHeight=None
        self.trueElevation=None
    def __str__(self):
        if self.Ecc!=None and self.Ncc!=None and self.Hcc!=None:
                out=str(self.id)+","+str(self.Ncc)+","+str(self.Ecc)+","+str(self.trueElevation)+","+str(self.gpsTime)+","+str(self.numberSatelite)+","+str(self.precision)+","+str(self.depth)+","+str(self.bathyTime)
        else:
            out=str(self.id)+","+str(self.N)+","+str(self.E)+","+str(self.H)+","+str(self.gpsTime)+","+str(self.numberSatelite)+","+str(self.precision)+","+str(self.depth)+","+str(self.bathyTime)
        return out

class DataArray:
    def __init__(self):
        self.data=[]
    def append(self,lineData):
        self.data.append(lineData)
    def __str__(self):
        out="nnnn,xxxxxxx.xx,yyyyyyy.yy,zzz.zz,hh.mm.ss,ss,p.p,h.hh,hh.mm.ss,yy-mm-dd\n"
        for i in self.data:
            out+=str(i)+"\n"
        return  out
    def filterData(self):
        data=[]
        for i in self.data:
            if i.N==None or i.E==None or i.H==None or i.depth==None:
            # if i.N == None or i.E == None or i.H == None:
                continue
            data.append(i)
        self.data=data

def formatGpsData(data,format_org="ddmm.mmmmmmm",format_dest="dd.ddddd"):
    data=str(data)
    pointPos=data.find(".")
    d=data[pointPos-4:pointPos-2]
    m=data[pointPos-2:]
    out=int(d)+float(m)/60
    return float(out)

def yuxiangLoadGpsBathyData(filename):
    try:
        with open(filename,'r') as file:
            data=file.readlines()
        dataArray=DataArray()

        for lineNb in range(len(data)):
            lineData=GpsBathyData()
            l=data[lineNb].replace("\'","")
            pos_GPGGA=l.find("$GPGGA")
            gpsElements=l[pos_GPGGA:].split(',')
            pos_SDDPT=l.find("$SDDPT")
            bathyElements=l[pos_SDDPT:].split(',')
            lineData.id = lineNb
            try:
                lineData.bathyTime=data[lineNb][9:28]

                if gpsElements[1]!='':
                    lineData.gpsTime=gpsElements[1]

                if gpsElements[3]=='N':
                    lineData.N = float(formatGpsData(gpsElements[2]))
                elif gpsElements[3]=='S':
                    lineData.N = -float(formatGpsData(gpsElements[2]))
                if gpsElements[5]=='E':
                    lineData.E=float(formatGpsData(gpsElements[4]))
                elif gpsElements[5]=='W':
                    lineData.E = -float(formatGpsData(gpsElements[4]))
                if gpsElements[7]!='':
                    lineData.numberSatelite=int(gpsElements[7])
                if gpsElements[8] != '':
                    lineData.precision = float(gpsElements[8])
                if gpsElements[9] != '':
                    lineData.H = float(gpsElements[9])
                if bathyElements[1]!='':
                    lineData.depth=float(bathyElements[1])

            except:
                print("can't load data")
            dataArray.append(lineData)
        return dataArray
    except:
        print("could not open this file")
        return []

def yuxiangList2StandardModel(list,hasHeader=True):
    model = QStandardItemModel()
    if hasHeader==True:
        model.setHorizontalHeaderLabels(list[0])
        list=list[1:]
    size1=len(list)
    try:
        size2=len(list[0])
    except:
        size2=None
    if size1!=None and size2!=None:
        for i in range(size1):
            for j in range(size2):
                try:
                    item=QStandardItem(str(list[i][j]))
                    model.setItem(i,j,item)
                except:
                    item = QStandardItem("")
                    model.setItem(i, j, item)
    elif size1!=None and size2==None:
        for i in range(size1):
            item=QStandardItem(str(list[i]))
            model.setItem(0,i,item)
    return model

def yuxiangStandardModel2List(model,hasHeader=True):
    r = model.rowCount()
    c = model.columnCount()
    table = []
    if hasHeader:
        header = []
        for col in range(c):
            header.append(model.headerData(col, Qt.Horizontal))
        table.append(header)
    for i in range(r):
        row = []
        for j in range(c):
            row.append(model.data(model.index(i, j)))
        table.append(row)
    return table

def getModelDataByIndex(model,i,j):
    return model.data(model.index(i, j))

def yuxiangList2StandardModel(list,hasHeader=True):
    model = QStandardItemModel()
    if hasHeader==True:
        model.setHorizontalHeaderLabels(list[0])
        list=list[1:]
    size1=len(list)
    try:
        size2=len(list[0])
    except:
        size2=None
    if size1!=None and size2!=None:
        for i in range(size1):
            for j in range(size2):
                try:
                    item=QStandardItem(str(list[i][j]))
                    model.setItem(i,j,item)
                except:
                    item = QStandardItem("")
                    model.setItem(i, j, item)
    elif size1!=None and size2==None:
        for i in range(size1):
            item=QStandardItem(str(list[i]))
            model.setItem(0,i,item)
    return model


class mainwindow(QMainWindow,bathypost.Ui_BathyPost):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton_Browser.clicked.connect(self.loadData)
        self.pushButton_Calculate.clicked.connect(self.calculate)
        self.pushButton_Save.clicked.connect(self.save)
        self.dataArray=DataArray()
    def loadBathyGpsFile(self,filename):
        try:
            with open(filename, 'r') as file:
                data = file.readlines()
            dataArray = DataArray()

            for lineNb in range(len(data)):
                lineData = GpsBathyData()
                l = data[lineNb].replace("\'", "")
                pos_GPGGA = l.find("$GPGGA")
                gpsElements = l[pos_GPGGA:].split(',')
                pos_SDDPT = l.find("$SDDPT")
                bathyElements = l[pos_SDDPT:].split(',')
                lineData.id = lineNb
                try:
                    lineData.bathyTime = data[lineNb][9:28]

                    if gpsElements[1] != '':
                        lineData.gpsTime = gpsElements[1]

                    if gpsElements[3] == 'N':
                        lineData.N = float(formatGpsData(gpsElements[2]))
                    elif gpsElements[3] == 'S':
                        lineData.N = -float(formatGpsData(gpsElements[2]))
                    if gpsElements[5] == 'E':
                        lineData.E = float(formatGpsData(gpsElements[4]))
                    elif gpsElements[5] == 'W':
                        lineData.E = -float(formatGpsData(gpsElements[4]))
                    if gpsElements[7] != '':
                        lineData.numberSatelite = int(gpsElements[7])
                    if gpsElements[8] != '':
                        lineData.precision = float(gpsElements[8])
                    if gpsElements[9] != '':
                        lineData.H = float(gpsElements[9])
                    if bathyElements[1] != '':
                        lineData.depth = float(bathyElements[1])
                    try :
                        temp=self.lineEdit_GpsHeight.text().replace(",",".")
                        lineData.gpsHeight=float(temp)
                    except TypeError:
                        print("wrong type")
                        lineData.gpsHeight=0
                        self.lineEdit_GpsHeight.setText("0")
                except:
                    print("can't load data")
                dataArray.append(lineData)
            return dataArray
        except:
            print("could not open this file")
            return []
    def loadData(self):
        filename,_=QFileDialog.getOpenFileName()
        self.lineEdit_DataBrowser.setText(filename)
        self.dataArray=self.loadBathyGpsFile(filename)
        self.loadDataArray1()
        self.pushButton_Calculate.setEnabled(True)
    def loadDataArray1(self):
        data=str(self.dataArray)
        line=data.split("\n")
        all=[]
        for i in line:
            all.append(i.split(','))
        model=yuxiangList2StandardModel(all)
        self.tableView.setModel(model)
    def loadDataArray2(self):
        data=str(self.dataArray)
        line=data.split("\n")
        all=[]
        for i in line:
            all.append(i.split(','))
        model=yuxiangList2StandardModel(all)
        self.tableView_2.setModel(model)
    def calculate(self):
        projection=self.comboBox_CCZone.currentText()[-2:]
        self.dataArray.filterData()
        out=""
        for i in range(len(self.dataArray.data)):
            # self.gpsData.dataCC[i].N,self.gpsData.dataCC[i].W,self.gpsData.dataCC[i].H= yuxiangProjection.WGS84ToCC(self.gpsData.dataWGS[i].N,self.gpsData.dataWGS[i].W,self.gpsData.dataWGS[i].H,self.comboBox_zone.currentText()[-2:])
            # print(self.gpsData.dataWGS[i].N,self.gpsData.dataWGS[i].W,self.gpsData.dataWGS[i].H,self.comboBox_zone.currentText()[-2:])
            self.dataArray.data[i].Ecc,self.dataArray.data[i].Ncc,self.dataArray.data[i].Hcc= yuxiangProjection.WGS84ToCC(self.dataArray.data[i].E,self.dataArray.data[i].N,self.dataArray.data[i].H,projection)
            self.dataArray.data[i].trueElevation=self.dataArray.data[i].Hcc-self.dataArray.data[i].depth-float(self.lineEdit_GpsHeight.text())
        self.loadDataArray2()
        self.pushButton_Save.setEnabled(True)
    def save(self):
        try:
            filename,_=QFileDialog.getSaveFileName()
            file=open(filename,'w')
            file.write(str(self.dataArray))
            file.close()
        except:
            print("cloud not open this file")
if __name__=='__main__':
    app=QApplication(sys.argv)
    form=mainwindow()
    form.show()
    app.exec_()