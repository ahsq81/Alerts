#!usr/bin/env python
# encoding=utf-8

from django.conf.urls.defaults import *

from views import index

urlpatterns = patterns('',
    url(r'groupmessaging/?', index.index, name='index'),
)
