import multiprocessing

bind = "unix:/run/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 3
worker_connections = 1000
timeout = 30
keepalive = 2

proc_name = 'social_media_api'

accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

pidfile = "/run/gunicorn/gunicorn.pid"
daemon = False
preload_app = True
