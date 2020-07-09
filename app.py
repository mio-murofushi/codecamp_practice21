from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import model.database as db
from model.employee import Employee
from model.department import Department
from model.photo import  Photo

app= Flask(__name__)
employee_infomation=[]

@app.route("/")
def employee_top():
    employee_infomation = db.get_employee_infomation()

    params ={
        "employee_infomation" : employee_infomation
    }

    return render_template("employee_top.html", **params)

@app.route("/search")
def search_employee():
    return render_template("search_employee.html")

@app.route("/search/result")
def search_managiment_employee():
    return render_template("search_managiment_employee.html")

# search employee.htmlの表示用
@app.route("/search/managiment")
def fix_employee_employee_infomation():
    return render_template("fix_employee.html")

@app.route("/department")
def department_top():
    department_infomation = db.get_department_infomation()
    params = {
        "department_infomation" : department_infomation
    }
    return render_template("department_top.html", **params)