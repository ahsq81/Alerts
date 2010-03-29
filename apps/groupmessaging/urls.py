#!usr/bin/env python
# encoding=utf-8

from django.conf.urls.defaults import *

from views import index
from views import messages
from views import groups

urlpatterns = patterns('',
    url(r'groupmessaging/?', index.index, name='index'),
    url(r'groupmessaging/messages?', messages.list, name='messages_list'),
    url(r'groupmessaging/groups?', groups.list, name='manage_groups'),
)
