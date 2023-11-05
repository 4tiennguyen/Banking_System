from flask import Flask, render_template, make_response, request, redirect, flash, session, url_for
import mysql.connector
import requests
from requests import ConnectionError

app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
app.secret_key = 'APP_SECRET_KEY'

# Database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bankdb'

# Database connection
db = mysql.connector.connect(user=app.config['MYSQL_USER'], database = app.config['MYSQL_DB'])
cursor = db.cursor(dictionary = True)

try:
    query = "CREATE DATABASE IF NOT EXISTS bankdb;"
    cursor.execute(query)
    db.commit()
except:
    pass


@app.route("/", methods = ['POST', 'GET'])
def index():
    db = mysql.connector.connect(user = app.config['MYSQL_USER'], database = app.config['MYSQL_DB'])
    cursor = db.cursor(dictionary = True)
    if request.method == "POST":
        em = request.form.get("em")
        pw = request.form.get("pw")
        req = request.form.get("req")
        if (req == 'Login'):
            query = "SELECT * FROM login_data WHERE Email = '" + em + "' AND Password = '" + pw + "';"
            cursor.execute(query)
            info = cursor.fetchall()
            print(info)
            if (len(info) == 0):
                return redirect(url_for("index"))
            else:
                session['email'] = em
        elif (req == "Sign up"):
            try:
                query = "INSERT INTO login_data (Email, Password) VALUES ('" + em + "', '" + pw + "');"
                cursor.execute(query)
            except:
                return redirect(url_for("index"))
        return redirect(url_for("acct"))
    return render_template('index.html')


@app.route("/account", methods = ['POST', 'GET'])
def acct():
    info = {}
    info[0] = session['email']
    info[1] = [{"0": "run", "1": "walk", "2": "swim"}, {"run": "1"}]
    '''
    try:
        query = "SELECT * FROM transaction_data WHERE AccountID = (SELECT AccountID FROM account_data WHERE PeronID = (SELECT PersonID FROM person_data WHERE Email = '" + info[0] + "'));"
        # Select from transaction_data
        #   Select from account_data
        #       Select from person_data
        cursor.execute(query)
        info = cursor.fetchall()
    except:
        return "<p>No transaction data found.</p> <a href='/' target='_blank'>Click here to go back</a>"
    '''
    return render_template("account.html", info=info)

cursor.close()

if __name__ == "__main__":
    app.run(debug = True)