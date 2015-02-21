#!/bin/bash

# Minifying css/js files
for f in `find static_root/ -regex ".*\.\(css\|js\)"`
do
  echo "Minifying $f"
  java -jar scripts/yuicompressor-2.4.8.jar $f -o $f
done

# optimize all png files
for f in `find static_root/ -name '*.png'`
do
  echo "Optimizing $f"
  optipng $f >/dev/null
done

#optimize all jpg/jpeg files
for f in `find static_root/ -regex ".*\.\(jpeg\|jpg\)"`
do
  echo "Optimizing $f"
  jpegtran -copy none -optimize -outfile $f $f
done
