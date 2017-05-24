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
        self.model=QStandardItemModel(1000,365)
        self.updateHeader()
    def updateHeader(self):
        dateList=[]
        dateStringList=[]
        for M in range(1,13):
            for d in range(1,32):
                date=QDateTime(QDate(2017,M,d))
                if date!=QDateTime(0,0,0,0,0):
                    dateList.append(date)
                    dateStringList.append(date.toString("dd-MMM-yyyy"))
        self.model.setHorizontalHeaderLabels(dateStringList)
        self.tableView.setModel(self.model)
        item=QItemDelegate(self)

    def setData(self):
        x=[[1,2,3,2,3,4]]
        self.model=yuxiangList2StandardModel(x)
        self.tableView.setModel(self.model)
    def contextMenuEvent(self, event):
        self.menu=QMenu(self)
        action=QAction("action name",self)
        self.menu.addAction(action)
        self.menu.popup(QCursor.pos())
        # action.triggered.connect(lambda: self.rename())
        action.triggered.connect(self.action)
    def action(self):
        index=self.tableView.currentIndex()
        print(self.model.data(index))


if __name__=='__main__':
    app=QApplication(sys.argv)
    form=window()
    form.show()
    app.exec_()
