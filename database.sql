create table user(
    	cid BIGINT NOT NULL,
    	first_name VARCHAR(64) NOT NULL,
    	last_name VARCHAR(64),
    	username VARCHAR(32),
    	national_code CHAR(10),
    	phone VARCHAR(15),
    	address TINYTEXT,
    	PRIMARY KEY (cid),
    	UNIQUE (username));

create table breed(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, 
    	species ENUM('cat', 'dog', 'bird', 'rabbit', 'rat', 'other') NOT NULL,
    	name VARCHAR(45) NOT NULL,
    	specifications TINYTEXT,
    	PRIMARY KEY (id),
    	UNIQUE (name));

create table pet(
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
    	FOREIGN KEY (breed_id) REFERENCES breed(id));

create table test_group(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    	name VARCHAR(45) NOT NULL,
    	PRIMARY KEY (id),
    	UNIQUE (name));

create table test(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    	test_group_id SMALLINT UNSIGNED NOT NULL,
    	parameter VARCHAR(45) NOT NULL,
    	type ENUM('quantity', 'quality') NOT NULL,
    	price DECIMAL NOT NULL,
    	unit VARCHAR(10),
    	minimum_range DECIMAL(8,3),
    	maximum_range DECIMAL(8,3),
    	analyze_date tinyint(30),
    	description TINYTEXT,
    	PRIMARY KEY (id),
    	FOREIGN KEY (test_group_id) REFERENCES test_group(id),
    	UNIQUE (parameter));

create table reception(
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

create table reception_test(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	reception_id SMALLINT UNSIGNED NOT NULL,
	test_id SMALLINT UNSIGNED NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (reception_id) REFERENCES reception(id),
	FOREIGN KEY (test_id) REFERENCES test(id));

create table result(
    	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	reception_test_id INT UNSIGNED NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,
	result_quantity DECIMAL(8,3),
	result_quality ENUM('negative', 'positive'),
	analysis ENUM('high','low','normal'),
	conclusion TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (reception_test_id) REFERENCES reception_test(id),
    	UNIQUE (reception_test_id));
	





	
	



		
	