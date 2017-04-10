#!/bin/bash

#for f in csvs/pigz_compress_full.csv
for f in csvs/enwik4*_avg.csv

do
	for d_t in "encrypt" #enw8 enw9 app wav game flac
	do
		#for rep in {1..10} 
		#do

		python start.py ${f:5} $d_t 5 1 96&! # $rep&!
		##echo ${f:5}
		#done
	done
#	for d_t in {16..22}
 #       do
        
  #              python start.py ${f:5} $d_t 1 1
                #echo ${f:5}
   #     done

done
