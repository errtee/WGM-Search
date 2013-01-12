drop table if exists person;
create table entries (
	  id integer primary key autoincrement,
	  name string,
	  zip string not null,
	  city string
);

