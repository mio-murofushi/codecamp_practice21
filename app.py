from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import re, os
from mysql.connector import errorcode
import model.database as db
from model.employee import Employee
from model.department import Department
from model.photo import  Photo

app= Flask(__name__)
employee_infomation=[]

# フォルダ
UPLOAD_FOLDER = './static/images/'
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
    #get_search_employee_infomation(department_infomation)

    params = {
        "department_infomation":department_infomation
    }
    return render_template("search_employee.html", **params)

# 検索情報の取得
@app.route("/search/result", methods=["GET", "POST"])
def get_search_employee_infomation():
    search_department_name,search_employee_id, search_employee_name = "", "", ""
    if "search" in request.form.keys():
        search_department_name = request.form.get("search_department_name")
        search_employee_id = request.form.get("search_employee_id")
        search_employee_name = request.form.get("search_employee_name")
        #check_search_employee_infomation(search_department_name, search_employee_id, search_employee_name)
    
    return render_template("search_managiment_employee.html")

# 社員情報の編集・新規登録の表示用
@app.route("/fix_employee", methods=["GET","POST"])
def add_new_employee_infomation():
    department_infomation = db.get_department_infomation()
    if "change_infomation" in request.form.keys():
        fix_employee_id = request.form.get("fix_employee_id")
        can_get_fix_infomation, fix_employee_id, fix_employee_name, fix_employee_age, fix_gender, fix_photo_id, fix_department_id, fix_join_date, fix_photo_name, fix_postalcode, fix_adress, fix_prefectures = db.get_select_employee_infomation(fix_employee_id)
        fix_department_name = db.get_department_name(fix_department_id)
        fix_photo_name = db.get_photo_name(fix_photo_id)
        params = {
        "department_infomation" : department_infomation,
        "can_get_fix_infomation" : can_get_fix_infomation,
        "fix_employee_id" : fix_employee_id,
        "fix_employee_name" : fix_employee_name,
        "fix_employee_age" : fix_employee_age,
        "fix_gender" : fix_gender,
        "fix_photo_id" : fix_photo_id,
        "fix_department_id" : fix_department_id,
        "fix_join_date" : fix_join_date,
        "fix_photo_name" : fix_photo_name,
        "fix_postalcode" : fix_postalcode,
        "fix_adress" : fix_adress,
        "fix_department_name" : fix_department_name,
        "fix_prefectures" :fix_prefectures
        }
        return render_template("fix_employee.html", **params)
    
    params = {
        "department_infomation" : department_infomation
    }
    return render_template("fix_employee.html", **params)

# 社員情報の変更
@app.route("/fix_employee/fix" , methods={"GET","POST"})
def change_new_employee():
    if "change_new_employee_infomation" in request.form.keys():
        # 社員情報の変更情報等の取得
        new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date = get_new_all_employee_infomation()
        # 社員情報の新規情報の形式確認
        check_mes = check_new_all_employee_infomation(new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date)
        if check_mes=="":
            all_employee_infomation = db.get_all_employee_infomation()
            new_photo_id = db.get_photo_infomation()
            connect_adress = connect_adress_info(new_postalcode, new_adress)
            result_mes = db.add_new_employee_info(new_employee_id, new_employee_name, new_employee_age, new_gender, new_photo_id, file_name, connect_adress, new_department, update_join_date, update_leave_date)
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name.filename))
        if not update_leave_date == "":
            if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', update_leave_date):
                db.add_leave_date(update_leave_date, new_employee_id)
            else:
                check_mes =  "退社日の形式を確認して下さい"
    return redirect(url_for('result_add_employee', check_mes=check_mes, reslut_mes=result_mes))


# 社員情報の新規登録
@app.route("/fix_employee/add", methods=["GET", "POST"])
def add_new_employee():
    new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date = "", "", "", "", "", "", "", "", "", "", ""
    result_mes = "失敗"
    check_mes = ""
    
    if "add_new_employee_infomation" in request.form.keys():
        # 社員情報の新規情報の取得
        new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date = get_new_all_employee_infomation()
        # 社員情報の新規情報の形式確認
        check_mes = check_new_all_employee_infomation(new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date)
        if check_mes=="":
            all_employee_infomation = db.get_all_employee_infomation()
            new_photo_id = db.get_photo_infomation()
            connect_adress = connect_adress_info(new_postalcode, new_prefectures, new_adress)
            result_mes = db.add_new_employee_info(new_employee_id, new_employee_name, new_employee_age, new_gender, new_photo_id, file_name, connect_adress, new_department, update_join_date, update_leave_date)
            file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name.filename))
        if not update_leave_date == "":
            if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', update_leave_date):
                db.add_leave_date(update_leave_date, new_employee_id)
            else:
                check_mes =  "退社日の形式を確認して下さい"
    return redirect(url_for('result_add_employee', check_mes=check_mes, reslut_mes=result_mes))

# 社員情報の新規情報取得
def get_new_all_employee_infomation():
    new_employee_id = request.form.get("new_employee_id")
    new_employee_name = request.form.get("new_employee_name")
    new_employee_age = request.form.get("new_employee_age")
    new_gender = request.form.get("new_gender")
    file_name = request.files["file_name"]
    new_postalcode = request.form.get("new_postalcode")
    new_prefectures = request.form.get("new_prefectures")
    new_adress = request.form.get("new_adress")
    new_department = request.form.get("new_department")
    update_join_date = request.form.get("update_join_date")
    update_leave_date = request.form.get("update_leave_date")
    return new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date

# 社員情報の新規情報の形式検査
def check_new_all_employee_infomation(new_employee_id, new_employee_name, new_employee_age, new_gender, file_name, new_postalcode, new_prefectures, new_adress, new_department, update_join_date, update_leave_date):
    if new_employee_id=="" or new_employee_name == "" or new_employee_age=="" or new_gender=="" or file_name=="" or new_postalcode=="" or new_prefectures=="" or new_adress=="" or new_department=="" or update_join_date=="":
        return "未入力の欄が存在しています。"
    if not re.match(r'^EMP+[0-9]{4}', new_employee_id):
        return "社員番号の表記が違います。"
    if not re.match(r'[0-9]{2}', new_employee_age):
        return "正しい年齢を入力してください"
    if not re.match(r'.+?[市|町|村|区]', new_adress):
        return "住所の入力を確認してください。"
    if new_gender=="":
        return "性別を選択してください。"
    if not re.match(r'([^\s]+(\.(?i)(jpeg|png))$)', file_name.filename):
        return "写真ファイルの拡張子を確認してください。"
    if not re.match(r'[0-9]{3}-[0-9]{4}', new_postalcode):
        return "郵便番号の形式を確認してください"
    if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', update_join_date):
        return "入社日の形式を確認して下さい"
    return ""

# 住所の接続。
def connect_adress_info(new_postalcode, new_prefectures, new_adress):
    connect_adress = ""
    connect_adress = "〒"+new_postalcode+" "+ new_prefectures + new_adress
    print(connect_adress)
    return connect_adress

# 社員情報の新規登録結果
@app.route("/fix_employee/add/result", methods=["GET","POST"])
def result_add_employee():
    return render_template("result_add.html", check_mes = request.args.get("check_mes"))

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
            "department_infomation" : department_infomation,
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