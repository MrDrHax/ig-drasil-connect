# gunicorn_config.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8080'

accesslog = '/home/ubuntu/logs/access.log'  # replace with the path to your access log file
errorlog = '/home/ubuntu/logs/error.log'  # replace with the path to your error log file
loglevel = 'info' 
