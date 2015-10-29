#!usr/bin/python
#coding=utf-8
import sys
import os
import MySQLdb
import time

dbname = "resolver"
tablename = "open_resolver"
init_status = "NULL"

def ExtractorIP(cur):
	data = []
	try:
		count = cur.execute("select IP from %s " % tablename)
	except MySQLdb.Error,e:
	 	print "extractor ip from  %s failed!" % tablename
	 	return([])

	data = cur.fetchall()
	try:
		count = cur.execute("update %s set total=total+1,status='%s'" % (tablename,init_status))
	except MySQLdb.Error,e:
	 	print "init total and status from %s failed!" % tablename
	 	return([])
	return(data)

def main():
	global dbname
	outputfile = sys.argv[1]
#	outputfile = "/tmp/tempiplist"
	try:
		conn = MySQLdb.connect(host='localhost',user='remote',passwd='remote',db=dbname)
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
