import mysql.connector
from config import *


def insert_test_group_data(name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO test_group (name) VALUES (%s);"
    cursor.execute(SQL_Quary, (name, ))
    cursor.close()
    conn.commit()
    conn.close()

def insert_test_data(test_group_id, parameter, type, price, unit=None, minimum_range=None, maximum_range=None, analyze_date=None, description=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO test (test_group_id, parameter, type, price, unit, minimum_range, maximum_range, analyze_date, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(SQL_Quary, (test_group_id, parameter, type, price, unit, minimum_range, maximum_range, analyze_date, description))
    cursor.close()
    conn.commit()
    conn.close()

def insert_user_data(cid, first_name, last_name=None, username=None, national_code=None, phone=None, address=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO user (cid, first_name, last_name, username, national_code, phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(SQL_Quary, (cid, first_name, last_name, username, national_code, phone, address))
    cursor.close()
    conn.commit()
    conn.close()

def edit_user_first_name(first_name, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE user SET first_name=%s WHERE cid=%s;"
    cursor.execute(SQL_Quary, (first_name, cid))
    cursor.close()
    conn.commit()
    conn.close()

def edit_user_last_name(last_name, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE user SET last_name=%s WHERE cid=%s;"
    cursor.execute(SQL_Quary, (last_name, cid))
    cursor.close()
    conn.commit()
    conn.close()

def edit_user_username(username, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE user SET username=%s WHERE cid=%s;"
    cursor.execute(SQL_Quary, (username, cid))
    cursor.close()
    conn.commit()
    conn.close()

def edit_user_national_code(national_code, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE user SET national_code=%s WHERE cid=%s;"
    cursor.execute(SQL_Quary, (national_code, cid))
    cursor.close()
    conn.commit()
    conn.close()

def edit_phone(phone, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE user SET phone=%s WHERE cid=%s;"
    cursor.execute(SQL_Quary, (phone,cid))
    cursor.close()
    conn.commit()
    conn.close()

def edit_address(address, cid):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE user SET address=%s WHERE cid=%s;"
    cursor.execute(SQL_Quary, (address, cid))
    cursor.close()
    conn.commit()
    conn.close()

def insert_breed_data(species, name, specifications=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO breed (species, name, specifications) VALUES (%s, %s, %s);"
    cursor.execute(SQL_Quary, (species, name, specifications))
    cursor.close()
    conn.commit()
    conn.close()

def insert_pet_data(user_id, breed_id, name, gender=None, birth_date=None, weight=None, personality=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    INSERT INTO pet (user_id, breed_id, name, gender, birth_date, weight, personality) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(SQL_Quary, (user_id, breed_id, name, gender, birth_date, weight, personality))
    cursor.close()
    conn.commit()
    conn.close()

def edit_pet_gender(gender, user_id, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE pet SET gender=%s WHERE user_id=%s and id=%s;"
    cursor.execute(SQL_Quary, (gender, user_id, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_pet_birth_date(birh_date, user_id, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE pet SET birth_date=%s WHERE user_id=%s and id=%s;"
    cursor.execute(SQL_Quary, (birh_date, user_id, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_pet_weight(weight, user_id, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE pet SET weight=%s WHERE user_id=%s and id=%s;"
    cursor.execute(SQL_Quary, (weight, user_id, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_pet_personality(personality, user_id, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE pet SET personality=%s WHERE user_id=%s and id=%s;"
    cursor.execute(SQL_Quary, (personality, user_id, id))
    cursor.close()
    conn.commit()
    conn.close()

def insert_reception_data(pet_id, code=None, reception_date=None, sampling_date=None, answer_date=None, comment=None, is_pay=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO RECEPTION (pet_id, code, reception_date, sampling_date, answer_date, comment, is_pay) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(SQL_Quary, (pet_id, code, reception_date, sampling_date, answer_date, comment, is_pay))
    cursor.close()
    conn.commit()
    conn.close()

def insert_reception_test_data(reception_id, test_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO reception_test(reception_id, test_id) VALUES (%s, %s);"
    cursor.execute(SQL_Quary, (reception_id, test_id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_reception_code(code, reception_date, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE reception SET code=%s, reception_date=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (code, reception_date, id))
    cursor.close()
    conn.commit()
    conn.close()







def inesrt_payment_data(user_id, ammount):
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost', database=db_name)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO payment (user_id, ammount) VALUES (%s, %s);"
    cursor.execute(SQL_Quary, (user_id, ammount))
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


