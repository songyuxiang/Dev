from PyQt5.Qt import *
import sys
import mainwindow
class mainwindow(QMainWindow,mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)
        self.Parcourir1.clicked.connect(self.openfile)
        self.Calculer.clicked.connect(self.calculate)
    def openfile(self):
        file,_=QFileDialog.getOpenFileName()
        print(file)
    def calculate(self):
        print("calculate")
def calcul_gps(source,e_calculee,n_calculee,el_calculee):
    # source = "20170330lussan.rw5"
    # destination = "resultat.txt"

    rawfile = open(source, 'r')
    destination = source[:-4]
    destination += str("_calc.txt")
    print(destination)
    fichier = open(destination, "w")
    table = [line.rstrip().split() for line in rawfile.readlines()]

    k = ligne_2info(table, "Method:", "GSM")
    table_GSM = table[k:base_ligne(table)]

    l = ligne_2info(table, "Method:", "Satel")
    table_Satel = table[l:]

    table_clean = table[base_ligne(table):l]
    pts_base = trouver_ligne_coord(table_clean)


    print( "///////// Info des coordonnees de la base approchee /////////")
    print ("Id: " + str(pts_base[0]) + " Est: " + str(pts_base[1]) + " Nord: " + str(pts_base[2]) + " Elevation: " + str(
        pts_base[3]) + " Code: " + str(pts_base[4]))

    print ("///////// Info des coordonnees de la base calculee /////////")
    print ("Coordonees de la base calculee: E:" + str(e_calculee) + " N: " + str(n_calculee) + " Elevation: " + str(
        el_calculee))


    delta_est = float(e_calculee) - float(pts_base[1])
    delta_nord = float(n_calculee) - float(pts_base[2])
    delta_el = float(el_calculee) - float(pts_base[3])

    print ("///////// Delta = Base calculee - Base approchee /////////")
    print ("Delta E:" + str(delta_est) + " Delta N: " + str(delta_nord) + " Delta Elevation: " + str(delta_el))

    print ("Est-ce que le donnees sont correctes ? (o/n)")

    #print ("///////// Points Teria /////////")
    pts_teria = trouver_ligne_coord(table_GSM)
    #print pts_teria

    #print ('///////// Points Approches /////////')
    pts_approche = trouver_ligne_coord(table_Satel)

    #print ("///////// Points Calcules /////////")
    #print pts_calculee(pts_approche, delta_est, delta_nord, delta_el)

    # ///////// Ecriture du fichier texte ///////////////////////////////////////////////////////////////

    fichier.write("///////// Coordonnees de la base approchee /////////\n")
    fichier.write(
                "Id: " + str(pts_base[0]) + " Est: " + str(pts_base[1]) + " Nord: " + str(pts_base[2]) + " Elevation: " + str(
                    pts_base[3]) + " Code: " + str(pts_base[4]))
    fichier.write("\n")
    fichier.write("\n")
    fichier.write("///////// Coordonnees de la base calculee /////////\n")
    fichier.write("Coordonees de la base calculee: E: {} N: {} Elevation: {}".format(e_calculee, n_calculee, el_calculee))
    fichier.write("\n")
    fichier.write("\n")
    fichier.write("///////// Delta = Base calculee - Base approchee /////////\n")
    fichier.write("Delta E: {} Delta N: {} Delta Elevation: {}".format(delta_est, delta_nord, delta_el))

    fichier.write("\n")
    fichier.write("\n")
    fichier.write("///////// Points Teria /////////\n")
    fichier.write("  ".join(str(pts) for pts in pts_teria))
    fichier.write("\n")
    fichier.write("\n///////// Points Calcules /////////")
    pts_recalculee = pts_calculee(pts_approche, delta_est, delta_nord, delta_el)
    for ligne in pts_recalculee:
            fichier.write("\n{} {} {} {} {}".format(ligne[0], round(ligne[1],4), round(ligne[2],4), round(ligne[3],4), ligne[4]))

    fichier.close()


    # dest_r=open(destination,"r")
    # dest_w=open("resultat2.txt","w")
    # for line in dest_r:
    #     line = line.replace("'", "").replace("(","").replace(")","").replace("[","").replace("]","")
    #     dest_w.write(line)


    # fichier.close()


# /////////// Determination du numero de la ligne contenant "Base" //////////////////////////////////////////////
def base_ligne(table):
    i = 0
    for ligne in table:
        if not "Base" in ligne:
            i += 1
        else:
            break
    return i


# Determination du numero de la ligne contenant deux caracteres /////////////////////////////////////
def ligne_2info(table, info1, info2):
    k = 0
    for ligne in table:
        if not (info1 and info2) in ligne:
            # if not info2 in ligne:
            k += 1
        else:
            break
    return k


# ///// Fonction qui isole les differentes infos pour chaque point sur une ligne ///////////////
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


# //////// Fonction qui rassemble tous les points d'une table ////////////////////////////////////////
def trouver_ligne_coord(table):
    # ligne_coord=[]
    point = []
    for ligne in table:
        for element in ligne:
            # print element[0:4]
            if element[0:4] == "--GS":
                # ligne_coord+=ligne
                point.append(isoler_coord(ligne))
    if len(point) == 1:
        return point[0]
    else:
        return point  # ,ligne_coord

# /////////// Fonction qui donne le listing final des points recalcules /////////////////////////
def pts_calculee(table, delta_est, delta_nord, delta_el):
    final_table = []
    for element in table:
        final_table.append([element[0], float(element[2]) + delta_est, float(element[1]) + delta_nord,
                        float(element[3]) + delta_el, element[4]])
    return final_table

# ///// Fin des fonctions//////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////DEBUT DU PROGRAMME ///////////////////////////////////////////////////////////////////////////////////////

# ////////// Calcul des tables /////////////////////////////////////////////////////////////////////


if __name__ == "__main__":

    app = QApplication(sys.argv)
    form=mainwindow()
    form.show()
    sys.exit(app.exec_())