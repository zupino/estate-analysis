#!/bin/bash

/home/zeta/autoHouse/auto2.py > /home/zeta/autoHouse/raw/`date +"%Y%m%d"`.csv

mv /home/zeta/autoHouse/new /home/zeta/autoHouse/old
cp /home/zeta/autoHouse/raw/`date +"%Y%m%d"`.csv /home/zeta/autoHouse/new


#echo -e "To: eng.marco.zunino@gmail.com, anca.onisoru@gmail.com\nFrom:houseSearcher@zupino.com\nSubject: Daily report new houses\nMIME-Version: 1.0\nContent-Type: text/html\nContent-Disposition: inline\n<html>\n<body>\n<pre style=\"font: monospace\">" > /home/zeta/autoHouse/`date +"%Y%m%d"`_summary.html
#/home/zeta/autoHouse/analysis.r >> /home/zeta/autoHouse/`date +"%Y%m%d"`_summary.html
#echo -e "</pre></body></html>" >> /home/zeta/autoHouse/`date +"%Y%m%d"`_summary.html
#
#
#cat /home/zeta/autoHouse/`date +"%Y%m%d"`_summary.html | /usr/sbin/sendmail -t
#
#mv /home/zeta/autoHouse/`date +"%Y%m%d"`_summary.html /home/zeta/autoHouse/raw/


