create table meta.student(
	srn char(10) not null,
	batch timestamp not null
) inherits (meta.person);

-- TODO: major, degree
create table active.student(
	guardian serial not null,
	year int not null,
	roll int not null,
	foreign key(guardian) references meta.person(id)
) inherits (meta.student);