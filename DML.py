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

def edit_test_group_name(name, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test_group SET name=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (name, id))
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

def edit_test_parameter(parameter, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET parameter=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (parameter, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_type(type, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET type=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (type, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_price(price, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET price=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (price, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_unit(unit, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET unit=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (unit, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_minimum_range(minimum_range, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET minimum_range=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (minimum_range, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_maximum_range(maximum_range, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET maximum_range=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (maximum_range, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_analyze_date(analyze_date, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET analyze_date=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (analyze_date, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_test_description(description, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE test SET description=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (description, id))
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

def edit_breed_name(name, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE breed SET name=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (name, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_breed_specifications(specifications, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE breed SET specifications=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (specifications, id))
    cursor.close()
    conn.commit()
    conn.close()

def insert_pet_data(user_id, breed_id, name, gender=None, birth_date=None, weight=None, personality=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO pet (user_id, breed_id, name, gender, birth_date, weight, personality) VALUES (%s, %s, %s, %s, %s, %s, %s);"
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

def insert_reception_data(pet_id, code=None, reception_date=None, answer_date=None, comment=None, receipt_image_file_id=None, is_pay=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT INTO RECEPTION (pet_id, code, reception_date, answer_date, comment,receipt_image_file_id, is_pay) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(SQL_Quary, (pet_id, code, reception_date, answer_date, comment, receipt_image_file_id, is_pay))
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

def edit_reception_code_date(code, reception_date, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE reception SET code=%s, reception_date=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (code, reception_date, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_reception_answer_date(answer_date, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE reception SET answer_date=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (answer_date, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_reception_receipt_image_file_id(receipt_image_file_id, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE reception SET receipt_image_file_id=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (receipt_image_file_id, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_reception_total_price(total_price, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE reception SET total_price=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (total_price, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_reception_is_pay(is_pay, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE reception SET is_pay=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (is_pay, id))
    cursor.close()
    conn.commit()
    conn.close()

def insert_result_data(reception_test_id, result_quantity=None, result_quality=None, analysis=None, conclusion=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "INSERT IGNORE INTO result (reception_test_id, result_quantity, result_quality, analysis, conclusion) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(SQL_Quary, (reception_test_id, result_quantity, result_quality, analysis, conclusion))
    cursor.close()
    conn.commit()
    conn.close()

def edit_result_date(result_date, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE result SET date=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (result_date, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_result_quantity(result_quantity, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE result SET result_quantity=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (result_quantity, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_result_analysis(analysis, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE result SET analysis=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (analysis, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_result_quality(result_quality, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE result SET result_quality=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (result_quality, id))
    cursor.close()
    conn.commit()
    conn.close()

def edit_result_conclusion(conclusion, id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = "UPDATE result SET conclusion=%s WHERE id=%s;"
    cursor.execute(SQL_Quary, (conclusion, id))
    cursor.close()
    conn.commit()
    conn.close()