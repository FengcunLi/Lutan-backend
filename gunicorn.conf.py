bind = ['0.0.0.0:8000']
time_out = 60

proc_name = 'Lutan'
pidfile = '/tmp/lutan.pid'
worker_class = 'gevent'
max_requests = 600
accesslog = '/tmp/gunicorn_access.log'
errorlog = '/tmp/gunicorn_error.log'
