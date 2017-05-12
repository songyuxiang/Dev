from PyQt5.QtChart import *
from PyQt5.Qt import *

import numpy as np


def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline
def yuxiangGeneratePieSerial(dataList,nameList,isLabelVisible=False):
    size=len(dataList)
    serial=QPieSeries()
    for i in range(size):
        try:
            pieSlice=QPieSlice(nameList[i],dataList[i])
            pieSlice.setLabelVisible(isLabelVisible)
            serial<<pieSlice
        except IndexError:
            pieSlice=QPieSlice("",dataList[i])
            serial << pieSlice
        except TypeError:
            pieSlice=QPieSlice("",0)
            serial << pieSlice
    return serial
def yuxiangGerenateLineSerial(x,y):
    serial=QLineSeries()
    try:
        serial.append(series_to_polyline(x,y))
    except:
        print("data not match")
    return serial
class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent=parent)
        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        # serial=yuxiangGeneratePieSerial([1,2,3,4],["1","2","3","4"])
        serial=yuxiangGerenateLineSerial([1,2,3,4,5,6,7],[2,3,1,3,4,5,6])
        self.chart.addSeries(serial)
        self.chart.legend().show()
    def set_title(self, title):
        self.chart.setTitle(title)




if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    app = QApplication(sys.argv)

    window = TestWindow()

    npoints = 1000000
    xdata = np.linspace(0., 10., npoints)

    window.set_title("test")
    window.setWindowTitle("Simple performance example")
    window.show()
    window.resize(500, 400)

    sys.exit(app.exec_())