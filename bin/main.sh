#!/bin/bash
#获取脚本所在路径
cd `dirname $0`

#读取配置文件
CONF_PATH="../etc/program.conf"

#LOGPATH="/var/cache/bind/query.log"
LOGPATH=`grep ^LOGPATH $CONF_PATH | awk '{print $3}'`
#RESULTPATH="../result"
RESULTPATH=`grep ^MAIN_RESULTPATH $CONF_PATH | awk '{print $3}'`
#LOGDATA="../log_data"
LOGDATA=`grep ^LOGDATA $CONF_PATH | awk '{print $3}'`

LC_TIME=en_US.UTF-8
str_date=$(date --date='yesterday' +%d-%b-%Y)
LC_TIME=zh_CN.UTF-8
time=$(date "+%Y%m%d" -d "-1day")

if [ ! -d $RESULTPATH ]
then
	mkdir $RESULTPATH
fi
if [ ! -d $LOGDATA ]
then
	mkdir $LOGDATA
fi
#取出前一天的请求日志，存入$LOGDATA/目录中
echo "Reading query.log"
if [ ! -e $LOGDATA/query.log ]
then
	grep '^'$str_date $LOGPATH > $LOGDATA/query.log
fi
#调用分析日志脚本,该脚本保存结果在../log_result/$time目录下
echo "Processing query.log"
python ../libexec/process.py $time
		
#将处理完结果存入done目录
if [ ! -d $LOGDATA/done ]
then
	mkdir $LOGDATA/done
fi
mv $LOGDATA/query.log $LOGDATA/done/query.log.$time

#调用dig测量脚本测量递归解析器IP地址是否开放,开放的ip地址列表存入$RESULTPATH/$time中的ip文件中,每行格式为'ip status'
echo "Measuring Open resolvers"
outpath=$RESULTPATH/$time
if [ ! -d "$outpath" ]; then
	mkdir "$outpath"
fi
python ../libexec/dig_measure.py ../log_result/$time/responseip $outpath

if [ ! -e $outpath/ip ]; then
	echo "dig_measure's result is empty!"
	exit
fi
#更新数据库
echo "Updating databases"
#sh ../libexec/sql_create.sh
#python ../libexec/sql_update.py $outpath/ip $time main
python ../libexec/sql_update.py -t $time --main $outpath/ip
#结束
