import mysql.connector
from mysql.connector import errorcode
from model.const import DB
from model.item import Item

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
        query=("SELECT employee_id, employee_name FROM employee_infomation")
        cursor.execute(query)

        for (employee_id, employee_name) in cursor:
            item = Item(employee_id, employee_name)
            employee_infomation.append(item)

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
            department_info = Item(department_id, department_name)
            department_infomation.append(department_info)

    except mysql.connector.Error as err:
        printerror(err)
    else:
        cnx.close()
    
    return department_infomation