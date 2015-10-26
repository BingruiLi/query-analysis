#!bin/bash

#获取脚本所在路径
cd `dirname $0`
#query.log路径
logpath="/var/cache/bind/query.log"
resultpath="../result"
time=$(date "+%Y%m%d" -d "-1day")

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
#调用蛮力扫描验证递归解析器IP地址是否开放,开放的ip地址列表存入$resultpath/$time中的iplist文件中
echo "Measuring Open resolvers"
sh ../libexec/measureopenresolver.sh ../log_result/$time/responseip $time $resultpath
#更新数据库
echo "Updating databases"
sh ../libexec/createsql.sh
python ../libexec/updatesql.py $resultpath/$time/iplist $time main
#结束
