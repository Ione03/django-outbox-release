import imp,os,sys
sys.path.insert(0,os.path.dirname(__file__))
wsgi=imp.load_source('wsgi','django_outbox/wsgi.py')
application=wsgi.application