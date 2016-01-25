#!/bin/bash
cd `dirname $0`


#读取配置文件
CONF_PATH="../etc/program.conf"
#RESULTPATH="../dig_result"
RESULTPATH=`grep ^MAINTAIN_RESULTPATH $CONF_PATH | awk '{print $3}'`

tmpfile=$RESULTPATH"/iplist"
time=$(date "+%Y%m%d")
timehour=$(date "+%Y%m%d%H")

if [ ! -d $RESULTPATH ]; then
	mkdir $RESULTPATH
fi
#extractor IP address from SQL database
echo `date`" Extractor IP address from SQL database"
python ../libexec/sql_extractor.py $tmpfile
if [ ! -e $tmpfile ]
then
	echo " IP data doesn't exists"
	exit 1
fi

#调用dig测量脚本测量递归解析器IP地址是否开放,开放的ip地址列表存入$RESULTPATH/$time中的ip文件中,每行格式为'ip status'
echo `date`" Measuring IP list"
outpath=$RESULTPATH/$timehour
if [ ! -d $outpath ]; then
	mkdir $outpath
else
	rm -r $outpath
fi
python ../libexec/dig_measure.py $tmpfile $outpath

if [ ! -e $outpath/ip ]; then
	echo "dig_measure's result is empty!"
	exit
fi

#更新数据库
echo `date`" Updating databases"
#sh ../libexec/sql_create.sh
python ../libexec/sql_update.py -t $time --maintain $outpath/ip
#Delete tmp files
#
#if [ -d $outpath ]
#then
#	rm -r $outpath
#fi
#if [ -e $tmpfile ]
#then
#	rm $tmpfile
#fi
