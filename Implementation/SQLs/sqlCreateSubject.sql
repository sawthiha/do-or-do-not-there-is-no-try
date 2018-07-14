create table meta.subject(
	id serial,
	code char(10) not null,
	name varchar(50) not null,
	description text,

	primary key(id)
);