#!/bin/bash

apt-get install -y gcc
apt-get install -y libapache2-mod-wsgi
apt-get install -y python-pip
apt-get install -y php5
apt-get install -y ruby
apt-get install -y rubygems
apt-get install -y python-mysqldb
apt-get install -y python-pygresql

pip install Django\==1.7

# Installing PIL
#apt-get build-dep python-imaging
#apt-get install libjpeg62 libjpeg62-dev
#ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so
#ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
#ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/libfreetype.so
#pip install PIL (install pillow instead)

# Installing Pillow
pip install Pillow

#Install nodejs
curl -sL https://deb.nodesource.com/setup | bash -
apt-get install -y nodejs

#Install handlebars
npm install --verbose handlebars -g

# django-compressor
pip install django-appconf
pip install versiontools

# Installing compass
gem install --verbose compass
apt-get install -y ruby-compass

# django-debug-toolbar
pip install sqlparse

# django-fluent-comments
pip install Akismet

# Install JAVA
sudo apt-get install openjdk-7-jdk

# Install jetty
#sudo apt-get install jetty
#sudo apt-get install libjetty-extra

####### 'BeautifulSoup' Installation ########

# python lxml parser [Dependency]
apt-get install -y python-lxml

# python html5lib parser [Dependency]
apt-get install -y python-html5lib

# python BeautifulSoup [Main installation]
pip install BeautifulSoup

#################### Ends ###################

# django-extensions
pip install Werkzeug

# several python modules

pip install xhtml2pdf
pip install pisa
pip install xlrd
pip install xlwt
pip install whoosh
pip install mutagen
pip install reportlab
pip install python-dateutil
pip install simplejson

# fuzzy wuzzy
pip install -e git+https://github.com/seatgeek/fuzzywuzzy.git#egg=fuzzywuzzy

# memcached
apt-get install -y memcached
pip install python-memcached

# haystack
pip install django-haystack

# django-user-agents
pip install pyyaml ua-parser user-agents
pip install django-user-agents

#Install redis
apt-get install -y redis-server
pip install redis

pip install elasticsearch
