#!/bin/bash

/home/jagan/channeli/apps/news/scripts/rss.sh
python /home/jagan/channeli/manage.py shell < /home/jagan/channeli/apps/news/scripts/scrap_n_load.py
