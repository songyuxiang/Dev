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
        self.timeEdit_BathyStartTime.dateTimeChanged.connect(self.changeBathyTime)
        self.timeEdit_GpsStartTime.dateTimeChanged.connect(self.changeGpsTime)
        self.pushButton_Match.clicked.connect(self.matchBathyGps)
        self.lineEdit_Hdiff.editingFinished.connect(self.hDiffChange)
        self.gpsData=DataArray()
        self.bathyData=DataArray()
        self.postBathyData=DataArray()
        self.postGpsData=DataArray()
        self.bathyReferenceList=None
        self.gpsReferenceList=None
        self.bathyParameterList=[]
        self.gpsParameterList=[]
        self.Hdiff=0
    def hDiffChange(self):
        self.Hdiff=float(self.lineEdit_Hdiff.text())
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Q:
            self.close()
    def importBathyData(self):
        filename,_=QFileDialog.getOpenFileName()
        self.bathyData=loadBathyData(filename)
        self.postBathyData=self.bathyData
        if self.bathyData!=None:
            self.updateParameterList()
            self.printLeft(self.bathyData)
            self.bathyReferenceList=self.bathyData.checkAllStatics(parametersList=self.bathyParameterList)
            self.comboBox_BathyReferencePoint.clear()
            for i in self.bathyReferenceList:
                self.comboBox_BathyReferencePoint.addItem(str(self.bathyData.at(i)))
        else:
            print("cloud not open this file")
    def importGpsData(self):
        filename,_=QFileDialog.getOpenFileName()
        self.gpsData=loadGpsData(filename)
        self.postGpsData=self.gpsData
        if not self.gpsData==None:
            self.updateParameterList()
            self.printRight(self.gpsData)
            self.gpsReferenceList = self.gpsData.checkAllStatics(parametersList=self.gpsParameterList)
            self.comboBox_GpsReferencePoint.clear()
            for i in self.gpsReferenceList:
                self.comboBox_GpsReferencePoint.addItem(str(self.gpsData.at(i)))
        else:
            print("could not open this gps file")
    def printLeft(self,data):
        self.plainTextEdit_BathyTerminal.setPlainText(str(data))
    def printRight(self,data):
        self.plainTextEdit_GpsTerminal.clear()
        self.plainTextEdit_GpsTerminal.setPlainText(str(data))
    def changeBathyTime(self):
        newDataArray = DataArray()
        for i in range(self.bathyData.size()):
            data = self.bathyData.at(i)
            if self.compareTime(data.Time, self.timeEdit_BathyStartTime.text()) == ">" and self.compareTime(data.Time,
                                                                                                          self.timeEdit_BathyEndTime.text()) == "<":
                newDataArray.append(data)
        self.printLeft(newDataArray)
        self.postBathyData=newDataArray
        try:
            self.bathyReferenceList = self.bathyData.checkAllStatics(parametersList=self.bathyParameterList)
            self.comboBox_BathyReferencePoint.clear()
            for i in self.bathyReferenceList:
                self.comboBox_BathyReferencePoint.addItem(str(self.postBathyData.at(i)))
        except TypeError:
            print("There is no bathy data")
    def changeGpsTime(self):
        newDataArray=DataArray()
        for i in range(self.gpsData.size()):
            data=self.gpsData.at(i)
            if self.compareTime(data.Time,self.timeEdit_GpsStartTime.text())==">" and self.compareTime(data.Time,self.timeEdit_GpsEndTime.text())=="<":
                newDataArray.append(data)
        self.printRight(newDataArray)
        self.postGpsData=newDataArray
        try:
            self.gpsReferenceList = self.postGpsData.checkAllStatics(parametersList=self.gpsParameterList)
            self.comboBox_GpsReferencePoint.clear()
            for i in self.gpsReferenceList:
                self.comboBox_GpsReferencePoint.addItem(str(self.postGpsData.at(i)))
        except TypeError:
            print("There is no Gps Data")
    def compareTime(self,time1,time2,spliter1=':',spliter2=':'):
        t1=time1.split(spliter1)
        t2=time2.split(spliter2)
        h1 = float(t1[0])
        h2 = float(t2[0])
        m1 = float(t1[1])
        m2 = float(t2[1])
        try:
            s1 = float(t1[2])+m1*60+h1*60*60
            s2 = float(t2[2])+m2*60+h2*60*60
        except IndexError:
            s1 =  m1 * 60 + h1 * 60 * 60
            s2 =  m2 * 60 + h2 * 60 * 60
        if s1>s2:
            return ">"
        elif s1==s2:
            return "="
        else:
            return "<"
    def matchBathyGps(self):
        try:
            bathyIndex=self.bathyReferenceList[self.comboBox_BathyReferencePoint.currentIndex()]
            gpsIndex=self.gpsReferenceList[self.comboBox_GpsReferencePoint.currentIndex()]
            newArray=linkDataArray(self.postBathyData,bathyIndex,self.postGpsData,gpsIndex,self.Hdiff)
            self.plainTextEdit_MatchResult.setPlainText(str(newArray))
        except IndexError:
            print("could not find reference point")
    def updateParameterList(self):
        self.bathyParameterList=[]
        self.gpsParameterList=[]
        if self.checkBox_BathyA.isChecked():
            self.bathyParameterList.append("A")
        if self.checkBox_BathyDepth.isChecked():
            self.bathyParameterList.append("Depth")
        if self.checkBox_BathyE.isChecked():
            self.bathyParameterList.append("E")
        if self.checkBox_BathyN.isChecked():
            self.bathyParameterList.append("N")
        if self.checkBox_BathyS.isChecked():
            self.bathyParameterList.append("S")
        if self.checkBox_BathyW.isChecked():
            self.bathyParameterList.append("W")
        if self.checkBox_GpsE.isChecked():
            self.gpsParameterList.append("E")
        if self.checkBox_GpsElev.isChecked():
            self.gpsParameterList.append("Elev")
        if self.checkBox_GpsN.isChecked():
            self.gpsParameterList.append("N")
        if self.checkBox_GpsS.isChecked():
            self.gpsParameterList.append("S")
        if self.checkBox_GpsW.isChecked():
            self.gpsParameterList.append("W")
if __name__=='__main__':
    app=QApplication(sys.argv)
    form=mainwindow()
    form.show()
    app.exec_()