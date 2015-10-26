#!/bin/sh
dbname="resolver";
tablename="open_resolver";
mysql -u root -plbr <<EOF
create database if not exists $dbname;
use $dbname;
create table if not exists $tablename(
	ID int AUTO_INCREMENT primary key,
	IP char(16),
	first_time char(30),
	last_time char(30),
	find int unsigned default 0,
	total int unsigned default 0,
	percent float default 0,
	state tinyint(1) unsigned default 0,
	comment char(30)
	);
grant all on $dbname.* to remote@'%' identified by "remote";
flush privileges;

EOF
