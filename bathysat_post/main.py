from PyQt5.Qt import *
import sys
from yuxiangDataArray import *


import mainwindow

class mainwindow(QMainWindow,mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton_importBathyData.clicked.connect(self.importBathyData)
        self.pushButton_importGpsData.clicked.connect(self.importGpsData)
        self.timeEdit_BathyTime.dateTimeChanged.connect(self.changeBathyTime)
        self.timeEdit_GpsTime.dateTimeChanged.connect(self.changeGpsTime)
        self.pushButton_Match.clicked.connect(self.matchBathyGps)
        self.gpsData=DataArray()
        self.bathyData=DataArray()
        self.bathyReferenceList=None
        self.gpsReferenceList=None
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Q:
            self.close()
    def importBathyData(self):
        filename,_=QFileDialog.getOpenFileName()
        self.bathyData=loadBathyData(filename)
        self.printLeft(self.bathyData)
        self.bathyReferenceList=self.bathyData.checkAllStatics(parametersList=["Depth","A","N","W"])
        for i in self.bathyReferenceList:
            self.comboBox_BathyReferencePoint.addItem(str(self.bathyData.at(i)))
    def importGpsData(self):
        filename,_=QFileDialog.getOpenFileName()
        self.gpsData=loadGpsData(filename)
        self.printRight(self.gpsData)
        self.gpsReferenceList = self.gpsData.checkAllStatics(parametersList=["Elev","N", "E"])
        for i in self.gpsReferenceList:
            self.comboBox_GpsReferencePoint.addItem(str(self.gpsData.at(i)))
    def printLeft(self,data):
        self.plainTextEdit_BathyTerminal.setPlainText(str(data))
    def printRight(self,data):
        self.plainTextEdit_GpsTerminal.setPlainText(str(data))
    def changeBathyTime(self):
        print("changed")
    def changeGpsTime(self):
        for i in self.gpsData.size():
            data=self.gpsData.at(i)
    def compareTime(self,time1,time2,spliter1=':',spliter2=':'):
        t1=time1.split(spliter1)
        t2=time2.split(spliter2)
        h1 = int(t1[1])
        h2 = int(t2[1])
        m1 = int(t1[2])
        m2 = int(t2[2])
        s1 = float(t1[3])+m1*60+h1*60*60
        s2 = float(t2[3])+m2*60+h2*60*60
        if s1>s2:
            return ">"
        elif s1==s2:
            return "="
        else:
            return "<"
    def matchBathyGps(self):
        bathyIndex=self.bathyReferenceList[self.comboBox_BathyReferencePoint.currentIndex()]
        gpsIndex=self.gpsReferenceList[self.comboBox_GpsReferencePoint.currentIndex()]
        newArray=linkDataArray(self.bathyData,bathyIndex,self.gpsData,gpsIndex)
        self.plainTextEdit_MatchResult.setPlainText(str(newArray))
if __name__=='__main__':
    app=QApplication(sys.argv)
    form=mainwindow()
    form.show()
    app.exec_()