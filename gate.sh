#!/bin/bash
cd /home/pi/gate
gunicorn -c conf.py app:app
# if you just want gunicorn to serve it, will need to run as root to bind to ports under 1000. Comment previous line and uncomment following
#gunicorn -c conf.py -b 0.0.0.0:80 app:app