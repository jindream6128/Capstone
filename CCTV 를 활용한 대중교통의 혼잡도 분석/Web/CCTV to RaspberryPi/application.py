from flask import Flask, render_template
import sys
application = Flask(__name__)
from dbconn import *


@application.route("/") 
def hello(): #main 페이지
    return render_template("hello.html")

@application.route("/1") 
def one():     
    return render_template("1.html")

@application.route("/2") 
def two():
    return render_template("2.html")

@application.route("/3") 
def three():
    return render_template("3.html")

@application.route("/4") 
def four():     
    return render_template("4.html")

@application.route("/dashboard") 
def dashboard():     
    cursor = db.cursor()
    sql = """SELECT * FROM bus WHERE busID = (SELECT MAX(busID) FROM bus);"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template("dashboard.html", result=result)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=True)