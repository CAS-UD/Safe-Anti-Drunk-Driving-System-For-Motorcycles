import multiprocessing 
from gevent import monkey

monkey.patch_all()

worker_class = 'gevent'
bind = '0.0.0.0:8000'
debug = True
workers = multiprocessing.cpu_count() * 2 + 1

