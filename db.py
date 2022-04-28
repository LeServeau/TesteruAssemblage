import mysql.connector


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

    # Cette méthode permet de récuperer l'utilisateur et le renvois
    def userExistAndPasswordIsValid(self, username, password):
        cursor = self.db.cursor()

        cursor.execute(
            'SELECT username FROM users WHERE username = %s AND password = %s', (
                username, password)
        )

        return cursor.fetchone()
