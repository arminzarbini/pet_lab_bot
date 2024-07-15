import mysql.connector
from config import *


def check_test_group_name(name): #check unique test group name..return as true or false
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name FROM test_group WHERE name=%s;"
    cursor.execute(SQL_Quary, (name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def check_test_group_exists(): #check exist test_group..return as true or fales
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT COUNT(*) FROM test_group;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['COUNT(*)'] == 0

def show_test_group(): #retrun test group data as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT * from test_group;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def check_test_parameter(parameter): #check unique test parameter..return as true or false
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT parameter FROM test WHERE parameter=%s;"
    cursor.execute(SQL_Quary, (parameter, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def show_member_user(): #return member cid user as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT cid FROM user;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['cid'] for i in result]

def show_user_data(cid): #return user information as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT first_name, last_name, username, national_code, phone, address FROM user WHERE cid=%s;"
    cursor.execute(SQL_Quary, (cid, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def check_user_username(username): #check unique username..return as true or false
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT username FROM user WHERE username=%s;"
    cursor.execute(SQL_Quary, (username, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def check_breed_name(name): #check unique breed name..return as true or false
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name FROM breed WHERE name=%s;"
    cursor.execute(SQL_Quary, (name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def show_breed(species): #return breed id and name as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, name FROM breed WHERE species=%s;"
    cursor.execute(SQL_Quary, (species, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_breed_data(id): #return name and specifications as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name as breed_name, specifications from breed WHERE id=%s"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]
    
def show_pet(user_id): #return pet name of user as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT name FROM pet WHERE user_id=%s;"
    cursor.execute(SQL_Quary, (user_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['name'] for i in result]

def show_pet_data(user_id, name): #return pet information as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, gender, birth_date, weight, personality FROM pet WHERE user_id=%s and name=%s;"
    cursor.execute(SQL_Quary, (user_id, name))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def show_pet_id(user_id): #return id(key) and name(value) as dictionary 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id,name FROM pet WHERE user_id=%s"
    cursor.execute(SQL_Quary, (user_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {i['id']:i['name'] for i in result}

def show_test_test_group(test_group_id): #return test id and parameter as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, parameter FROM test WHERE test_group_id=%s;"
    cursor.execute(SQL_Quary, (test_group_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_test_data(id): #return test data as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT * FROM test WHERE id=%s"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def show_test(): #return id and paramater and price as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, parameter, price FROM test;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_reception_id(pet_id): #return last reception id
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id FROM reception WHERE pet_id=%s"
    cursor.execute(SQL_Quary, (pet_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i['id'] for i in result][-1]
 
def calculate_reception_price(reception_id): #calculate tests price of reception
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT test.price
    FROM reception_test
    INNER JOIN test
    ON reception_test.test_id=test.id
    WHERE reception_id=%s;
"""
    cursor.execute(SQL_Quary, (reception_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    total = [i['price'] for i in result]
    return sum(total)

def show_request(): #return reception data without code as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT reception.id, pet.name, user.username, reception.request_date
    FROM reception
    INNER JOIN pet
    ON reception.pet_id=pet.id
    INNER JOIN user
    ON pet.user_id=user.cid
    WHERE reception.code IS NULL;
    ORDER BY reception.request_date DESC;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_reception(): #return reception data with code as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT reception.id, pet.name, user.username, reception.code, reception.reception_date
    FROM reception
    INNER JOIN pet
    ON reception.pet_id=pet.id
    INNER JOIN user
    ON pet.user_id=user.cid
    WHERE reception.code IS NOT NULL
    ORDER BY reception.reception_date DESC;
"""
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_reception_test(reception_id): #return reception_test item as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT reception_test.id, reception_test.test_id, test.parameter
    FROM reception_test
    INNER JOIN test
    ON reception_test.test_id=test.id
    WHERE reception_id=%s;
"""
    cursor.execute(SQL_Quary, (reception_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_reception_data(id): #retrun reception data as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT code, answer_date, is_pay FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def check_reception_code(code): #check unique reception code ..return as true or false
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT code FROM reception WHERE code=%s;"
    cursor.execute(SQL_Quary, (code, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)!=0

def check_reception_test_analyze_date(reception_id): #return longest day of analyze 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT test.analyze_date
    FROM reception_test
    INNER JOIN test
    ON reception_test.test_id=test.id
    WHERE reception_id=%s AND test.analyze_date IS NOT NULL;
"""
    cursor.execute(SQL_Quary, (reception_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len ([i['analyze_date'] for i in result])!=0:
        return max([i['analyze_date'] for i in result])
    
def show_reception_comment(id): #retrun reception comment 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT comment FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['comment']

def show_reception_answer_date(id): #retrun reception answer_date 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT answer_date FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['answer_date']

def show_reception_receipt_image_file_id(id): #retrun receipt_image_file_id
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT receipt_image_file_id FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['receipt_image_file_id']

def show_reception_total_price(id): #return total price
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT total_price FROM reception WHERE id=%s;"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]['total_price']

def show_reception_user(cid): #retrun reception data and pet name as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT reception.id ,reception.code ,reception.reception_date, reception.request_date, pet.name
    FROM reception
    INNER JOIN pet
    ON reception.pet_id=pet.id
    INNER JOIN user
    ON pet.user_id=user.cid
    WHERE user.cid=%s
    ORDER BY reception.reception_date DESC, reception.request_date DESC;
"""
    cursor.execute(SQL_Quary, (cid, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def no_user_username(cid): #check exist username..return as true or fales #ok
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT username FROM user WHERE username IS NOT NULL and cid=%s"
    cursor.execute(SQL_Quary, (cid, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)==0

def show_result_data(reception_test_id): #return result item as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, date as result_date, result_quantity, result_quality, analysis, conclusion FROM result WHERE reception_test_id=%s"
    cursor.execute(SQL_Quary, (reception_test_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def show_test_type_range(id): #return type and minimum_range and maximum range as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT type, minimum_range, maximum_range FROM test WHERE id=%s"
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def show_result_user(reception_test_id): #return result data as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT date, result_quantity, result_quality, analysis, conclusion FROM result WHERE reception_test_id=%s"
    cursor.execute(SQL_Quary, (reception_test_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_all_user_data(): #return all cid and username as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT cid, username FROM user;"
    cursor.execute(SQL_Quary)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_user_all_pet_data(user_id): #return pet id and name as list
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT id, name FROM pet WHERE user_id=%s;"
    cursor.execute(SQL_Quary, (user_id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def show_user_pet_data(id): #return pet data and breed data as dictionary
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = """
    SELECT pet.name as pet_name, breed.name as breed_name, breed.specifications, pet.gender, pet.birth_date, pet.weight, pet.personality
    FROM pet
    INNER JOIN breed
    ON pet.breed_id=breed.id
    WHERE pet.id=%s;
    """
    cursor.execute(SQL_Quary, (id, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result[0]

def get_cid(username): #get cid with username
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    SQL_Quary = "SELECT cid FROM user WHERE username=%s;"
    cursor.execute(SQL_Quary, (username, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result) == 0:
        return False
    else:
        return result[0]['cid']





