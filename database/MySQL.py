from PyQt5.QtChart import *
from PyQt5.Qt import *

import numpy as np
from PyQt5.QtChart import QChart

class LineSeriesData():
    def __init__(self,name="",xList=[],yList=[]):
        self.name=name
        self.x=xList
        self.y=yList
        if len(self.x)!=len(self.y):
            print("can't initialize data")
            self.x=[]
            self.y=[]
            self.size=0
        else:
            self.size=len(self.x)
class PieSeriesData():
    def __init__(self,nameList=[],valueList=[]):
        self.names=nameList
        self.values=valueList
        if len(self.names)!=len(self.values):
            print("can't initialize data")
            self.names=[]
            self.values=[]
            self.size=0
        else:
            self.size=len(self.names)
class StackedBarSeriesData():
    def __init__(self,name="",valueList=[]):
        self.name=""
        self.values=valueList


def yuxiangGeneratePieChart(pieSeriesData,isLabelVisible=True,pieSize=1,hPos=0.5,vPos=0.5):
    chart=QChart()
    series=QPieSeries()
    for i in range(pieSeriesData.size):
        try:
            pieSlice=QPieSlice(pieSeriesData.names[i],pieSeriesData.values[i])
            pieSlice.setLabelVisible(isLabelVisible)
            series<<pieSlice
        except IndexError:
            pieSlice=QPieSlice("",pieSeriesData.values[i])
            series << pieSlice
        except TypeError:
            pieSlice=QPieSlice("",0)
            series << pieSlice
    series.setPieSize(pieSize)
    series.setHorizontalPosition(hPos)
    series.setVerticalPosition(vPos)
    chart.addSeries(series)
    chart.legend().show()
    return chart

def yuxiangGerenateLineChart(lineSeriesDataList):
    chart = QChart()
    for seriesData in lineSeriesDataList:
        series = QLineSeries()
        for i in range(seriesData.size):
            try:
                series << QPointF(float(seriesData.x[i]),float(seriesData.y[i]))

            except IndexError:
                print("index error")
            except TypeError:
                print("wrong input data type")
        series.setName(seriesData.name)
        chart.addSeries(series)
    chart.createDefaultAxes()
    chart.legend().show()
    return chart

def yuxiangString2MSecsSinceEpoch(string,spliter="-"):
    temp=string.split(spliter)
    datetime=QDateTime()
    datetime.setDate(QDate(int(temp[0]),int(temp[1]),int(temp[2])))
    out=datetime.toMSecsSinceEpoch()
    return out


def yuxiangGerenateDateTimeLineChart(lineSeriesDataList):
    chart = QChart()
    axisX = QDateTimeAxis()
    axisX.setFormat("dd-MMM-yyyy");
    axisX.setTitleText("Date");
    axisY = QValueAxis()
    chart.addAxis(axisX, Qt.AlignBottom)
    chart.addAxis(axisY, Qt.AlignLeft)
    yMin=0
    yMax=0
    for seriesData in lineSeriesDataList:
        series = QLineSeries()
        for i in range(seriesData.size):
            try:
                if float(seriesData.y[i])<yMin:
                    yMin=float(seriesData.y[i])
                if float(seriesData.y[i])>yMax:
                    yMax=float(seriesData.y[i])
                series.append(yuxiangString2MSecsSinceEpoch(seriesData.x[i]),float(seriesData.y[i]))

            except IndexError:
                print("index error")
            except TypeError:
                print("wrong input data type")
        series.setName(seriesData.name)

        chart.addSeries(series)
        series.attachAxis(axisX)
        series.attachAxis(axisY)
    axisY.setMax(yMax)
    axisY.setMin(yMin)
    chart.legend().show()
    return chart

def yuxiangGerenateSplineChart(lineSeriesDataList):
    chart = QChart()
    for seriesData in lineSeriesDataList:
        series = QSplineSeries()
        for i in range(seriesData.size):
            try:
                series << QPointF(float(seriesData.x[i]), float(seriesData.y[i]))

            except IndexError:
                print("index error")
            except TypeError:
                print("wrong input data type")
        series.setName(seriesData.name)
        chart.addSeries(series)
    chart.createDefaultAxes()
    chart.legend().show()
    return chart


def yuxiangGerenateHorizontalStackedBarChart(starcedBarSeriesDataList,categories=[]):
    chart = QChart()
    series = QHorizontalStackedBarSeries()

    for seriesData in starcedBarSeriesDataList:
        set=QBarSet(seriesData.name)
        for i in seriesData.values:
            set << float(i)
        series.append(set)
    axis=QBarCategoryAxis()
    axis.append(categories)
    chart.addSeries(series)
    chart.createDefaultAxes()
    chart.setAxisY(axis,series)
    chart.legend().show()
    return chart









class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        name=["test1","test2","test3","test4","test5","test6","test"]
        date=["2017-02-01","2017-02-02","2017-02-03","2017-02-04","2017-02-05","2017-02-06","2017-02-07"]
        print(yuxiangString2MSecsSinceEpoch("2017-02-01"))
        x=[1,2,3,4,5,6,7]
        y=[2,3,1,3,4,5,6]
        # self.pieChart=yuxiangGeneratePieChart(PieSeriesData(name,x))
        self.pieChart=yuxiangGerenateDateTimeLineChart([LineSeriesData("series1",date,y),LineSeriesData("series2",date,x)])
        # self.pieChart=yuxiangGerenateDateTimeLineChart([LineSeriesData("series1",date,x)])
        # axis=QDateTimeAxis()
        # axis.setTickCount(10)
        # axis.setFormat("dd-MM-yyyy")
        # axis.setTitleText("Date")
        # chartView=QChartView()
        # self.pieChart.addAxis(axis,Qt.AlignBottom)
        # 
        # chartView.setChart(self.pieChart)
        # self.setCentralWidget(chartView)

        chartView=QChartView(self.pieChart)
        self.setCentralWidget(chartView)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)

    window = TestWindow()

    npoints = 1000000
    xdata = np.linspace(0., 10., npoints)

    window.show()
    window.resize(500, 400)

    sys.exit(app.exec_())