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
savename="verify.log"
timename="verify.time"
date_start=`date +%s%N|cut -c1-13`
./my_find_open_resolvers $inputpath > $outpath/$savename
date_end=`date +%s%N|cut -c1-13`
time=$((($date_end-$date_start)/1000))
echo "run time:" $time > $outpath/$timename
#extractor ip from verify.log
cat $outpath/$savename | perl -ne ' print $1."\n" if (m/!!! Got an.* (\d+.+) - possible/)' > $outpath/iplist
