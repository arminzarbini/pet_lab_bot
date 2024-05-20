create table user(
	cid BIGINT NOT NULL,
	first_name VARCHAR(64) NOT NULL,
	last_name VARCHAR(64),
	username VARCHAR(32),
	national_code CHAR(10),
	phone VARCHAR(15),
	address TINYTEXT,
	PRIMARY KEY (cid));

create table payment(
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
	user_id BIGINT NOT NULL,
	ammount DECIMAL(10,2) NOT NULL,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES user(cid));

create table species(
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(45) NOT NULL,
	PRIMARY KEY (id));

create table breed(
	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, 
	species_id SMALLINT UNSIGNED NOT NULL,
	name VARCHAR(45) NOT NULL,
	specifications TINYTEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (species_id) REFERENCES species(id));

create table pet(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    	user_id BIGINT NOT NULL,
	breed_id SMALLINT UNSIGNED NOT NULL,
    	name varchar(45) not null,
    	gender ENUM('male', 'female'),
    	age TINYINT UNSIGNED,
    	weight DECIMAL(3,1),
    	personality TINYTEXT,
    	PRIMARY KEY (id),
    	FOREIGN KEY (user_id) REFERENCES user(cid),
    	FOREIGN KEY (breed_id) REFERENCES breed(id));

create table test_group(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    	name VARCHAR(45) NOT NULL,
    	PRIMARY KEY (id));

create table test(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    	test_group_id SMALLINT UNSIGNED NOT NULL,
    	parameter VARCHAR(45) NOT NULL,
    	type ENUM('quantity', 'quality') NOT NULL,
    	price DECIMAL(10,2) NOT NULL,
    	unit VARCHAR(10),
    	minimum_range DECIMAL(5,3),
	maximum_range DECIMAL(5,3),
    	analyze_date tinyint(30),
    	description TINYTEXT,
    	PRIMARY KEY (id),
    	FOREIGN KEY (test_group_id) REFERENCES test_group(id));

create table reception(
    	id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
	pet_id SMALLINT UNSIGNED NOT NULL,
	code CHAR(5),
	request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	reception_date DATETIME,
	sampling_date DATETIME,
	answer_date DATE,
	comment TINYTEXT,
	is_pay TINYINT(1) DEFAULT 0,
	PRIMARY KEY (id),
	FOREIGN KEY (pet_id) REFERENCES pet(id));

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
	result_quantity DECIMAL(5,3),
	result_quality ENUM('negative', 'positive'),
	analysis ENUM('high','low','normal'),
	conclusion TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (reception_test_id) REFERENCES reception_test(id));

	





	
	



		
	