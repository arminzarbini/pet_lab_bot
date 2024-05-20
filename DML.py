import mysql.connector
from config import *


def insert_test_group_data(name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO test_group (name) VALUES (%s);
    """
    cursor.execute(SQL_Quary, (name, ))
    cursor.close()
    conn.commit()
    conn.close()


def insert_test_data(test_group_id, parameter, type, price, unit=None, minimum_range=None, maximum_range=None, analyze_date=None, description=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO test (test_group_id, parameter, type, price, unit, minimum_range, maximum_range, analyze_date, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(SQL_Quary, (test_group_id, parameter, type, price, unit, minimum_range, maximum_range, analyze_date, description))
    cursor.close()
    conn.commit()
    conn.close()


def insert_user_data(cid, first_name, last_name=None, username=None, national_code=None, phone=None, address=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO user (cid, first_name, last_name, username, national_code, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(SQL_Quary, (cid, first_name, last_name, username, national_code, phone, address))
    cursor.close()
    conn.commit()
    conn.close()

def edit_user_first_name(first_name, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    UPDATE user SET first_name=%s WHERE cid=%s
"""
    cursor.execute(SQL_Quary, (first_name, cid))
    cursor.close()
    conn.commit()
    conn.close()


def edit_user_last_name(last_name, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    UPDATE user SET last_name=%s WHERE cid=%s
"""
    cursor.execute(SQL_Quary, (last_name, cid))
    cursor.close()
    conn.commit()
    conn.close()


def edit_user_username(username, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    UPDATE user SET username=%s WHERE cid=%s
"""
    cursor.execute(SQL_Quary, (username, cid))
    cursor.close()
    conn.commit()
    conn.close()

def edit_user_national_code(national_code, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    UPDATE user SET national_code=%s WHERE cid=%s
"""
    cursor.execute(SQL_Quary, (national_code, cid))
    cursor.close()
    conn.commit()
    conn.close()









def inesrt_payment_data(user_id, ammount):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO payment (user_id, ammount) VALUES (%s, %s);
    """
    cursor.execute(SQL_Quary, (user_id, ammount))
    cursor.close()
    conn.commit()
    conn.close()


def insert_species_data(name):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO species (name) VALUES (%s);
    """
    cursor.execute(SQL_Quary, (name, ))
    cursor.close()
    conn.commit()
    conn.close()


def insert_breed_data(species_id, name, specifications=None):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO breed (species_id, name, specifications) VALUES (%s, %s, %s);
    """
    cursor.execute(SQL_Quary, (species_id, name, specifications))
    cursor.close()
    conn.commit()
    conn.close()


def insert_vet_data(user_id, breed_id, name, gender=None, age=None, weight=None, personality=None):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO vet (user_id, breed_id, name, gender, age, weight, personality) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(SQL_Quary, (user_id, breed_id, name, gender, age, weight, personality))
    cursor.close()
    conn.commit()
    conn.close()





def insert_reception_data(vet_id, code=None, reception_date=None, Sampling_date=None, answer_date=None, comment=None, is_pay=None):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO reception(vet_id, code, reception_date, Sampling_date, answer_date, comment, is_pay) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(SQL_Quary, (vet_id, code, reception_date, Sampling_date, answer_date, comment, is_pay))
    cursor.close()
    conn.commit()
    conn.close()


def insert_reception_test_data(reception_id, test_id):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO reception_test(reception_id, test_id) VALUES (%s, %s);
    """
    cursor.execute(SQL_Quary, (reception_id, test_id))
    cursor.close()
    conn.commit()
    conn.close()



def insert_result_data(reception_test_id, result_quantity=None, result_quality=None, analysis=None, conclusion=None):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO result (reception_test_id, result_quantity, result_quality, analysis, conclusion) VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(SQL_Quary, (reception_test_id, result_quantity, result_quality, analysis, conclusion))
    cursor.close()
    conn.commit()
    conn.close()


