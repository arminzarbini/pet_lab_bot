import mysql.connector
from config import *


def check_test_group_name(name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name FROM test_group WHERE name=%s;"
    cursor.execute(SQL_Quary, (name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def check_test_group_exists():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT COUNT(*) FROM test_group;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['COUNT(*)'] == 0

def show_test_group():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT * from test_group;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def check_test_parameter(parameter):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT parameter FROM test WHERE parameter=%s;"
    cursor.execute(SQL_Quary, (parameter, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def show_member_user():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT cid FROM user;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['cid'] for i in result]

def show_user_data(cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT * FROM user WHERE cid=%s;"
    cursor.execute(SQL_Quary, (cid, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def check_user_username(username):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT username FROM user WHERE username=%s;"
    cursor.execute(SQL_Quary, (username, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def check_breed_name(name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name FROM breed WHERE name=%s;"
    cursor.execute(SQL_Quary, (name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def show_breed_name(species):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, name FROM breed WHERE species=%s"
    cursor.execute(SQL_Quary, (species, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {i['id']:i['name'] for i in result}
    