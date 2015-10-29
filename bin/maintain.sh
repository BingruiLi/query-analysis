#!/bin/bash
cd `dirname $0`
tmpfile="/tmp/iplist"
time=$(date "+%Y%m%d")
resultpath="/tmp"
#extractor IP address from SQL database
echo "Extractor IP address from SQL database"
python ../libexec/sql_extractor.py $tmpfile
if [ ! -e $tmpfile ]
then
	echo " IP data doesn't exists"
	exit 1
fi

#调用dig测量脚本测量递归解析器IP地址是否开放,开放的ip地址列表存入$resultpath/$time中的ip文件中,每行格式为'ip status'
echo "Measuring IP list"
outpath=$resultpath/$time
if [ ! -d "$outpath" ]; then
	mkdir "$outpath"
fi
python ../libexec/dig_measure.py $tmpfile $outpath

#更新数据库
echo "Updating databases"
sh ../libexec/sql_create.sh
python ../libexec/sql_update.py $outpath/ip $time maintain

#Delete tmp files
if [ -d $resultpath/$time ]
then
	rm -r $resultpath/$time
fi
if [ -e $tmpfile ]
then
	rm $tmpfile
fi
