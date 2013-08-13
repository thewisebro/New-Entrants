#!/bin/bash

media_dir=/home/`whoami`/channeli/media/

recursive_func() {
  for d in *; do
    if [ -d $d ]; then
      cp $media_dir/.gitignore $d/
      chmod 777 $d
      (cd $d; recursive_func)
    fi
  done
}

cd $media_dir
recursive_func
