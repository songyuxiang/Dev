import os

def calcul_gps(source,e_calculee,n_calculee,el_calculee):

    rawfile = open(source, 'r')
    destination = source[:-4]
    destination += str("_calc.txt")
    #print(destination)
    fichier = open(destination, "w")
    table = [line.rstrip().split() for line in rawfile.readlines()]
    #print (table)

# PERMET DE CREER UNE LISTE DES LIGNES OU APPARAIT LA CHAINE DE CARACTERE SOUHAITEE /////////////////////////////////////////////////////////////////////////////
    def trouver_base(table, chaine):
        liste_base=[]
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
    def point_intervalle (liste1, liste2):
        liste3= liste1+liste2
        liste4 = sorted(liste3)
        liste5=[]
        for element1 in liste1:
            for element4 in liste4:
                if element1==element4:
                    liste5.append(liste4.index(element4))
        liste_final=[]
        for element in liste5:
            intervalle = [liste4[element],liste4[element+1]]
            liste_final.append(intervalle)
        return liste_final

# ETAPE FINALE PERMET DE SORTIR LES LIGNES DES INTERVALLES DEPUIS LA TABLE BRUTE ///////////////////////////////////////////////////////////////////////////////////
    def liste_final(table_brute, table_interval):
        table_finale1=[]
        table_finale2 = []
        for element in table_interval:
            table_finale1.append(isoler_coord(table_brute[element[1]]))
        if len(table_finale1)==1:
            table_finale2=table_finale1[0]
            return table_finale2
        else:
            return table_finale1


# LISTING DE TOUS LES POINTS DEPUIS UNE LISTE DE LIGNE ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def calcul_all_pts(table,ligne_pts):
        liste_finale=[]
        for ligne in table:
            for element in ligne_pts:
                if table.index(ligne)==element:
                    liste_finale.append(isoler_coord(ligne))
        return liste_finale

# SORTIR TERIA ET BASE DE LA LISTE TOTALE POUR AVOIR LES PTS APPROCHES ///////////////////////////////////////////////////////////////////////////////////////////
    def isoler_ligne_pts_approche(table,intervalle_base,intervalle_teria):
        table_calc=table
        print (intervalle_base)
        print(intervalle_teria)
        for element1 in intervalle_base:
            for element in table_calc:
                if element==element1[1]:
                    table_calc.remove(element)
        for element2 in intervalle_teria:
            for element in table_calc:
                if element==element2[1]:
                    table_calc.remove(element)
        return table_calc

# /////////// Fonction qui donne le listing final des points recalcules /////////////////////////
    def pts_calculee(table, delta_est, delta_nord, delta_el):
        final_table = []
        for element in table:
            final_table.append([element[0], float(element[2]) + delta_est, float(element[1]) + delta_nord,
                                float(element[3]) + delta_el, element[4]])
        return final_table



    #print(trouver_base(table, "Base"))
    #print (trouver_type_point(table,"Satel","Method:"))
    #print(trouver_type_point(table, "GSM", "Method:"))
    #print(trouver_ligne_coord(table))
    ligne_base = trouver_base(table, "Base")
    ligne_GSM = trouver_type_point(table, "GSM", "Method:")
    ligne_Satel = trouver_type_point(table,"Satel","Method:")
    ligne_point = trouver_ligne_coord(table)

    intervalle_base = point_intervalle(ligne_base,ligne_point)
    intervalle_GSM = point_intervalle(ligne_GSM,ligne_point)
    #print(point_intervalle(ligne_base,ligne_point))
    #print(point_intervalle(ligne_GSM,ligne_point))
    pt_base=(liste_final(table,intervalle_base))
    pt_teria=(liste_final(table, intervalle_GSM))
    #print (pt_base)
    #print (pt_teria)

    ligne_pt_approche = isoler_ligne_pts_approche(ligne_point,intervalle_base,intervalle_GSM)
    pt_approche=calcul_all_pts(table,ligne_pt_approche)
    #print(pt_approche)

    #print(pt_base[1])
    #print(pt_base[2])
    #print(pt_base[3])

    delta_est = float(e_calculee) - float(pt_base[1])
    delta_nord = float(n_calculee) - float(pt_base[2])
    delta_el = float(el_calculee) - float(pt_base[3])

    fichier.write("///////// Coordonnees de la base approchee /////////\n")
    fichier.write(
                "Id: " + str(pt_base[0]) + " Est: " + str(pt_base[1]) + " Nord: " + str(pt_base[2]) + " Elevation: " + str(
                    pt_base[3]) + " Code: " + str(pt_base[4]))
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
    fichier.write("  ".join(str(pts) for pts in pt_teria))
    fichier.write("\n")
    fichier.write("\n///////// Points Calcules /////////")
    pts_recalculee = pts_calculee(pt_approche, delta_est, delta_nord, delta_el)
    for ligne in pts_recalculee:
            fichier.write("\n{} {} {} {} {}".format(ligne[0], round(ligne[1],4), round(ligne[2],4), round(ligne[3],4), ligne[4]))

    fichier.close()

if __name__ == "__main__":
    calcul_gps("20170330lussan.rw5","5202243","1403625","22")
