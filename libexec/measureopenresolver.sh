#!/bin/bash
cd `dirname $0`
inputpath=$1
#outpath="../result"
time=$2
outpath=$3
if [ ! -d "$outpath" ]; then
	mkdir "$outpath"
fi
#outpath=$outpath/$(date +%Y%m%d);
outpath=$outpath/$time
if [ ! -d "$outpath" ]; then
	mkdir "$outpath"
fi
date_start=`date +%s%N|cut -c1-13`
python ./dig_measure.py $inputpath $outpath
date_end=`date +%s%N|cut -c1-13`
time=$((($date_end-$date_start)/1000))
echo "run time:" $time > $outpath/$timename
#created iplist is saved at $outpath/ip, with the format 'ip status' each line

