#!/bin/sh
#must running at sql-server end
DBROOTUSER="root"
DBROOTPASSWD="lbr"
#读取配置文件
CONF_PATH="../etc/program.conf"
DBHOST=`grep ^DBHOST $CONF_PATH | awk '{print $3}'`
DBNAME=`grep ^DBNAME $CONF_PATH | awk '{print $3}'`
DBUSER=`grep ^DBUSER $CONF_PATH | awk '{print $3}'`
DBPASSWD=`grep ^DBPASSWD $CONF_PATH | awk '{print $3}'`
TABLENAME=`grep ^TABLENAME $CONF_PATH | awk '{print $3}'`
mysql -u $DBROOTUSER -p$DBROOTPASSWD -h $DBHOST <<EOF
create database if not exists $DBNAME;
use $DBNAME;
create table if not exists $TABLENAME(
	ID int AUTO_INCREMENT primary key,
	IP char(16),
	first_time char(30),
	last_time char(30),
	find int unsigned default 0,
	total int unsigned default 0,
	percent float default 0,
	status char(30) default "NULL",
	comment char(30)
	);
grant all on $DBNAME.* to $DBUSER@'%' identified by "$DBPASSWD";
flush privileges;

EOF
