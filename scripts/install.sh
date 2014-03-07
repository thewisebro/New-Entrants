#!/bin/bash

apt-get install gcc
apt-get install libapache2-mod-wsgi
apt-get install python-pip
apt-get install php5
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

# django-compressor
pip install django-appconf
pip install versiontools

# Installing compass
gem install compass

# django-debug-toolbar
pip install sqlparse

# django-fluent-comments
pip install Akismet

# Install JAVA
sudo apt-get install openjdk-7-jdk

# Install jetty
sudo apt-get install jetty
sudo apt-get install libjetty-extra

####### 'BeautifulSoup' Installation #########

# python lxml parser [Dependency]
apt-get install python-lxml

# python html5lib parser [Dependency]
apt-get install python-html5lib

# python BeautifulSoup [Main installation]
pip install BeautifulSoup

#################### Ends ###################


