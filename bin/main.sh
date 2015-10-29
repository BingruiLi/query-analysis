#!bin/bash

#获取脚本所在路径
cd `dirname $0`
#query.log路径
logpath="/var/cache/bind/query.log"
resultpath="../result"
time=$(date "+%Y%m%d" -d "-1day")
if [ ! -d $resultpath ]
then
	mkdir $resultpath
fi
if [ ! -d ../log_data ]
then
	mkdir ../log_data
fi
#取出前一天的请求日志，存入../log_data/目录中
echo "Reading query.log"
if [ ! -e ../log_data/query.log ]
then
	cat $logpath | perl -ne ' ($week,$mon,$day,$ht,$year)=split(" ",localtime(time()-3600*24)); my $time= $day."-".$mon."-".$year; my @field = split(" ",$_); if($field[0] eq $time){ print $_;}' > ../log_data/query.log
fi
#调用分析日志脚本,该脚本保存结果在../log_result/$time目录下
echo "Processing query.log"
python ../libexec/process.py $time
		
#将处理完结果存入done目录
if [ ! -d ../log_data/done ]
then
	mkdir ../log_data/done
fi
mv ../log_data/query.log ../log_data/done/query.log.$time

#调用dig测量脚本测量递归解析器IP地址是否开放,开放的ip地址列表存入$resultpath/$time中的ip文件中,每行格式为'ip status'
echo "Measuring Open resolvers"
outpath=$resultpath/$time
if [ ! -d "$outpath" ]; then
	mkdir "$outpath"
fi
python ../libexec/dig_measure.py ../log_result/$time/responseip $outpath

#更新数据库
echo "Updating databases"
sh ../libexec/sql_create.sh
python ../libexec/sql_update.py $outpath/ip $time main
#结束
