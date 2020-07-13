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
        
        for (department_name, department_id) in cursor:
            department_info = Department(department_name=department_name,department_id=department_id)
            department_infomation.append(department_info)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return department_infomation

def delete_employee_info(delete_id):
    cnx, cursor = get_db_cursor()
    delete_query = F"DELETE FROM employee_infomation WHERE id = {delete_id}"
    cursor.execute(delete_query)
    return "削除しました"

# 新規部署情報追加
def add_department_info(new_department_name):
    department_new_infomation=[]

    try:
        cnx, cursor = get_db_cursor()
        get_department_new_info = ("SELECT * FROM department ORDER BY department_id DESC LIMIT 1")
        cursor.execute(get_department_new_info)

        for (department_id, department_name) in cursor:
            department_new_info = Department(department_name=department_name,department_id=department_id)
            department_new_infomation.append(department_new_info)

        new_department_id = check_new_department_id(department_id)
        add_department_query = F"INSERT INTO department (department_id, department_name) VALUES ({new_department_id},'{new_department_name}')"
        cursor.execute(add_department_query)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()

# 新規部署idを決定
def check_new_department_id(department_id):
    max_number = re.sub("\\D", "", department_id)
    new_number = int(max_number) + 1
    
    if new_number <10:
        new_number = "0" + str(new_number)
    
    return new_number