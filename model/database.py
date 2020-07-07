import mysql.connector
from mysql.connector import errorcode
from const import DB
from model.item import Item

def get_db_cursor():
    cnx = mysql.connector.connect(
                    user=DB["DB_USER_NAME"],
                    password=DB["DB_PASSWORD"],
                    host=DB["DB_HOST"],
                    database=DB["DB_NAME"])
    return cnx, cnx.cursor()

def get_infomation():
    infomation = []
    try:
        cnx, cursor = get_db_cursor()
        query=("SELECT employee_id, employee_name FROM employee_infomation")
        cursor.execute(query)

        for (employee_id, employee_name) in cursor:
            item = Item(employee_id, employee_name)
            infomation.append(item)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        # DB切断
        cnx.close()
    
    return infomation