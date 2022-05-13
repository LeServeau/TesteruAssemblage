from unicodedata import name
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_mysqldb import MySQL
import MySQLdb.cursors
import yaml

from db import DB

app = Flask(__name__)
app.secret_key = 'secretkey'

# Configure db
db = yaml.load(open('database/db.yaml'))
# app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
# app.config['MYSQL_DB'] = db['mysql_db']

# mysql = MySQL(app)
db = DB(user=db['mysql_user'], password=db['mysql_password'],
        host=db['mysql_host'], database=db['mysql_db'])


@app.route('/',  methods=['GET'])
def index():
    products = db.getProducts()
    print(products)

    return render_template('index.html', produits=products)


@app.route('/admin/login', methods=['GET'])
def showLoginPage():
    return render_template('admin/login.html')


@app.route('/admin/login', methods=['POST'])
def loginIntoAdmin():
    if 'username' in request.form and 'password' in request.form:
        # Variable d'accès pour loginAdmin
        username = request.form['username']
        password = request.form['password']

        user = db.userExistAndPasswordIsValid(username, password)
        print(username)

        if user:
            # Create session data, we can access this data in other routes
            print(user)
            session['loggedin'] = True
            session['username'] = user[0]
            # Redirect to adminConfig page
            return redirect(url_for('showAdminConfiguration'))
            # return "Test reussis"

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('admin/login.html', msg=msg)


@app.route('/admin/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('username', None)

    return redirect(url_for('showLoginPage'))


@app.route('/admin/configuration', methods=['GET'])
def showAdminConfiguration():
    if not isLoggedIn():
        return redirect(url_for('showLoginPage'))

    products = db.getProducts()

    return render_template('admin/configuration.html', username=session['username'])


@app.route('/admin/reference/add', methods=['POST'])
def newReference():
    data = request.get_json()

    nameReference = data["nameReference"]
    maximumVoltage = data["maximumVoltage"]
    minimumVoltage = data["minimumVoltage"]
    maximumCurrent = data["maximumCurrent"]
    minimumCurrent = data["minimumCurrent"]

    db.new_reference(nameReference, maximumVoltage,
                     minimumVoltage, maximumCurrent, minimumCurrent)

    print(data)
    return jsonify({"Name Référence": nameReference, "maximumVoltage": maximumVoltage, "minimumVoltage": minimumVoltage, "maximumCurrent": maximumCurrent, "minimumCurrent": minimumCurrent})


@app.route('/admin/configuration', methods=['POST'])
def updateConfiguration():
    if not isLoggedIn():
        return redirect(url_for('showLoginPage'))

    return redirect(url_for('showAdminConfiguration'))


def isLoggedIn():
    return 'loggedin' in session


if __name__ == '__main__':
    app.run()
