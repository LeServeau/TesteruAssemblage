import mysql.connector
from flask import request
from mysql.connector import Error


class DB:
    def __init__(self, user, password, host, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def getProducts(self):
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT produits_id, produits_name FROM `produits` ORDER BY `produits_id`'
        )
        return cursor.fetchall()

    def getRef(self):
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT id, NomReference FROM `références` ORDER BY `id`'
        )
        return cursor.fetchall()

    # Cette méthode permet de récuperer l'utilisateur et le renvois
    def userExistAndPasswordIsValid(self, username, password):
        cursor = self.db.cursor()

        cursor.execute(
            'SELECT username FROM users WHERE username = %s AND password = %s', (
                username, password)
        )

        return cursor.fetchone()

    def new_product_LED(self, product, label, anode, cathode):
        cursor = self.db.cursor()
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

    def new_product_TOUCHES(self, product, label_touche, resMax, resMin, P_b, P_a):
        cursor = self.db.cursor()
        # vérifie si la liste retournée est vide ou non, si comporte des caractè
        # re, le produit existe déjà donc on ajoute pas à la BDD
        if self.get_product(product):
            print("le produit existe déjà")
        else:
            NameProduct = request.form["NameProduct"]
            label_touche = request.form["label_touche"]
            ResMax = request.form["ResMax"]
            ResMin = request.form["ResMin"]
            Pa = request.form["Pa"]
            Pb = request.form["Pb"]
            try:
                #####POUR AJOUTER PRODUIT TOUCHES#####
                commande_sql = "INSERT INTO `produits` VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(commande_sql, (NameProduct,
                               label_touche, ResMax, ResMin, Pa, Pb))
                # on ajoute le nouveau produit à la BDD
                print("Le produitTOUCHES est ajouté à la BDD")
            except Error as e:
                print("Error while connecting and inserting data to MySQL", e)

    def new_reference(self, NameRef, MaxV, MinV, MaxC, MinC):
        ###Mettre la requete SQL pour ajouter ref a la BDD###
        cursor = self.db.cursor()
        commande_sql = """INSERT INTO références (NomReference, MaxVoltage, MinVoltage, MaxCourant, MinCourant) VALUES (%s, %s, %s, %s, %s) """
        data = (NameRef, MaxV, MinV, MaxC, MinC)
        cursor.execute(commande_sql, data)
        self.db.commit()
        print("La Référence " + NameRef + " est ajouté à la BDD...")

        # Puis l'appeler dans app.py avec db.new_reference" dans la route /admin/products/add

    def get_product(self, reaserch):
        cursor = self.db.cursor()
        try:
            commande_sql = "SELECT DISTINCT(produits_name) FROM `produits` WHERE (produits_name = \""+reaserch+"\")"
            cursor.execute(commande_sql)  # execute la commande SQL
            records = cursor.fetchall()  # Récupère la réponse de la BDD
            print(records)
            return records
        except Error as e:
            print("Error while retrieving data from MySQL", e)
