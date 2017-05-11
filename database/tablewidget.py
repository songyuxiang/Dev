from PyQt5.Qt import *
import mainwindow
import sys

def yuxiangList2StandardModel(list):
    size1=len(list)
    try:
        size2=len(list[0])
    except:
        size2=None
    model=QStandardItemModel()
    if size1!=None and size2!=None:
        for i in range(size1):
            for j in range(size2):
                item=QStandardItem(str(list[i][j]))
                model.setItem(i,j,item)
    elif size1!=None and size2==None:
        for i in range(size1):
            item=QStandardItem(str(list[i]))
            model.setItem(0,i,item)

    return model

class window(QMainWindow,mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model=QStandardItemModel()
        self.setData()
    def setData(self):
        x=[[1,2,3,2,3,4]]
        self.model=yuxiangList2StandardModel(x)
        self.tableView.setModel(self.model)
if __name__=='__main__':
    app=QApplication(sys.argv)
    form=window()
    form.show()
    app.exec_()
