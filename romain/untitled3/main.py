from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import sys
import os



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(517, 423)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit_X = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_X.setGeometry(QtCore.QRect(40, 120, 133, 20))
        self.lineEdit_X.setText("")
        self.lineEdit_X.setObjectName("lineEdit_X")
        self.titre_Y_calc = QtWidgets.QLabel(self.centralWidget)
        self.titre_Y_calc.setGeometry(QtCore.QRect(190, 120, 16, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Y_calc.sizePolicy().hasHeightForWidth())
        self.titre_Y_calc.setSizePolicy(sizePolicy)
        self.titre_Y_calc.setLineWidth(1)
        self.titre_Y_calc.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Y_calc.setObjectName("titre_Y_calc")
        self.lineEdit_Y = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_Y.setGeometry(QtCore.QRect(210, 120, 133, 20))
        self.lineEdit_Y.setObjectName("lineEdit_Y")
        self.lineEdit_Z = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_Z.setGeometry(QtCore.QRect(380, 120, 133, 20))
        self.lineEdit_Z.setObjectName("lineEdit_Z")
        self.coord_base = QtWidgets.QLabel(self.centralWidget)
        self.coord_base.setGeometry(QtCore.QRect(170, 90, 157, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coord_base.sizePolicy().hasHeightForWidth())
        self.coord_base.setSizePolicy(sizePolicy)
        self.coord_base.setLineWidth(1)
        self.coord_base.setAlignment(QtCore.Qt.AlignCenter)
        self.coord_base.setObjectName("coord_base")
        self.Calculer = QtWidgets.QPushButton(self.centralWidget)
        self.Calculer.setGeometry(QtCore.QRect(40, 310, 201, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calculer.sizePolicy().hasHeightForWidth())
        self.Calculer.setSizePolicy(sizePolicy)
        self.Calculer.setObjectName("Calculer")
        self.titre_X_calc = QtWidgets.QLabel(self.centralWidget)
        self.titre_X_calc.setGeometry(QtCore.QRect(20, 120, 16, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_X_calc.sizePolicy().hasHeightForWidth())
        self.titre_X_calc.setSizePolicy(sizePolicy)
        self.titre_X_calc.setLineWidth(1)
        self.titre_X_calc.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_X_calc.setObjectName("titre_X_calc")
        self.titre = QtWidgets.QLabel(self.centralWidget)
        self.titre.setGeometry(QtCore.QRect(9, 9, 500, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.titre.setFont(font)
        self.titre.setAlignment(QtCore.Qt.AlignCenter)
        self.titre.setObjectName("titre")
        self.Photo = QtWidgets.QLabel(self.centralWidget)
        self.Photo.setGeometry(QtCore.QRect(270, 310, 200, 48))
        self.Photo.setText("")
        self.Photo.setPixmap(QtGui.QPixmap("G:/geosat.gif"))
        self.Photo.setObjectName("Photo")
        self.Parcourir1 = QtWidgets.QPushButton(self.centralWidget)
        self.Parcourir1.setGeometry(QtCore.QRect(260, 50, 131, 21))
        self.Parcourir1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Parcourir1.setObjectName("Parcourir1")
        self.entree = QtWidgets.QLabel(self.centralWidget)
        self.entree.setGeometry(QtCore.QRect(130, 50, 91, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entree.sizePolicy().hasHeightForWidth())
        self.entree.setSizePolicy(sizePolicy)
        self.entree.setAlignment(QtCore.Qt.AlignCenter)
        self.entree.setObjectName("entree")
        self.titre_Z_calc = QtWidgets.QLabel(self.centralWidget)
        self.titre_Z_calc.setGeometry(QtCore.QRect(360, 120, 16, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Z_calc.sizePolicy().hasHeightForWidth())
        self.titre_Z_calc.setSizePolicy(sizePolicy)
        self.titre_Z_calc.setLineWidth(1)
        self.titre_Z_calc.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Z_calc.setObjectName("titre_Z_calc")
        self.X_approch = QtWidgets.QLabel(self.centralWidget)
        self.X_approch.setGeometry(QtCore.QRect(40, 180, 121, 21))
        self.X_approch.setText("")
        self.X_approch.setObjectName("X_approch")
        self.Y_approch = QtWidgets.QLabel(self.centralWidget)
        self.Y_approch.setGeometry(QtCore.QRect(220, 180, 121, 21))
        self.Y_approch.setText("")
        self.Y_approch.setObjectName("Y_approch")
        self.Z_approch = QtWidgets.QLabel(self.centralWidget)
        self.Z_approch.setGeometry(QtCore.QRect(390, 180, 121, 21))
        self.Z_approch.setText("")
        self.Z_approch.setObjectName("Z_approch")
        self.coord_base_2 = QtWidgets.QLabel(self.centralWidget)
        self.coord_base_2.setGeometry(QtCore.QRect(160, 160, 191, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coord_base_2.sizePolicy().hasHeightForWidth())
        self.coord_base_2.setSizePolicy(sizePolicy)
        self.coord_base_2.setLineWidth(1)
        self.coord_base_2.setAlignment(QtCore.Qt.AlignCenter)
        self.coord_base_2.setObjectName("coord_base_2")
        self.titre_X_approch = QtWidgets.QLabel(self.centralWidget)
        self.titre_X_approch.setGeometry(QtCore.QRect(20, 180, 16, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_X_approch.sizePolicy().hasHeightForWidth())
        self.titre_X_approch.setSizePolicy(sizePolicy)
        self.titre_X_approch.setLineWidth(1)
        self.titre_X_approch.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_X_approch.setObjectName("titre_X_approch")
        self.titre_Y_approch = QtWidgets.QLabel(self.centralWidget)
        self.titre_Y_approch.setGeometry(QtCore.QRect(190, 180, 16, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Y_approch.sizePolicy().hasHeightForWidth())
        self.titre_Y_approch.setSizePolicy(sizePolicy)
        self.titre_Y_approch.setLineWidth(1)
        self.titre_Y_approch.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Y_approch.setObjectName("titre_Y_approch")
        self.titre_Z_approch = QtWidgets.QLabel(self.centralWidget)
        self.titre_Z_approch.setGeometry(QtCore.QRect(355, 180, 21, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Z_approch.sizePolicy().hasHeightForWidth())
        self.titre_Z_approch.setSizePolicy(sizePolicy)
        self.titre_Z_approch.setLineWidth(1)
        self.titre_Z_approch.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Z_approch.setObjectName("titre_Z_approch")
        self.coord_base_3 = QtWidgets.QLabel(self.centralWidget)
        self.coord_base_3.setGeometry(QtCore.QRect(160, 220, 191, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coord_base_3.sizePolicy().hasHeightForWidth())
        self.coord_base_3.setSizePolicy(sizePolicy)
        self.coord_base_3.setLineWidth(1)
        self.coord_base_3.setAlignment(QtCore.Qt.AlignCenter)
        self.coord_base_3.setObjectName("coord_base_3")
        self.titre_Delta_Y = QtWidgets.QLabel(self.centralWidget)
        self.titre_Delta_Y.setGeometry(QtCore.QRect(155, 240, 51, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Delta_Y.sizePolicy().hasHeightForWidth())
        self.titre_Delta_Y.setSizePolicy(sizePolicy)
        self.titre_Delta_Y.setLineWidth(1)
        self.titre_Delta_Y.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Delta_Y.setObjectName("titre_Delta_Y")
        self.Delta_X = QtWidgets.QLabel(self.centralWidget)
        self.Delta_X.setGeometry(QtCore.QRect(60, 240, 91, 21))
        self.Delta_X.setText("")
        self.Delta_X.setObjectName("Delta_X")
        self.titre_Delta_Z = QtWidgets.QLabel(self.centralWidget)
        self.titre_Delta_Z.setGeometry(QtCore.QRect(335, 240, 41, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Delta_Z.sizePolicy().hasHeightForWidth())
        self.titre_Delta_Z.setSizePolicy(sizePolicy)
        self.titre_Delta_Z.setLineWidth(1)
        self.titre_Delta_Z.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Delta_Z.setObjectName("titre_Delta_Z")
        self.Delta_Y = QtWidgets.QLabel(self.centralWidget)
        self.Delta_Y.setGeometry(QtCore.QRect(220, 240, 111, 21))
        self.Delta_Y.setText("")
        self.Delta_Y.setObjectName("Delta_Y")
        self.titre_Delta_X = QtWidgets.QLabel(self.centralWidget)
        self.titre_Delta_X.setGeometry(QtCore.QRect(10, 240, 41, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titre_Delta_X.sizePolicy().hasHeightForWidth())
        self.titre_Delta_X.setSizePolicy(sizePolicy)
        self.titre_Delta_X.setLineWidth(1)
        self.titre_Delta_X.setAlignment(QtCore.Qt.AlignCenter)
        self.titre_Delta_X.setObjectName("titre_Delta_X")
        self.Delta_Z = QtWidgets.QLabel(self.centralWidget)
        self.Delta_Z.setGeometry(QtCore.QRect(390, 240, 121, 21))
        self.Delta_Z.setText("")
        self.Delta_Z.setObjectName("Delta_Z")
        self.entree.raise_()
        self.lineEdit_X.raise_()
        self.titre_Y_calc.raise_()
        self.lineEdit_Y.raise_()
        self.lineEdit_Z.raise_()
        self.coord_base.raise_()
        self.Calculer.raise_()
        self.titre_X_calc.raise_()
        self.titre.raise_()
        self.Photo.raise_()
        self.Parcourir1.raise_()
        self.titre_Z_calc.raise_()
        self.X_approch.raise_()
        self.Y_approch.raise_()
        self.Z_approch.raise_()
        self.coord_base_2.raise_()
        self.titre_X_approch.raise_()
        self.titre_Y_approch.raise_()
        self.titre_Z_approch.raise_()
        self.coord_base_3.raise_()
        self.titre_Delta_Y.raise_()
        self.Delta_X.raise_()
        self.titre_Delta_Z.raise_()
        self.Delta_Y.raise_()
        self.titre_Delta_X.raise_()
        self.Delta_Z.raise_()
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 517, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titre_Y_calc.setText(_translate("MainWindow", "Y:"))
        self.coord_base.setText(_translate("MainWindow", "Coordonnées de la base calculée"))
        self.Calculer.setText(_translate("MainWindow", "Calculer"))
        self.titre_X_calc.setText(_translate("MainWindow", "X:"))
        self.titre.setText(_translate("MainWindow", "Programme permettant de transformer un fichier \".rw5\" en un fichier de points colonné"))
        self.Parcourir1.setText(_translate("MainWindow", "Parcourir..."))
        self.entree.setText(_translate("MainWindow", "Fichier en entrée:"))
        self.titre_Z_calc.setText(_translate("MainWindow", "Z:"))
        self.coord_base_2.setText(_translate("MainWindow", "Coordonnées de la base approchée:"))
        self.titre_X_approch.setText(_translate("MainWindow", "X:"))
        self.titre_Y_approch.setText(_translate("MainWindow", "Y:"))
        self.titre_Z_approch.setText(_translate("MainWindow", "Z:"))
        self.coord_base_3.setText(_translate("MainWindow", "Delta entre les bases:"))
        self.titre_Delta_Y.setText(_translate("MainWindow", "Delta_Y:"))
        self.titre_Delta_Z.setText(_translate("MainWindow", "Delta_Z:"))
        self.titre_Delta_X.setText(_translate("MainWindow", "Delta_X:"))

class mainwindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Parcourir1.clicked.connect(self.openfile)
        self.Calculer.clicked.connect(self.calculate)

    def calcul_gps(self,source, e_calculee, n_calculee, el_calculee):

        rawfile = open(source, 'r')
        destination = source[:-4]
        destination += str("_calc.txt")
        # print(destination)
        fichier = open(destination, "w")
        table = [line.rstrip().split() for line in rawfile.readlines()]

        # print (table)

        # PERMET DE CREER UNE LISTE DES LIGNES OU APPARAIT LA CHAINE DE CARACTERE SOUHAITEE /////////////////////////////////////////////////////////////////////////////
        def trouver_base(table, chaine):
            liste_base = []
            for ligne in table:
                for element in ligne:
                    if element == chaine:
                        liste_base.append(table.index(ligne))
            return liste_base

            # PERMET DE CREER UNE LISTE DES LIGNES OU APPARAIT LA CHAINE DE CARACTERE DES POINTS /////////////////////////////////////////////////////////////////////////////

        def trouver_ligne_coord(table):
            liste_point = []
            for ligne in table:
                for element in ligne:
                    if element[0:4] == "--GS":
                        liste_point.append(table.index(ligne))
            return liste_point

            # PERMET DE CREER UNE LISTE DES LIGNES OU APPARAIT DEUX CHAINES DE CARACTERE /////////////////////////////////////////////////////////////////////////////

        def trouver_type_point(table, chaine1, chaine2):
            liste_base = []
            for ligne in table:
                if chaine1 in ligne:
                    if chaine2 in ligne:
                        liste_base.append(table.index(ligne))
            return liste_base

            # PERMET DE CREER UNE LISTE DES LIGNES OU APPARAIT DEUX CHAINES DE CARACTERE /////////////////////////////////////////////////////////////////////////////

        def isoler_coord(ligne):
            id_brut = ligne[0]
            id_nettoye = id_brut[7:-2]
            nord_brut = ligne[1]
            nord_nettoye = nord_brut[:12]
            est_brut = ligne[2]
            est_nettoye = est_brut[:12]
            el_nettoye = est_brut[15:22]
            code_nettoye = est_brut[25:]
            return [id_nettoye, est_nettoye, nord_nettoye, el_nettoye, code_nettoye]

            # PERMET DE CREER UNE LISTE D'INTERVALLES ENTRE LES ELEMENTS D'UNE LISTE ET CELUI DIRECTEMENT SUPERIEUR D'UNE AUTRE ///////////////////////////////////////////////////

        def point_intervalle(liste1, liste2):
            liste3 = liste1 + liste2
            liste4 = sorted(liste3)
            liste5 = []
            for element1 in liste1:
                for element4 in liste4:
                    if element1 == element4:
                        liste5.append(liste4.index(element4))
            liste_final = []
            for element in liste5:
                intervalle = [liste4[element], liste4[element + 1]]
                liste_final.append(intervalle)
            return liste_final

            # ETAPE FINALE PERMET DE SORTIR LES LIGNES DES INTERVALLES DEPUIS LA TABLE BRUTE ///////////////////////////////////////////////////////////////////////////////////

        def liste_final(table_brute, table_interval):
            table_finale1 = []
            table_finale2 = []
            for element in table_interval:
                table_finale1.append(isoler_coord(table_brute[element[1]]))
            if len(table_finale1) == 1:
                table_finale2 = table_finale1[0]
                return table_finale2
            else:
                return table_finale1


                # LISTING DE TOUS LES POINTS DEPUIS UNE LISTE DE LIGNE ////////////////////////////////////////////////////////////////////////////////////////////////////////////

        def calcul_all_pts(table, ligne_pts):
            liste_finale = []
            for ligne in table:
                for element in ligne_pts:
                    if table.index(ligne) == element:
                        liste_finale.append(isoler_coord(ligne))
            return liste_finale

            # SORTIR TERIA ET BASE DE LA LISTE TOTALE POUR AVOIR LES PTS APPROCHES ///////////////////////////////////////////////////////////////////////////////////////////

        def isoler_ligne_pts_approche(table, intervalle_base, intervalle_teria):
            table_calc = table
            print(intervalle_base)
            print(intervalle_teria)
            for element1 in intervalle_base:
                for element in table_calc:
                    if element == element1[1]:
                        table_calc.remove(element)
            for element2 in intervalle_teria:
                for element in table_calc:
                    if element == element2[1]:
                        table_calc.remove(element)
            return table_calc

            # /////////// Fonction qui donne le listing final des points recalcules /////////////////////////

        def pts_calculee(table, delta_est, delta_nord, delta_el):
            final_table = []
            for element in table:
                final_table.append([element[0], float(element[2]) + delta_est, float(element[1]) + delta_nord,
                                    float(element[3]) + delta_el, element[4]])
            return final_table

        # print(trouver_base(table, "Base"))
        # print (trouver_type_point(table,"Satel","Method:"))
        # print(trouver_type_point(table, "GSM", "Method:"))
        # print(trouver_ligne_coord(table))
        ligne_base = trouver_base(table, "Base")
        ligne_GSM = trouver_type_point(table, "GSM", "Method:")
        ligne_Satel = trouver_type_point(table, "Satel", "Method:")
        ligne_point = trouver_ligne_coord(table)

        intervalle_base = point_intervalle(ligne_base, ligne_point)
        intervalle_GSM = point_intervalle(ligne_GSM, ligne_point)
        # print(point_intervalle(ligne_base,ligne_point))
        # print(point_intervalle(ligne_GSM,ligne_point))
        pt_base = (liste_final(table, intervalle_base))
        pt_teria = (liste_final(table, intervalle_GSM))
        # print (pt_base)
        # print (pt_teria)

        ligne_pt_approche = isoler_ligne_pts_approche(ligne_point, intervalle_base, intervalle_GSM)
        pt_approche = calcul_all_pts(table, ligne_pt_approche)
        # print(pt_approche)

        # print(pt_base[1])
        # print(pt_base[2])
        # print(pt_base[3])

        delta_est = float(e_calculee) - float(pt_base[1])
        delta_nord = float(n_calculee) - float(pt_base[2])
        delta_el = float(el_calculee) - float(pt_base[3])

        self.titre_Delta_X.setText(str(delta_est))


        fichier.write("///////// Coordonnees de la base approchee /////////\n")
        fichier.write(
            "Id: " + str(pt_base[0]) + " Est: " + str(pt_base[1]) + " Nord: " + str(pt_base[2]) + " Elevation: " + str(
                pt_base[3]) + " Code: " + str(pt_base[4]))
        fichier.write("\n")
        fichier.write("\n")
        fichier.write("///////// Coordonnees de la base calculee /////////\n")
        fichier.write(
            "Coordonees de la base calculee: E: {} N: {} Elevation: {}".format(e_calculee, n_calculee, el_calculee))
        fichier.write("\n")
        fichier.write("\n")
        fichier.write("///////// Delta = Base calculee - Base approchee /////////\n")
        fichier.write("Delta E: {} Delta N: {} Delta Elevation: {}".format(delta_est, delta_nord, delta_el))

        fichier.write("\n")
        fichier.write("\n")
        fichier.write("///////// Points Teria /////////\n")
        fichier.write("  ".join(str(pts) for pts in pt_teria))
        fichier.write("\n")
        fichier.write("\n///////// Points Calcules /////////")
        pts_recalculee = pts_calculee(pt_approche, delta_est, delta_nord, delta_el)
        for ligne in pts_recalculee:
            fichier.write(
                "\n{} {} {} {} {}".format(ligne[0], round(ligne[1], 4), round(ligne[2], 4), round(ligne[3], 4),
                                          ligne[4]))

        fichier.close()
    def openfile(self):
        filename = QFileDialog.getOpenFileName()
        isole_source = filename[0]
        source_sep = isole_source.split("/")
        self.source = source_sep[-1:]
        path = "/".join(source_sep[:-1])
        print(path)
        print(type(self.source[0]))
        sys.path.append(path)
        print(os.getcwd())
        print(filename)

    def calculate(self):
        e_calculee = self.lineEdit_X.text()
        n_calculee = self.lineEdit_Y.text()
        el_calculee = self.lineEdit_Z.text()
        self.calcul_gps(self.source[0],e_calculee,n_calculee,el_calculee)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = mainwindow()
    form.show()
    sys.exit(app.exec_())