#!/bin/bash

if [ "$USER" == "root" ]; then
  cd /home/apps/channeli/third_party_apps
else
  cd ~/channeli/third_party_apps
fi

for dir in *
do
  if [ -d "$dir" ] ; then
    pip install -e $dir
  fi
done
