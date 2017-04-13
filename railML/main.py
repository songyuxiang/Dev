from PyQt5.Qt import *
import sys
from syx import *
import mainwindow
class mainwindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.database = []
        self.initUI()

    def initUI(self):
        self.database.append(self.formatData(n1="railml",att="version",value="2.3"))
        self.database.append(self.formatData(n1="railml",n2="infrastructure", att="version", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="id", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="code", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="name", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="description", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="xml:lang", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="xml:base", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="timetableRef", value="2.3"))
        self.database.append(self.formatData(n1="railml", n2="infrastructure", att="rollingstockRef", value="2.3"))

        print("init")
    def formatData(self, n1="", n2="", n3="", n4="", n5="", n6="", n7="", n8="",n9="",n10="",n11="", att="", value=""):
        out = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|" % ( n1, n2, n3, n4, n5, n6, n7, n8,n9,n10,n11, att, value)
        return out
    def saveFile(self):
        filename,_=QFileDialog.getSaveFileName()
        file=QFile(filename)
        if file.open(QFile.WriteOnly):
            out = QTextStream(file)
            for i in self.database:
                out<<i<<"\n"
            file.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = mainwindow()
    form.show()
    app.exec_()