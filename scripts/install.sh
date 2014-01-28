#!/bin/bash

apt-get install gcc
apt-get install libapache2-mod-wsgi
apt-get install python-pip
apt-get install rubygems
apt-get install python-mysqldb

pip install Django\==1.6.1

# Installing PIL
apt-get build-dep python-imaging
apt-get install libjpeg62 libjpeg62-dev
ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so
ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/libfreetype.so
pip install PIL

# django-compressor dependency
pip install django-appconf
pip install versiontools

# Installing compass
gem install compass

# django-debug-toolbar
pip install sqlparse
