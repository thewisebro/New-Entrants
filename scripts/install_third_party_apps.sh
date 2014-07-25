#!/bin/bash

cd ~/channeli/third_party_apps

for dir in *
do
  if [ -d "$dir" ] ; then
    pip install -e $dir
  fi
done
