#!usr/bin/python
import os
import sys
import time
import threading
import MySQLdb
import re

Thread_MAX = 100
fqdn = "www.baidu.com A"

count = 0
find = 0
logpath = ""
datapath = ""
ippath = ""
lock = threading.RLock()


def Log(string):
	lock.acquire()
	fw = open(logpath,'a')
	fw.write(string+'\n')
	fw.close()
	lock.release()
def Writedata(data):
	lock.acquire()
	fw = open(datapath,'a')
	for i in data:
		fw.writelines(i)
	fw.close()
	lock.release()
def Writeip(string,status):
	lock.acquire()
	fw = open(ippath,'a')
	fw.write(string+'\t'+status+'\n')
	fw.close()
	lock.release()
	
def Analysis(data):
	pattern = re.compile(r'status: (\w+),')
	for line in data:
		line = line.strip()
		search = pattern.search(line)
		if search:
			return(search.group(1))
	return("")

def Run(ip_set):
	global fqdn
	global find
	##############################
	for ip in ip_set:
		ip = ip.strip()
		response = os.popen("dig @%s %s" % (ip,fqdn)).readlines()
		Writedata(response) 
		if len(response) > 7:
			status = Analysis(response)
			if status == "":
				Log("!!!!!%s analysis error, original data:\n%s" % (ip,response))
				continue
			lock.acquire()
			find = find + 1
			lock.release()
			Writeip(ip,status)
		else:
			status = "NULL"
			Writeip(ip,status)

def Thread_Run(data,ip_count):
	global count
	thread_task = 10
	while 1:
		ip_set = []
		lock.acquire()
		if len(data) > thread_task:
			ip_set = data[0:thread_task]
			del data[0:thread_task]
		else:
			ip_set = data[0:]
			del data[0:]
		lock.release()
		if ip_set == []:
			return
		Run(ip_set)
		lock.acquire()
		count = count + len(ip_set) 
		lock.release()
		Log("%s:%s->%s\tfinish:%d/%d" % (time.ctime(),ip_set[0].strip(),ip_set[-1].strip(),count,ip_count))

def File_run(inputfile,outputpath):
	global logpath
	global datapath
	global ippath
	global find
	global count
	isExists = os.path.exists(outputpath)
	if not isExists:
		os.mkdir(outputpath)
#	else:
#		os.system('rm -r '+outputpath)
#		os.mkdir(outputpath)
	logpath = os.path.join(outputpath,"log")
	datapath = os.path.join(outputpath,"data")
	ippath = os.path.join(outputpath,"ip")
	############################
	fr = open(inputfile)
	data = fr.readlines()
	ip_count = len(data)
	fr.close()
	###############################
	threads = []
	for i in range(Thread_MAX):
		t = threading.Thread(target=Thread_Run,args=(data,ip_count,))
		threads.append(t)
	Log("%s:%s\tstart" % (time.ctime(),inputfile))
	statis_start = time.asctime()
	starttime = time.time()
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	endtime = time.time()
	statis_end = time.asctime()
	Log("%s:%s\tend" % (time.ctime(),inputfile))
	spend = (endtime-starttime)/3600
	Log("find ip count:\t%s" % find)
	Log("check ip count:\t%s" % count)
	Log("spend time :\t%.5s" % spend)
	count = 0
	find = 0
	return


def main():
	##############################
	inputfile = sys.argv[1]
	outputpath = sys.argv[2]
	File_run(inputfile,outputpath)
	return

if __name__ == '__main__':
 	main() 
