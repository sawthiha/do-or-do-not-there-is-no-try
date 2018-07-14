create table meta.person(
	id serial,
	nrc char(18) not null,
	name char(80) not null,
	phone char(20),
	address varchar(255) not null,
	primary key(id)
);