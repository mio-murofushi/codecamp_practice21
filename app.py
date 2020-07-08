from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import model.database as db
from model.item import Item

app= Flask(__name__)
infomation=[]

@app.route("/")
def employee_top():
    infomation = db.get_infomation()

    params ={
        "infomation" : infomation
    }

    return render_template("employee_top.html", **params)

@app.route("/search")
def search_employee():
    return render_template("search_employee.html")