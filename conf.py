import multiprocessing

bind = "unix:gate.sock"
workers = multiprocessing.cpu_count() * 2 + 1
#daemon = True
accesslog = "/home/pi/gate/logs/access.log"
errorlog = "/home/pi/gate/logs/error.log"
loglevel = "warning"
capture_output = True
