drop table if exists person;
create table person (
  id integer primary key autoincrement,
  name text not null
);

drop table if exists match;
create table match (
  id integer primary key autoincrement
);

drop table if exists gamer;
create table gamer (
  id integer primary key autoincrement,
  userid integer,
  matchid integer,
  sessionid integer,
  foreign key(userid) references person(id),
  foreign key(matchid) references match(id)
);

