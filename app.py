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

    params = {
        "employee_infomation" : employee_infomation,
        "del_mes" : del_mes
    }
    return render_template("employee_top.html", **params)

# 社員情報の削除
@app.route("/delete_employee_info", methods=["POST", "GET"])
def delete_employee():
    delete_employee_id=""
    del_mes = ""

    if "delete_infomation" in request.form.keys():
        delete_employee_id = request.form.get("delete_employee_id")
        del_mes = db.delete_employee_info(delete_employee_id)

    return redirect(url_for('employee_top', del_mes=del_mes))

# 社員管理　検索画面
@app.route("/search", methods=["POST", "GET"])
def search_employee():
    department_infomation=[]
    department_infomation = db.get_department_infomation()
    get_search_employee_infomation(department_infomation)

    params = {
        "department_infomation":department_infomation
    }
    return render_template("search_employee.html", **params)

# 検索情報の取得
def get_search_employee_infomation(department_infomation):
    search_department_name,search_employee_id, search_employee_name = "", "", ""
    if "search" in request.form.keys():
        search_department_name = request.form.get("search_department_name")
        search_employee_id = request.form.get("search_employee_id")
        search_employee_name = request.form.get("search_employee_name")
        #check_search_employee_infomation(search_department_name, search_employee_id, search_employee_name)

# 検索情報の
"""
def check_search_employee_infomation(search_department_name, search_employee_id, search_employee_name):
"""

@app.route("/search/result")
def search_managiment_employee():
    return render_template("search_managiment_employee.html")

# 社員情報の編集・新規登録の表示用
@app.route("/fix_employee", methods=["GET","POST"])
def add_new_employee_infomation():
    fix_employee_id = ""
    if "change_infomation" in request.form.keys():
        fix_employee_id = request.form.get("fix_employee_id")
    return render_template("fix_employee.html")

# 社員情報の新規登録
@app.route("/fix_employee/add", methods=["GET", "POST"])
def add_new_employee():
    #if "add_new_employee" in request.form.keys():
        # 全要素取得
    return redirect(url_for('employee_top'))

# search employee.htmlの表示用
@app.route("/search/managiment", methods=["POST","GET"])
def fix_employee_infomation():
    return render_template("fix_employee.html")

# 部署管理トップページ
@app.route("/department", methods=["GET", "POST"])
def department_top():
    mes=""
    department_infomation = db.get_department_infomation()

    if "change_department" in request.form.keys():
        fix_department_id = request.form.get("fix_department_id")
        fix_department_name = request.form.get("fix_department_name")
        params = {
            "fix_department_id":fix_department_id,
            "fix_department_name":fix_department_name
            }
        return render_template("fix_department.html", **params)
    params = {
        "department_infomation" : department_infomation,
        "mes": mes
    }
    return render_template("department_top.html", **params)

# 新規部署の追加
@app.route("/department/add", methods=["GET", "POST"])
def add_department():
    new_department_name, mes="",""

    if "add_new_department_name" in request.form.keys():
        new_department_name = request.form.get("new_department_name")
        mes = db.add_department_info(new_department_name)
        return redirect(url_for('department_top', mes=mes))
        
    return render_template("add_new_department.html")

# 既存部署の部署名変更
@app.route("/department/fix", methods=["GET", "POST"])
def fix_department_infomation():
    department_rename, mes="",""
    if "rename" in request.form.keys():
        department_rename = request.form.get("department_rename")
        fix_department_id = request.form.get("fix_department_id")
        mes = db.fix_department_rename(fix_department_id, department_rename)
    
    return redirect(url_for('department_top', mes=mes))

# 部署情報の削除
@app.route("/delete_department_info", methods=["GET", "POST"])
def delete_department():
    delete_department_id=""
    del_mes = ""

    if "delete_department" in request.form.keys():
        delete_department_id = request.form.get("delete_department_id")
        del_mes = db.delete_department_info(delete_department_id)

    return redirect(url_for('department_top', del_mes=del_mes))