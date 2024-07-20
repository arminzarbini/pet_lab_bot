import mysql.connector
from config import *

def create_database():
    conn = mysql.connector.connect(user=db_user, password=db_password, host='localhost')
    cursor = conn.cursor()
    SQL_Quary = f"CREATE DATABASE IF NOT EXISTS {db_name}"
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_user_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS user (
    cid BIGINT NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64),
    username VARCHAR(32),
    national_code CHAR(10),
    phone VARCHAR(15),
    address TINYTEXT,
    PRIMARY KEY (cid),
    UNIQUE (username)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_breed_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS breed (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, 
    species ENUM('cat', 'dog', 'bird', 'rabbit', 'rat', 'other') NOT NULL,
    name VARCHAR(45) NOT NULL,
    specifications TINYTEXT,
    PRIMARY KEY (id),
    UNIQUE (name)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_pet_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS pet (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    breed_id SMALLINT UNSIGNED NOT NULL,
    name varchar(45) not null,
    gender ENUM('male', 'female'),
    birth_date DATE,
    weight DECIMAL(6,3),
    personality TINYTEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(cid),
    FOREIGN KEY (breed_id) REFERENCES breed(id)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_test_group_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS test_group (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(45) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_test_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS test (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    test_group_id SMALLINT UNSIGNED NOT NULL,
    parameter VARCHAR(45) NOT NULL,
    type ENUM('quantity', 'quality') NOT NULL,
    price DECIMAL NOT NULL,
    unit VARCHAR(10),
    minimum_range DECIMAL(8,3),
	maximum_range DECIMAL(8,3),
    analyze_date tinyint,
    description TINYTEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (test_group_id) REFERENCES test_group(id),
    UNIQUE (parameter)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_reception_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS reception (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
	pet_id SMALLINT UNSIGNED NOT NULL,
	code CHAR(5),
	request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	reception_date DATETIME,
	answer_date DATE,
    total_price DECIMAL,
	comment TINYTEXT,
    receipt_image_file_id VARCHAR(100),
	is_pay TINYINT(1) DEFAULT 0,
	PRIMARY KEY (id),
	FOREIGN KEY (pet_id) REFERENCES pet(id),
    UNIQUE (code)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_reception_test_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS reception_test (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	reception_id SMALLINT UNSIGNED NOT NULL,
	test_id SMALLINT UNSIGNED NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (reception_id) REFERENCES reception(id),
	FOREIGN KEY (test_id) REFERENCES test(id)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()

def create_result_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    SQL_Quary = """
    CREATE TABLE IF NOT EXISTS result (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	reception_test_id INT UNSIGNED NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,
	result_quantity DECIMAL(8,3),
	result_quality ENUM('negative', 'positive'),
	analysis ENUM('high','low','normal'),
	conclusion TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (reception_test_id) REFERENCES reception_test(id),
    UNIQUE (reception_test_id)
    );
    """
    cursor.execute(SQL_Quary)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
    create_user_table()
    create_breed_table()
    create_pet_table()
    create_test_group_table()
    create_test_table()
    create_reception_table()
    create_reception_test_table()
    create_result_table()