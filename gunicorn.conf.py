bind = ['0.0.0.0:8000']
time_out = 60

proc_name = 'Lutan'
pidfile = '/tmp/lutan.pid'
worker_class = 'gevent'
max_requests = 600
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
