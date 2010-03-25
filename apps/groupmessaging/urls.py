#!usr/bin/env python
# encoding=utf-8

from django.conf.urls.defaults import *

from views import index
from views import messages
from views import groups
from views import recipients

urlpatterns = patterns('',
    url(r'^groupmessaging/?$', index.index, name='index'),
    url(r'^groupmessaging/messages/?$', messages.list, name='messages_list'),
    url(r'^groupmessaging/groups/?$', groups.list, name='groups'),
    url(r'^groupmessaging/groups/add_group/?$', groups.add, name='new_group'),
    url(r'^groupmessaging/recipients/?$', recipients.list, \
        name='recipients_list'),
    url(r'^groupmessaging/recipients/(\d+)/?$', recipients.recipient, \
        name='recipient'),
    url(r'^groupmessaging/recipients/add/?$', recipients.recipient, \
        name='recipient_add'),
)
