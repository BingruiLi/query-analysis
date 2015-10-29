#!usr/bin/python
#coding=utf-8
import sys
import os
import MySQLdb

dbname = "resolver"
tablename = "open_resolver"
time = ""
def InsertData(ip_line,cur,flag):
	global time
	global tablename
	ip,status = ip_line.split(' ')
	find = 0
	total = 0
	percent = 0.0
	try:
		count = cur.execute("select find,total,percent from %s where IP='%s'" % (tablename,ip))
	except MySQLdb.Error,e:
	 	print "select %s failed!" % ip
	 	return
	if count > 1:
		print "select %s return more than one results"
		return
	elif count == 0:
		find = 1
		total = 1
		percent = 1.0
		try:
			cur.execute("insert into %s values(0,'%s','%s','%s',%d,%d,%f,'%s','%s')" % (tablename,ip,time,time,find,total,percent,status,"Open Resolver Discovery"))
		except MySQLdb.Error,e:
	 		print "insert %s failed!" % ip
	 		return
		print "insert %s success!" % ip
		return
	result = cur.fetchone()
	find = int(result[0])+1
	total = int(result[1])+1
	if flag == 1:
		total = total-1
	percent = float(find)/float(total)
	try:
		cur.execute("update %s set last_time='%s',find=%d,total=%d,percent=%f,status='%s' where IP='%s'" % (tablename,time,find,total,percent,status,ip))
	except MySQLdb.Error,e:
	 	print "update %s failed!" % ip
	 	return

def main():
	global dbname
	global time

	flag = 0
	inputfile = sys.argv[1]
	time = sys.argv[2]
	if "maintain"==sys.argv[3]:
		flag = 1
	f = open(inputfile)
	data = f.readlines()
	f.close()
	try:
		conn = MySQLdb.connect(host='localhost',user='remote',passwd='remote',db=dbname)
	except MySQLdb.Error,e:
	 	print "connection failed!"
	 	return
	cur = conn.cursor()
	for line in data:
		ip = line.strip()
		InsertData(ip,cur,flag)
	print "Update database finished!"
	cur.close()
	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()
