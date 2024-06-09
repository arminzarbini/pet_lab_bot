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
    SQL_Quary = "SELECT parameter FROM test WHERE paramshow_member_usereter=%s;"
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
    SQL_Quary = "SELECT first_name, last_name, username, national_code, phone, address FROM user WHERE cid=%s LIMIT 1;"
    cursor.execute(SQL_Quary, (cid, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

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
    SQL_Quary = "SELECT id, name FROM breed WHERE species=%s;"
    cursor.execute(SQL_Quary, (species, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {i['id']:i['name'] for i in result}
    
def show_pet(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name FROM pet WHERE user_id=%s;"
    cursor.execute(SQL_Quary, (user_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['name'] for i in result]

def show_pet_data(user_id, name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, gender, birth_date, weight, personality FROM pet WHERE user_id=%s and name=%s;"
    cursor.execute(SQL_Quary, (user_id, name))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def show_pet_id(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id,name FROM pet WHERE user_id=%s"
    cursor.execute(SQL_Quary, (user_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {i['id']:i['name'] for i in result}

def show_test():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, parameter, price FROM test;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_reception(pet_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id FROM reception WHERE pet_id=%s"
    cursor.execute(SQL_Quary, (pet_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['id'] for i in result][-1]

def show_reception_request():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT reception.id, pet.name, user.username, reception.request_date 
    FROM reception 
    INNER JOIN pet
    ON reception.pet_id=pet.id
    INNER JOIN user
    ON pet.user_id=user.cid
    ORDER BY reception.request_date DESC;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_reception_test(reception_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT test.parameter
    FROM reception_test
    INNER JOIN test
    ON reception_test.test_id=test.id
    WHERE reception_id=%s;
"""
    cursor.execute(SQL_Quary, (reception_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['parameter'] for i in result]

def show_reception_data(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT code, sampling_date, answer_date, is_pay FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def check_reception_code_exist(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT code FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['code']!=None


def check_reception_code(code):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT code FROM reception WHERE code=%s;"
    cursor.execute(SQL_Quary, (code, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

