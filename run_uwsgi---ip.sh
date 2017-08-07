#!/bin/bash

if [ -z $1 ];then
	ip=127.0.0.1
else
	ip=$1
fi

uwsgi   --socket $ip:3031 \
	--chdir $(pwd) \
	--wsgi-file django_phone/wsgi.py \
	--master --processes 1 --threads 2 \
	--stats $ip:9191
