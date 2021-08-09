CREATE TABLE package (
	id numeric PRIMARY KEY,
	length numeric NOT NULL,
	date TIMESTAMP NOT NULL
);

CREATE TABLE segment (
	id numeric PRIMARY KEY,
	package_id numeric,
	date TIMESTAMP NOT NULL,
	microsec numeric,
	rate numeric,
	flag1 text,
	flag2 text,
	flag3 text,
	flag4 text,
	
	FOREIGN KEY (package_id) 
		REFERENCES package(id)
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE measurement (
	payload_uuid UUID NOT NULL DEFAULT uuid_generate_v1(),
	segment_id numeric,
	package_id numeric,
	date TIMESTAMP NOT NULL,
	distance numeric,
	
	PRIMARY KEY (payload_uuid),
	FOREIGN KEY (segment_id) 
		REFERENCES segment(id),
	FOREIGN KEY (package_id) 
		REFERENCES package(id)
);

CREATE TABLE measurement (
	payload_uuid UUID NOT NULL DEFAULT uuid_generate_v1(),
	segment_id numeric,
	package_id numeric,
	date TIMESTAMP NOT NULL,
	-- replace here the columns for your use case
	position numeric,
	temperature numeric,
	
	-- this should not be replaced
	PRIMARY KEY (payload_uuid),
	FOREIGN KEY (segment_id) 
		REFERENCES segment(id),
	FOREIGN KEY (package_id) 
		REFERENCES package(id)
);
