#!/usr/bin/env python
# encoding=utf-8

from django.contrib import admin

from models import *

admin.site.register(Site)
admin.site.register(WebUser)
admin.site.register(Group)
admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(SendingLog)
admin.site.register(OutgoingLog)
