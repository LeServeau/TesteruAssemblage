"""
__author__ = "Alexandre HERVIEU"
__copyright__ = "Copyright 2021, Seribase Industrie"
__version__ = "1.0.1"
__email__ = "a.hervieu@seribase.fr"
__status__ = "Prototype"
"""

import mysql.connector
from mysql.connector import Error


class BddTesteur:

    def __init__(self, ip, nombdd):
        self.connect(ip, nombdd)

    # fonction qui ajoute une nouvelle référence à une base de donnée si elle n'existe pas déjà
    def new_product_LED(self, product, label, anode, cathode):
        # vérifie si la liste retournée est vide ou non, si comporte des caractère, le produit existe déjà donc on ajoute pas à la BDD
        if self.get_product(product):
            print("le produit existe déjà")
        else:
            try:
                #####POUR AJOUTER PRODUIT LEDS#####
                commande_sql = "INSERT INTO `produits` (`produits_id`, `produits_name`, `produits_label`, `produits_anode`, `produits_cathode`) VALUES ('', '" + \
                    product + "', '" + label + "', '" + anode + "', '" + cathode + "')"
                cursor.execute(commande_sql)
                # on ajoute le nouveau produit à la BDD
                print("Le produitLEDS est ajouté à la BDD")
            except Error as e:
                print("Error while connecting and inserting data to MySQL", e)

    def new_product_TOUCHES(self, product, label, res_max, res_min, p_A, p_B):
        # vérifie si la liste retournée est vide ou non, si comporte des caractère, le produit existe déjà donc on ajoute pas à la BDD
        if self.get_product(product):
            print("le produit existe déjà")
        else:
            try:
                #####POUR AJOUTER PRODUIT TOUCHES#####
                commande_sql = "INSERT INTO `produits` (`produits_id`, `produits_name`, `produits_label`, `produits_resMax`, `produits_resMin`, `PA`, `PB`) VALUES ('', '" + \
                    product + "', '" + label + "', '" + res_max + "', '" + \
                    res_min + "', '" + p_A + "', '" + p_B + "')"
                cursor.execute(commande_sql)
                # on ajoute le nouveau produit à la BDD
                print("Le produitTOUCHES est ajouté à la BDD")
            except Error as e:
                print("Error while connecting and inserting data to MySQL", e)

    def get_product(self, reaserch):
        try:
            commande_sql = "SELECT DISTINCT(produits_name) FROM `produits` WHERE (produits_name = \""+reaserch+"\")"
            cursor.execute(commande_sql)  # execute la commande SQL
            records = cursor.fetchall()  # Récupère la réponse de la BDD
            print(records)
            return records
        except Error as e:
            print("Error while retrieving data from MySQL", e)

    # permet d'ajouter une ligne à une table produit

    def ajouter_ligne_ref(self, table, ref, anode, cathode, disposition, Type, numled, numtest):
        try:
            sql = "INSERT INTO `"+table + \
                "` (`Référence`, `Anode`, `Cathode`, `Disposition`, `Type`, `NuméroLed`, `NuméroTest`) VALUES ( %s, %s, %s, %s, %s, %s, %s)"  # on ajoute la ligne
            val = (ref, anode, cathode, disposition, Type, numled, numtest)
            print(sql, val)
            cursor.execute(sql, val)
            connection.commit()  # Commit n'est pas fait automatiquement sur python, c'est nécessaire pour les transactions qui modifient la BDD
            # on ajoute la nouvelle ref à la BDD
            print("La ligne est ajouté à la table ", table)
        except Error as e:
            print("Error while connecting and inserting data to MySQL", e)

    # cette fonction permet d'ajouter une référence de LED.

    def ajouter_ligne_led(self, Ref, Tension, TensionMin, TensionMax, Courant, CourantMin, CourantMax, Couleur):
        try:
            # on ajoute la ligne
            sql = "INSERT INTO `leds` (`Référence`, `Tension`, `Tension min`, `Tension max`, `Courant`, `Courant min`, `Courant max`, `Couleur`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (Ref, Tension, TensionMin, TensionMax,
                   Courant, CourantMin, CourantMax, Couleur)
            print(sql, val)
            cursor.execute(sql, val)
            connection.commit()  # Commit n'est pas fait automatiquement sur python, c'est nécessaire pour les les transactions qui modifient la BDD
            # on ajoute la nouvelle ref à la BDD
            print("La Référence LED à été ajoutée")
        except Error as e:
            print("Error while connecting and inserting data to MySQL", e)

    def liste_table(self):  # Liste toute les tables de la BDD
        try:
            commande_sql = "SHOW TABLES"
            cursor.execute(commande_sql)
            for table in cursor:
                print(table)
            connection.commit()
        except Error as e:
            print("Error while connecting and inserting data to MySQL", e)

    # Fonction qui permet la leture de table, récupère et retransmet l'information sous forme de liste

    def get_table_ref(self, table):
        try:
            # réduit toute les majuscules en minuscules car les nom des tables sont en minuscule
            table = table.lower()
            # récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            commande_sql = "select * from `"+table + \
                "` order by `NuméroTest`, `Type`, `NuméroLed`"
            cursor.execute(commande_sql)
            records = cursor.fetchall()
            # print(records)
            return records
        except Error as e:
            print("Error while reading produits", e)

    # Fonction qui permet la leture de table, récupère et retransmet l'information sous forme de liste
    def get_table(self, table):
        try:
            # réduit toute les majuscules en minuscules car les nom des tables sont en minuscule
            table = table.lower()
            # récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            commande_sql = "select * from `"+table+-"`"
            cursor.execute(commande_sql)
            records = cursor.fetchall()
            # print(records)
            return records
        except Error as e:
            print("Error while reading produits", e)

    def get_calib(self):  # Fonction qui permet la leture de table, récupère et retransmet l'information sous forme de liste
        try:
            # récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            commande_sql = "select * from `calibration`"
            cursor.execute(commande_sql)
            records = cursor.fetchall()
            # print(records)
            return records
        except Error as e:
            print("Error while reading produits", e)

    # Fonction qui permet la leture de table, récupère et retransmet l'information sous forme de liste
    def set_calib(self, liste):
        try:
            commande_sql = "delete from `calibration`"  # supprime le contenu de la table
            cursor.execute(commande_sql)
            commande_sql = "INSERT INTO `calibration`(`piste 1`, `piste 2`,`piste 3`,`piste 4`,`piste 5`,`piste 6`,`piste 7`,`piste 8`,`piste 9`,`piste 10`,`piste 11`,`piste 12`,`piste 13`,`piste 14`,`piste 15`,`piste 16`,`piste 17`,`piste 18`,`piste 19`,`piste 20`,`piste 21`,`piste 22`,`piste 23`,`piste 24`,`piste 25`,`piste 26`,`piste 27`,`piste 28`,`piste 29`,`piste 30`,`piste 31`,`piste 32`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # supprime le contenu de la table
            cursor.execute(commande_sql, liste)
            connection.commit()
            # print(records)
            return 1
        except Error as e:
            print("Error while reading produits", e)

    def get_line(self, table, colonne, ref):
        try:
            # réduit toute les majuscules en minuscules car les nom des tables sont en minuscule
            table = table.lower()
            # récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            commande_sql = "select * from `"+table+"` where `"+colonne+"` = \""+ref+"\""
            cursor.execute(commande_sql)
            records = cursor.fetchall()
            # print(records)
            return records
        except Error as e:
            print("Error while reading produits", e)

    # cette fonction permet de selectionner la data d'un tableau

    def get_datasorted(self, ligne, colonne, produit):
        data = produit[ligne][colonne]  # colonne et ligne commencent à 0
        print(data)
        return data

    # supprime une ligne d'un tableau à partir du choix de collone et de son contennu

    def delete_line(self, table, colonne, condition):
        try:
            if type(condition) is not int:
                # on rajoute des guillemets dans la chaine de charac si il ne s'agit pas d'un int
                condition = '\"'+condition+'\"'
            # récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            sql = "delete from `"+table+"` where `" + \
                colonne+"` = "+str(condition)+""
            cursor.execute(sql)
            connection.commit()
            print("Line deleted")
        except Error as e:
            print("failed to delete line, Error :", e)

    def delete_table(self, table):  # cette fonction permet la suppression d'une table
        try:
            sql = "DROP TABLE `"+table+"`"  # on supprime la table
            cursor.execute(sql)
            connection.commit()
            self.delete_line("produits", "Référence", table)
            print("table", table, " supprmiée")
        except Error as e:
            print("failed to delete table, Error :", e)

    def connect(self, ip, nombdd):  # cette fonction se connecte à la BDD
        global connection, cursor
        try:
            connection = mysql.connector.connect(host=ip,  # connexion à la BDD
                                                 database=nombdd,
                                                 user='alex',
                                                 password='seribase',
                                                 port=3306)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version", db_Info)
                cursor = connection.cursor()
        except Error as e:
            print("Failed connecting to database, Error:", e)

    def disconnect(self):  # cette fonction se déconnecte de la BDD
        cursor.close()
        connection.close()                                  # Déconnexion de la BDD
        print("MySQL connection is closed")


"""
Bdd = BddTesteur()
Bdd.connect("testeur assemblage")
#Bdd.nouvelle_reference("HC1-33")
#Bdd.delete_line("leds", "Référence", "HC13-454")
#Bdd.ajouter_ligne_ref("hc1-33", "test", 6, 3, 0, 0, 6, 1)
#Bdd.delete_table("HC1-33")
#produit = Bdd.get_table("leds")
#Bdd.get_datasorted(0,2,produit)
#Bdd.ajouter_ligne_led("HC13-454", 2, 1.7, 3.2, 10, 7.5, 11.5, "rouge")
Bdd.disconnect()
#t=Test()
#t.send("this is data")
"""
#Bdd = BddTesteur("192.168.1.83", "testeur assemblage")
# Bdd.nouvelle_reference("K2210-052-2000")
#Bdd.ajouter_ligne_ref("hc1-33aze", "led1", 21, 8, 0, 0, 6, 3)
