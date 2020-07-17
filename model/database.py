import mysql.connector
import re
from mysql.connector import errorcode
from model.const import DB
from model.employee import Employee
from model.department import Department
from model.photo import  Photo

def get_db_cursor():
    cnx = mysql.connector.connect(
        user=DB["DB_USER_NAME"],
        password=DB["DB_PASSWORD"],
        host=DB["DB_HOST"],
        database=DB["DB_NAME"])
    return cnx, cnx.cursor()

def printerror(err):
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("ユーザ名かパスワードに問題があります。")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("データベースが存在しません。")
    else:
        print(err)

def get_all_employee_infomation():
    all_employee_infomation = []
    try:
        cnx, cursor = get_db_cursor()
        query="SELECT employee_infomation.employee_id, employee_infomation.employee_name, employee_infomation.employee_age, employee_infomation.gender, employee_infomation.photo_id, employee_infomation.adress, employee_infomation.department_id, department.department_name, ID_photo.photo_name FROM employee_infomation JOIN department ON employee_infomation.department_id = department.department_id JOIN ID_photo ON employee_infomation.photo_id = ID_photo.photo_id"
        cursor.execute(query)

        for (employee_id, employee_name, employee_age, gender, photo_id, adress, department_id, department_name, photo_name) in cursor:
            employee = Employee(employee_id=employee_id, employee_name=employee_name, employee_age=employee_age, gender=gender, photo_id=photo_id, adress=adress, department_id=department_id)
            department = Department(department_id=department_id)
            photo = Photo(photo_name=photo_name)
            all_employee_infomation.append(employee)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return all_employee_infomation

def get_employee_infomation():
    employee_infomation = []
    try:
        cnx, cursor = get_db_cursor()
        query=("SELECT id, employee_id, employee_name FROM employee_infomation")
        cursor.execute(query)

        for (id, employee_id, employee_name) in cursor:
            employee = Employee( id=id, employee_id = employee_id, employee_name = employee_name)
            employee_infomation.append(employee)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return employee_infomation

def get_department_infomation():
    department_infomation = []
    try:
        cnx, cursor = get_db_cursor()
        get_department_query = ("SELECT department_id, department_name FROM department")
        cursor.execute(get_department_query)
        
        for (department_id, department_name) in cursor:
            department_info = Department(department_id=department_id, department_name=department_name)
            department_infomation.append(department_info)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return department_infomation

def get_photo_infomation():
    photo_infomation=[]
    try:
        cnx, cursor = get_db_cursor()
        get_photo_query = ("SELECT photo_id, photo_name FROM ID_photo ORDER BY photo_id DESC LIMIT 1")
        cursor.execute(get_photo_query)
        
        for (now_photo_id, now_photo_name) in cursor:
            new_photo_id = check_new_photo_id(now_photo_id)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return new_photo_id 

# 新規社員情報の追加の際に写真idの取得
def check_new_photo_id(now_photo_id):
    max_number = re.sub("\\D", "", now_photo_id)
    new_number = int(max_number) + 1
    new_number = str(new_number)
    new_photo_id = "P" + new_number.zfill(5)
    return new_photo_id

def delete_employee_info(delete_id):
    cnx, cursor = get_db_cursor()
    delete_query = F"DELETE FROM employee_infomation WHERE id = {delete_id}"
    cursor.execute(delete_query)
    cnx.commit()
    return "削除しました"

# 新規社員情報の追加
def add_new_employee_info(new_employee_id, new_employee_name, new_employee_age, new_gender, new_photo_id, file_name, connect_adress, new_department, update_join_date, update_leave_date):
    cnx, cursor = get_db_cursor()
    add_new_employee_query = F"INSERT INTO employee_infomation (employee_id, employee_name, employee_age, gender, photo_id, adress, department_id, join_date) VALUES ('{new_employee_id}', '{new_employee_name}',{new_employee_age}, '{new_gender}', '{new_photo_id}', '{connect_adress}', '{new_department}', '{update_join_date}')"
    cursor.execute(add_new_employee_query)
    add_new_photo_query = F"INSERT INTO ID_photo (photo_id, photo_name) VALUES ('{new_photo_id}','{file_name.filename}')"
    cursor.execute(add_new_photo_query)
    cnx.commit()

# 退社日の追加
def add_leave_date(update_leave_date, new_employee_id):
    cnx, cursor = get_db_cursor()
    add_leave_date_query = F"UPDATE employee_infomation SET leave_date = '{update_leave_date}' WHERE employee_id = '{new_employee_id}'"
    cursor.execute(add_leave_date_query)
    cnx.commit()

# 新規部署情報追加
def add_department_info(new_department_name):
    try:
        cnx, cursor = get_db_cursor()
        get_department_new_info = ("SELECT * FROM department ORDER BY department_id DESC LIMIT 1")
        cursor.execute(get_department_new_info)

        for (now_department_id, now_department_name) in cursor:
            new_department_id = check_new_department_id(now_department_id)

        add_department_query = F"INSERT INTO department (department_id, department_name) VALUES ('{new_department_id}','{new_department_name}')"
        cursor.execute(add_department_query)
        cnx.commit()
        result_mes = "成功"

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return result_mes

# 新規部署idを決定
def check_new_department_id(department_id):
    max_number = re.sub("\\D", "", department_id)
    new_number = int(max_number) + 1
    
    if int(new_number) <10:
        new_number = "D0" + str(new_number)
    else:
        new_number = "D" + str(new_number)
    
    return new_number

def delete_department_info(delete_department_id):
    cnx, cursor = get_db_cursor()
    delete_query = F"DELETE FROM department WHERE department_id = '{delete_department_id}'"
    cursor.execute(delete_query)
    cnx.commit()
    return "削除"

def fix_department_rename( fix_department_id, department_rename):
    cnx, cursor = get_db_cursor()
    rename_query = F"UPDATE department SET department_name = '{department_rename}' WHERE department_id = '{fix_department_id}'"
    cursor.execute(rename_query)
    cnx.commit()
    return "追加完了"