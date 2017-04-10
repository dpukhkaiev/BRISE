#!/bin/bash
for f in *avg.csv
do
	python csv_to_xml.py $f
done
