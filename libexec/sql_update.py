#!usr/bin/python
#coding=utf-8
import sys
import os
import MySQLdb
import getopt

DBHOST = "localhost"
DBNAME = "resolver"
DBUSER = "remote"
DBPASSWD = "remote"
TABLENAME = "open_resolver"
TIME = ""
def ManualAdd(inputfile):
	isExists = os.path.exists(inputfile)
	if not isExists:
		print inputfile+" is not exist!"
		return
	f = open(inputfile)
	data = f.readlines()
	f.close()
	try:
		conn = MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASSWD,db=DBNAME)
	except MySQLdb.Error,e:
	 	print "connection failed!"
	 	return
	cur = conn.cursor()
	for line in data:
		ip = line.strip()
		InsertData(ip,cur,2)
	print "Update database finished!"
	cur.close()
	conn.commit()
	conn.close()


def InsertData(ip_line,cur,flag):
	global TIME
	global TABLENAME
	ip,status = ip_line.split('\t')
	find = 0
	total = 0
	percent = 0.0
	comments = "Open Resolver Discovery"
	if flag == 2:
		comments = status
		status = ""
	try:
		count = cur.execute("select find,total,percent from %s where IP='%s'" % (TABLENAME,ip))
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
			cur.execute("insert into %s values(0,'%s','%s','%s',%d,%d,%f,'%s','%s')" % (TABLENAME,ip,TIME,TIME,find,total,percent,status,comments))
		except MySQLdb.Error,e:
	 		print "insert %s failed!" % ip
	 		return
		print "insert %s success!" % ip
		return
	if flag == 2:  #match ManualAdd()
		return
	result = cur.fetchone()
	find = int(result[0])+1
	total = int(result[1])+1
	if flag == 1: #match maintain mode
		total = total-1
	percent = float(find)/float(total)
	try:
		cur.execute("update %s set last_time='%s',find=%d,total=%d,percent=%f,status='%s' where IP='%s'" % (TABLENAME,TIME,find,total,percent,status,ip))
	except MySQLdb.Error,e:
	 	print "update %s failed!" % ip
	 	return

def Usage():
	print '''
Usage:
\t-h\t\tprint Usage()
\t-t\t\tinput updated time with format %Y%m%d default ""
\t--main [filename]\tuse when the main.sh script invoked and filename must be input, which the file has saved only IP
\t--maintain [filename]\tuse when the maintain.sh script invoked and filename must be input, which the file has saved only IP
\t--manual-add [filename]\tuse when need to add some items saved in filename with format IP\\tcomments
\t--help\t\tprint Usage()
	'''

def main(argv):
	global DBNAME
	global TIME
	flag = 0
	TIME = 0
	inputfile = ""
	try:
		opts,args = getopt.getopt(argv[1:], "t:h",["main=","maintain=","manual-add=","help"])
	except getopt.GetoptError,info:
		print info.msg
		Usage()
		sys.exit()
	for option,value in opts:
		if option in ('-t'):
			TIME = value
		elif option in ('-h'):
			Usage()
			sys.exit()
		else:
			pass
	for option,value in opts:
	  	if option in ("--main"):
	  		flag = 0
	  		inputfile = value
	  	elif option in ("--maintain"):
	  		flag = 1
	  		inputfile = value
	  	elif option in ("--manual-add"):
	  		ManualAdd(value)
	  		sys.exit()
	  	elif option in ("--help"):
	  		Usage()
	  		sys.exit()
	  	else:
			pass
	f = open(inputfile)
	data = f.readlines()
	f.close()
	try:
		conn = MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASSWD,db=DBNAME)
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
	main(sys.argv)
