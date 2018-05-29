#!/usr/bin/env bash
export ENVIRONMENT='development'
export PYTHONOPTIMIZE=1
export DATABASE_NAME=''
export DATABASE_HOST=''
export DATABASE_USER=''
export DATABASE_PASSWORD=''
export MAIL_SERVER='smtp.'
export MAIL_PORT=465
export MAIL_USE_SSL=1 #0: 关闭, 1: 开启
export MAIL_ADMIN=''
export MAIL_DEBUG=1
export CACHE_REDIS_HOST='127.0.0.1'
export CACHE_REDIS_PORT=6379
export CACHE_REDIS_PASSWORD=''
export REDIS_URL="redis://:$CACHE_REDIS_PASSWORD@$CACHE_REDIS_HOST:$CACHE_REDIS_PORT/0"
export SQLALCHEMY_DATABASE_URI="mysql+mysqldb://$DATABASE_USER:$DATABASE_PASSWORD@$DATABASE_HOST/$DATABASE_NAME?charset=utf8"
export LDAP_PROVIDER_URL='ldap://zyram.jiagouyun.com:389/'  # 生产
export LDAP_PROVIDER_USERNAME='uid=syncadmin,ou=Mgr,ou=SYSTEM,dc=jiagouyun,dc=com'
export LDAP_PROVIDER_PASSWORD='mF8DkC5meTLMpjv0b6Av'
export MAIL_USERNAME='@jiagouyun.com'
export MAIL_PASSWORD=''
export KITCHEN_USERNAME='devops'
export KITCHEN_PASSWORD='9dxtbami'
export KITCHEN_URL='https://kitchen.care.cn'
export WSGI_BIND='0.0.0.0:5000'
export WSGI_ACCESS_LOG="/tmp/access.log"
export WSGI_ERROR_LOG='/tmp/error.log'
export WSGI_PID_FILE='/tmp/gunicorn.pid'
export WSGI_LOG_LEVEL='debug'
export WSGI_RUN_WORKERS='4'
export WSGI_DEBUG=1
export APP_DEBUG=1     #0: 关闭, 1: 开启
export APP_TESTING=0   #0: 关闭, 1: 开启
export APP_RUN_LOG='/tmp/123.log'
