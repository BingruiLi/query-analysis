#!usr/bin/python
#coding=utf-8
import sys
import os
import MySQLdb
import time

CONF_PATH = "../etc/program.conf"
DBHOST = ""
DBNAME = ""
DBUSER = ""
DBPASSWD = ""
TABLENAME = ""
init_status = "NULL"

def ConfRead():
	global DBHOST
	global DBNAME
	global DBUSER
	global DBPASSWD
	global TABLENAME
	isExists = os.path.exists(CONF_PATH)
	if not isExists:
		print "CONF_PATH doesn't exists!\nquit now"
		sys.exit()
	DBHOST = os.popen("grep ^DBHOST %s | awk '{print $3}'" % CONF_PATH).read().strip()
	DBNAME = os.popen("grep ^DBNAME %s | awk '{print $3}'" % CONF_PATH).read().strip()
	DBUSER = os.popen("grep ^DBUSER %s | awk '{print $3}'" % CONF_PATH).read().strip()
	DBPASSWD = os.popen("grep ^DBPASSWD %s | awk '{print $3}'" % CONF_PATH).read().strip()
	TABLENAME = os.popen("grep ^TABLENAME %s | awk '{print $3}'" % CONF_PATH).read().strip()
	if DBHOST=="" or DBNAME=="" or DBUSER=="" or DBPASSWD=="" or TABLENAME=="":
		print "Read configure file failured!\nquit now"
		sys.exit()

def ExtractorIP(cur):
	data = []
	try:
		count = cur.execute("select IP from %s " % TABLENAME)
	except MySQLdb.Error,e:
	 	print "extractor ip from  %s failed!" % TABLENAME
	 	return([])

	data = cur.fetchall()
##### comment total+1 codes
#	try:
#		count = cur.execute("update %s set total=total+1, percent=find/total,status='%s'" % (TABLENAME,init_status))
#	except MySQLdb.Error,e:
#	 	print "init total and status from %s failed!" % TABLENAME
#	 	return([])
##### 
	return(data)


def main():
	ConfRead()
	outputfile = sys.argv[1]
#	outputfile = "/tmp/tempiplist"
	try:
		conn = MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASSWD,db=DBNAME)
	except MySQLdb.Error,e:
	 	print "connection failed!"
	 	return
	cur = conn.cursor()
	data = ExtractorIP(cur)
	if data == []:
		return
	
	f = open(outputfile,'w')
	for ip in data:
		f.write(ip[0]+"\n")
	f.close()
	print "Extractor data finished!"
	cur.close()
	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()
