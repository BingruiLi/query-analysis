#!/bin/bash
cd `dirname $0`
tmppath="/tmp/iplist"
time=$(date "+%Y%m%d")
resultpath="/tmp"
#extractor IP address from SQL database
echo "Extractor IP address from SQL database"
python ../libexec/extractorsql.py $tmppath

if [ ! -e $tmppath ]
then
	echo " IP data doesn't exists"
	exit 1
fi
#Measuring IP list
echo "Measuring IP list"
sh ../libexec/measureopenresolver.sh $tmppath $time $resultpath
#Update SQL database
echo "Update SQL database"
python ../libexec/updatesql.py $resultpath/$time/iplist $time maintain
#Delete tmp files
if [ -d $resultpath/$time ]
then
	rm -r $resultpath/$time
fi
if [ -e $tmppath ]
then
	rm $tmppath
fi
