create schema train;

create table train.evaluation  (
	id serial,
	student serial not null,
	score int not null,

	primary key(id),
	foreign key(student) references meta.student(id)
);

create table train.attend<Subject>(like train.evaluation);
create table train.commend<Subject>(like train.evaluation);
create table train.final<Subject>(like train.evaluation);
create table train.external<Subject>(
	like train.evaluation,
	host varchar(50) not null
);