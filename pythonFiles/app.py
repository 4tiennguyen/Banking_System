from flask import Flask, render_template, make_response, request, redirect, flash
import mysql.connector
import requests
from requests import ConnectionError

app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"

#Database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bankdb'

db = mysql.connector.connect(user=app.config['MYSQL_USER'], database = app.config['MYSQL_DB'])
cursor = db.cursor(dictionary = True)

try:
    query = "CREATE DATABASE IF NOT EXISTS bankdb;"
    cursor.execute(query)
    db.commit()
except:
    pass


@app.route("/", methods = ['POST', 'GET'])
def form():
    db = mysql.connector.connect(user = app.config['MYSQL_USER'], database = app.config['MYSQL_DB'])
    cursor = db.cursor(dictionary = True)
    if request.method == "POST":
        un = request.form.get("un")
        pw = request.form.get("pw")
        req = request.form.get("req")
        if (req == 'login'):
            query = "SELECT * FROM login_data WHERE Username = '" + un + "' AND Password = '" + pw + "';"
            cursor.execute(query)
            info = cursor.fetchall()
            if info == "":
                redirect("/")
            else:
                cook = make_response()
                cook.set_cookie("userData", info)
        return redirect("account")
    return render_template('index.html')

@app.route("/account", methods = ['POST', 'GET'])
def acct():
    return render_template("account.html")


def hello_world():
    return "<p>Hello, World!</p>"

cursor.close()

if __name__ == "__main__":
    app.run(debug = True)