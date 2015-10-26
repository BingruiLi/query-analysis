#-*- coding:utf-8 -*-
import re
import sys
import os
file_dir = ""
def extractor_resolver(filepath):
	isExists = os.path.exists(filepath)
	if not isExists:
		print "FILE PATH ERROR:has no directory or file "
		return
	count = 0
	fread = open(filepath,'r')
	out_filepath = "resolver.txt"
	out_filepath = os.path.join(file_dir,out_filepath)
	fwrite = open(out_filepath,'w')
	fin = fread.read().split('\n')
	pattern = re.compile(r'^!!! Got answer from (?P<ip>\d+.\d+.\d+.\d+)')
	for i in range(0,len(fin)):
		match = pattern.match(fin[i])
		if match:
			fwrite.write(match.group('ip')+'\n')
			count = count+1
	fwrite.close()
	fread.close()
	return(count)
def high_extractor_resolver(filepath):
	isExists = os.path.exists(filepath)
	if not isExists:
		print "FILE PATH ERROR:has no directory or file "
		return
	count = [0,0]
	fread = open(filepath,'r')
	fin = fread.read().split('\n')
	out_filepath = "real_resolver.txt"
	out_filepath = os.path.join(file_dir,out_filepath)
	fwrite = open(out_filepath,'w')
	out_filepath = "wrong_resolver.txt"
	out_filepath = os.path.join(file_dir,out_filepath)
	fwrite_wrong = open(out_filepath,'w')
	pattern = re.compile(r'^!!! Got answer from (?P<ip>\d+.\d+.\d+.\d+)')
	pattern_second = re.compile(r'\D*(?P<ip_res>\d+.\d+.\d+.\d+)')
	for i in range(0,len(fin)):
		match = pattern.match(fin[i])
		if match:			
			match_second = pattern_second.match(fin[i+1])
			if match_second and match_second.group('ip_res') == match.group('ip'):
				fwrite.write(match_second.group('ip_res')+'\n')
				count[0] = count[0] + 1
			elif match_second:
				fwrite_wrong.write(match.group('ip')+'\t'+"received from \t"+match_second.group('ip_res')+'\n')
				count[1] = count[1] + 1
	fwrite.close()
	fwrite_wrong.close()
	fread.close()
	return(count)
def extractor_auth(filepath):
	isExists = os.path.exists(filepath)
	if not isExists:
		print "FILE PATH ERROR:has no directory or file "
		return
	count = 0
	fread = open(filepath,'r')
	out_filepath = "auth_server.txt"
	out_filepath = os.path.join(file_dir,out_filepath)
	fwrite = open(out_filepath,'w')
	fin = fread.read().split('\n')
	pattern = re.compile(r'^!!! Got an answer from (?P<ip>\d+.\d+.\d+.\d+)')
	for i in range(0,len(fin)):
		match = pattern.match(fin[i])
		if match:
			fwrite.write(match.group('ip')+'\n')
			count = count + 1
	fwrite.close()
	fread.close()
	return(count)
def high_extractor_auth(filepath):
	isExists = os.path.exists(filepath)
	if not isExists:
		print "FILE PATH ERROR:has no directory or file "
		return
	count = [0,0]
	fread = open(filepath,'r')
	fin = fread.read().split('\n')
	out_filepath = "auth_real_server.txt"
	out_filepath = os.path.join(file_dir,out_filepath)
	fwrite = open(out_filepath,'w')
	out_filepath = "wrong_auth_server.txt"
	out_filepath = os.path.join(file_dir,out_filepath)
	fwrite_wrong = open(out_filepath,'w')
	pattern = re.compile(r'^!!! Got an answer from (?P<ip>\d+.\d+.\d+.\d+)')
	pattern_second = re.compile(r'\D*(?P<ip_res>\d+.\d+.\d+.\d+)')
	for i in range(0,len(fin)):
		match = pattern.match(fin[i])
		if match:			
			match_second = pattern_second.match(fin[i+1])
			if match_second and match_second.group('ip_res') == match.group('ip'):
				fwrite.write(match_second.group('ip_res')+'\n')
				count[0] = count[0] + 1
			elif match_second:
				fwrite_wrong.write(match.group('ip')+'\t'+"received from \t"+match_second.group('ip_res')+'\n')
				count[1] = count[1] + 1
	fwrite.close()
	fwrite_wrong.close()
	fread.close()
	return(count)
def Usage():
	print "Usage:\n\t"+sys.argv[0]+" 'filename'\n"+"\tthe format of filename must end with .log\n"+"\tthe script will make a dir in the directory of your filename with the same name without postfix."
	return
if __name__ == '__main__':
	if len(sys.argv)  != 2:
		print "The number of parameters is wrong!"
		Usage()
		exit(0)
	filepath = sys.argv[1]
	pattern = re.compile(r'(.*)\.log$')
	match = pattern.match(filepath)
	if match:
		file_dir = match.group(1)
	else:
		print "The format of filepath is wrong!"
		Usage()
		exit(0)
	isExists = os.path.exists(file_dir)
	if not isExists:
		os.makedirs(file_dir)
	statistics_file = os.path.join(file_dir,"count_statistics.txt")
	fout = open(statistics_file,'w')
	fout.write("total resolver number is :\t"+str(extractor_resolver(filepath))+'\n')
	fout.write("possible resolver number is :\t"+str(high_extractor_resolver(filepath)[0])+'\n')
	fout.write("wrong resolver number is :\t"+str(high_extractor_resolver(filepath)[1])+'\n')
	fout.write("total authority server number is :\t"+str(extractor_auth(filepath))+'\n')
	fout.write("possible authority server number is :\t"+str(high_extractor_auth(filepath)[0])+'\n')
	fout.write("wrong authority server number is :\t"+str(high_extractor_auth(filepath)[1])+'\n')
	fout.close()
		



