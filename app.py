from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import model.database as db

app= Flask(__name__)

@app.route("/", methods=["GET","POST"])
def employee_top():
    return render_template("employee_top.html")