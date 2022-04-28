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

    def nouvelle_reference(self,ref) :                       #fonction qui ajoute une nouvelle référence à une base de donnée si elle n'existe pas déjà
        if self.get_reference(ref):                              #vérifie si la liste retournée est vide ou non, si comporte des caractère, le produit existe déjà donc on ajoute pas à la BDD
            print("le produit existe déjà")
        else:
            try:
                commande_sql = "INSERT INTO `produits` (`Référence`) VALUES ('" + ref + "');"
                cursor.execute(commande_sql)
                print("Le produit est ajouté à la BDD")         #on ajoute la nouvelle ref à la BDD
            except Error as e:
                print("Error while connecting and inserting data to MySQL", e)
            finally:
                if connection.is_connected():
                    try :
                        commande_sql = "CREATE TABLE `"+ref+"` (Référence VARCHAR(32), Anode TINYINT, Cathode TINYINT, Disposition TINYINT, Type TINYINT, NuméroLed INT)"
                        cursor.execute(commande_sql)                #On créer une nouvelle table pour le nouveau produit
                    except:
                        print("ERROR creating a new table for the new product")


    def get_reference(self,reaserch):           #cette fonction recherche dans la table produit si le produit est déjà inscrit dans la BDD
        try:
            commande_sql = "SELECT DISTINCT(Référence) FROM `produits` WHERE (Référence = \""+reaserch+"\")"
            cursor.execute(commande_sql)        #execute la commande SQL
            records = cursor.fetchall()         #Récupère la réponse de la BDD
            print(records)
            return records
        except Error as e:
            print("Error while retrieving data from MySQL", e)



    def ajouter_ligne_ref(self,table, ref, anode, cathode, disposition, Type, numled):   #permet d'ajouter une ligne à une table produit
        try:
            sql = "INSERT INTO `"+table+"` (`Référence`, `Anode`, `Cathode`, `Disposition`, `Type`, `NuméroLed`) VALUES ( %s, %s, %s, %s, %s, %s)"  #on ajoute la ligne
            val = (ref, anode, cathode, disposition, Type, numled)
            print(sql, val)
            cursor.execute(sql, val)
            connection.commit()                                 #Commit n'est pas fait automatiquement sur python, c'est nécessaire pour les les transactions qui modifient la BDD
            print("La ligne est ajouté à la table ", table)     #on ajoute la nouvelle ref à la BDD
        except Error as e:
            print("Error while connecting and inserting data to MySQL", e)



    def ajouter_ligne_led(self, Ref, Tension, TensionMin, TensionMax, Courant, CourantMin, CourantMax, Couleur):    #cette fonction permet d'ajouter une référence de LED.
        try:
            sql = "INSERT INTO `leds` (`Référence`, `Tension`, `Tension min`, `Tension max`, `Courant`, `Courant min`, `Courant max`, `Couleur`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"  # on ajoute la ligne
            val = (Ref, Tension, TensionMin, TensionMax, Courant, CourantMin, CourantMax, Couleur)
            print(sql, val)
            cursor.execute(sql, val)
            connection.commit()  # Commit n'est pas fait automatiquement sur python, c'est nécessaire pour les les transactions qui modifient la BDD
            print("La Référence LED à été ajoutée")  # on ajoute la nouvelle ref à la BDD
        except Error as e:
            print("Error while connecting and inserting data to MySQL", e)




    def liste_table(self):                                   #Liste toute les tables de la BDD
        try:
            commande_sql = "SHOW TABLES"
            cursor.execute(commande_sql)
            for table in cursor:
                print(table)
            connection.commit()
        except Error as e:
            print("Error while connecting and inserting data to MySQL", e)



    def get_table(self, table):                              #Fonction qui permet la leture de table, récupère et retransmet l'information sous forme de liste
        try:
            table = table.lower()                           #réduit toute les majuscules en minuscules car les nom des tables sont en minuscule
            commande_sql = "select * from `"+table+"` "     #récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            cursor.execute(commande_sql)
            records = cursor.fetchall()
            print(records)
            return records
        except Error as e:
            print("Error while reading produits", e)



    def get_line(self, table, colonne, ref):
        try:
            table = table.lower()                           #réduit toute les majuscules en minuscules car les nom des tables sont en minuscule
            commande_sql = "select * from `"+table+"` where `"+colonne+"`"     #récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            cursor.execute(commande_sql)
            records = cursor.fetchall()
            print(records)
            return records
        except Error as e:
            print("Error while reading produits", e)



    def get_datasorted(self, ligne,colonne,produit):          #cette fonction permet de selectionner la data d'un tableau
        data = produit[ligne][colonne]                  #colonne et ligne commencent à 0
        print(data)
        return data



    def delete_line(self, table, colonne, condition):            #supprime une ligne d'un tableau à partir du choix de collone et de son contennu
        try :
            if type(condition) is not int:
                condition = '\"'+condition+'\"'             #on rajoute des guillemets dans la chaine de charac si il ne s'agit pas d'un int
            sql = "delete from `"+table+"` where `"+colonne+"` = "+str(condition)+""  # récupère les information de la table et les tri par typ (led, 8segements, forme, bouton)
            cursor.execute(sql)
            connection.commit()
            print("Line deleted")
        except Error as e:
            print("failed to delete line, Error :", e)


    def delete_table(self, table):             #cette fonction permet la suppression d'une table
        try:
            sql = "DROP TABLE `"+table+"`"      #on supprime la table
            cursor.execute(sql)
            connection.commit()
            self.delete_line("produits", "Référence", table)
            print("table",table," supprmiée")
        except Error as e:
            print("failed to delete table, Error :", e)


    def connect(self, nombdd):                                      #cette fonction se connecte à la BDD
        global connection,cursor
        try:
            connection = mysql.connector.connect(host='192.168.1.65',  # connexion à la BDD
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



    def disconnect(self):                                   #cette fonction se déconnecte de la BDD
        cursor.close()
        connection.close()                                  # Déconnexion de la BDD
        print("MySQL connection is closed")


Bdd = BddTesteur()
Bdd.connect("testeur assemblage")
#Bdd.nouvelle_reference("HC1-33")
#Bdd.delete_line("leds", "Référence", "HC13-454")
#Bdd.ajouter_ligne_ref("hc1-33", "test", 6, 3, 0, 0, 6)
#Bdd.delete_table("HC1-33")
#produit = Bdd.get_table("leds")
#Bdd.get_datasorted(0,2,produit)
#Bdd.ajouter_ligne_led("HC13-454", 2, 1.7, 3.2, 10, 7.5, 11.5, "rouge")
Bdd.disconnect()
#t=Test()
#t.send("this is data")

