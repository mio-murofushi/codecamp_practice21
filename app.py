from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import re
from mysql.connector import errorcode
import model.database as db
from model.employee import Employee
from model.department import Department
from model.photo import  Photo

app= Flask(__name__)
employee_infomation=[]

# フォルダ
UPLOAD_FOLDER = './static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["POST","GET"])
def employee_top():
    employee_infomation = db.get_employee_infomation()
    del_mes = ""

    params ={
        "employee_infomation" : employee_infomation,
        "del_mes" : del_mes
    }
    return render_template("employee_top.html", **params)

@app.route("/delete", methods=["POST", "GET"])
def delete_employee():
    change_infomation, delete_id="",""
    del_mes = ""

    if "delete_infomation" in request.form.keys():
        delete_id = request.form.get("delete_id")
        del_mes = db.delete_employee_info(delete_id)

    return redirect(url_for('employee_top', del_mes=del_mes))

@app.route("/search", methods=["POST", "GET"])
def search_employee():
    return render_template("search_employee.html")

@app.route("/search/result")
def search_managiment_employee():
    return render_template("search_managiment_employee.html")

# search employee.htmlの表示用
@app.route("/search/managiment", methods=["POST","GET"])
def fix_employee_infomation():
    return render_template("fix_employee.html")

@app.route("/department", methods=["GET", "POST"])
def department_top():
    department_infomation = db.get_department_infomation()
    params = {
        "department_infomation" : department_infomation
    }
    return render_template("department_top.html", **params)

# 新規部署の追加
@app.route("/department/add", methods=["GET", "POST"])
def add_department():
    new_department_name=""

    if "add_new_department_name" in request.form.keys():
        new_department_name = request.form.get("new_department_name")

    db.add_department_info(new_department_name)
    return render_template("add_new_department.html")

@app.route("/department/add/result", methods=["GET", "POST"])
def result_add_department():
    return render_template("result.html")