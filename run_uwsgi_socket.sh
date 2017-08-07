#!/bin/sh

ip=127.0.0.1
ip_stats=$ip

uwsgi   --socket $ip:3031 \
	--chdir $(pwd) \
	--wsgi-file django_phone/wsgi.py \
	--master --processes 1 --threads 2 \
	--stats $ip_stats:9191
