#!/usr/bin/python
import sys
import os
logpath = "/var/cache/bind/query.log"
my_logpath = "./my_log"
def Log(log_str):
	f = open(my_logpath,'a')
	f.writelines(my_logpath+"\n")
	f.close()

def processdate(flag):
	day = flag[0].split('-')[0:-1]
	day_str = day[1]+"-"+day[0]
	return(day_str)

def save(m_list,m_flag,m_hour):
	day = processdate(m_flag)
	path = "./"
	path = os.path.join(path,day)
	isExists = os.path.exists(path)
	if not isExists:
		os.mkdir(path)
	path = os.path.join(path,m_hour)
	isExists = os.path.exists(path)
	if not isExists:
		os.mkdir(path)
	filepath = os.path.join(path,"query.log")
	f = open(filepath,'w')
	for i in m_list:
		f.write(i)
	f.close()

def main():
	isExists = os.path.exists(logpath)
	if not isExists:
		Log("logpath not exists!")
		return
	m_list = []
	f = open(logpath)
	m_flag = f.readline().strip().split(' ')[0:2]
	m_time = m_flag[-1]
	m_hour = m_time[0:2]
	f.seek(0,0)
	while True:
		line = f.readline()	
		if not line:
			save(m_list,m_flag,m_hour)
			break
		time = line.split(' ')[1]
		hour = time[0:2]
		if hour == m_hour:
 			m_list.append(line)
		else:
			save(m_list,m_flag,m_hour)		
			m_list = []
			m_flag = line.strip().split(' ')[0:2]
			m_time = m_flag[-1]
			m_hour = m_time[0:2]
			m_list.append(line)
	f.close()
	return




if __name__ == '__main__':
	main()
