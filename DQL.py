import mysql.connector
from config import *



def show_test_group():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT * FROM test_group;
    """
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result



def show_test_parameter():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT parameter FROM test;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def show_member_user_cid():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT cid FROM user;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def show_user_data(cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT * FROM user WHERE cid=%s;
"""
    cursor.execute(SQL_Quary, (cid, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_user_username():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT username FROM user;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_species():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT * FROM species;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_breed():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT * FROM breed;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
