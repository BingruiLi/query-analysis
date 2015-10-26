#!usr/bin/python
#coding=utf-8
import sys
import os
import re
import datetime
list_resolver = []
result_path = ""
my_logfile = "log"
my_real_resolver_file = "real_resolver"
_inttoIP = lambda x: '.'.join([str(int(x)/(256**i)%256) for i in range(3,-1,-1)])
def Log(log_str):
	f = open(my_logfile,'a')
	f.writelines(log_str+"\n")
	f.close()

def Write_resolver(iplist):
	f = open(my_real_resolver_file,'a')
	for i in iplist:
		f.write(i+"\n")
	f.close()

def Write_list(iplist,filename):
	global result_path
	filename = os.path.join(result_path,filename)
	f = open(filename,'w')
	for i in iplist:
		f.write(i+"\n")
	f.close()

def Write_dict(ipdict,filename):
	global result_path
	filename = os.path.join(result_path,filename)
	f = open(filename,'w')
	for i in ipdict:
		f.write(i+"\t")
		for j in ipdict[i]:
			f.write(j+"\t")
		f.write("\n")
	f.close()

def Write_list_response(ipdict,filename):
	global result_path
	filename = os.path.join(result_path,filename)
	f = open(filename,'w')
	for i in ipdict:
		f.write(i[0]+":"+str(i[1])+"\n")
	f.close()
def Write_dict_process(ipdict,filename):
	global result_path
	filename = os.path.join(result_path,filename)
	f = open(filename,'w')
	for i in ipdict:
		f.write(i+"---\t")
		for j in ipdict[i]:
			f.write(j+":"+str(ipdict[i][j])+"\t")
		f.write("\n")
	f.close()

def Iptoiprange(ip):
	temp = ip.split('.')[0:-1]
	i = ip.split('.')[-1]
	iprange = ""
	for j in temp:
		iprange = iprange+j+'.'	
	iprange = iprange + "0"
	return(iprange,i)

def process_1(data):

	dict_process = {}
	dict_response = {}


	pattern = re.compile(r'client (.+)#.* (\d+).hitnis.cn')
	#pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
	for line in data:
		find = pattern.search(line)
		if not find:
			continue
		if find.group(2) == '1111' or find.group(1) == '127.0.0.1':
			continue
		query = _inttoIP(find.group(2))
		response = find.group(1)

		if response not in dict_response:
			dict_response[response] = 0
		dict_response[response] = dict_response[response] + 1

		qiprange,i = Iptoiprange(query)	
		if qiprange not in dict_process:
			dict_process[qiprange] = {}
		riprange,i = Iptoiprange(response)	
		if riprange not in dict_process[qiprange]:
			dict_process[qiprange][riprange] = 0
		dict_process[qiprange][riprange] = dict_process[qiprange][riprange] + 1

	Write_dict_process(dict_process,"iprange_statistic")
	Write_list_response(sorted(dict_response.items(),key = lambda d:d[0]),"response_statistic")

def process(data):
	global list_resolver

	list_query = []
	list_response = []
	dict_query = {}
	dict_response = {}
	num = len(data)
	count = 0
	pattern = re.compile(r'client (.+)#.* (\d+).hitnis.cn')
	#pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
	for line in data:
		count = count + 1
		find = pattern.search(line)
		if not find:
			continue
		if find.group(2) == '1111' or find.group(1) == '127.0.0.1':
			continue
		query = _inttoIP(find.group(2))
		response = find.group(1)
		if query == response:
			if query not in list_resolver:
				list_resolver.append(query)

		if query not in list_query:
			list_query.append(query)
		if response not in list_response:
			list_response.append(response)
		if query not in dict_query:
			dict_query[query] = []
		dict_query[query].append(response)
		if response not in dict_response:
			dict_response[response] = []
		dict_response[response].append(query)
		Log("processed: %d\ttotal %d" % (count,num))
	Write_resolver(list_resolver)
	Write_list(list_query,"queryip")
	del list_query
	Write_list(list_response,"responseip")
	del list_response
	Write_dict(dict_response,"responseip_map")
	del dict_response
	Write_dict(dict_query,"queryip_map")

def main():
	global my_logfile
	global my_real_resolver_file
	global result_path
	my_time = sys.argv[1]
	result_path = os.path.dirname(sys.path[0])
	filepath = os.path.join(result_path,"log_data")
	file_list = os.listdir(filepath)
	result_path = os.path.join(result_path,"log_result")
	isExists = os.path.exists(result_path)
	if not isExists:
		os.mkdir(result_path)

	for filename in file_list:
		if filename != "query.log":
			continue
		f = open(os.path.join(filepath,filename))
		data = f.readlines()
		f.close()
		for i in range(0,len(data)):
			data[i] = data[i].strip()
			
		#获取昨天格式化的日期
#		now_time = datetime.datetime.now()
#		yes_time = now_time + datetime.timedelta(-1)
#		filename = yes_time.strftime("%Y%m%d")
		filename = my_time

		result_path = os.path.join(result_path,filename)
		isExists = os.path.exists(result_path)
		if not isExists:
			os.mkdir(result_path)
		my_logfile = os.path.join(result_path,my_logfile)
		my_real_resolver_file = os.path.join(result_path,my_real_resolver_file)
		process(data)
		process_1(data)

if __name__ == '__main__':
	main()
