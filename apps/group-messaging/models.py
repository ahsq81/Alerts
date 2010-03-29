#!/usr/bin/env python
# encoding=utf8

''' Group Messaging Models '''

from django.db import models
from django.contrib.auth.models import User, UserManager


class Site(models.Model):
    ''' Site Model

    Stores Top Level Entity
    Sites holds groups and users and recipients '''

    name = models.CharField(max_length=50)
    status = models.BooleanField()
    credit = models.PositiveIntegerField()
    manager = models.ForeignKey('User', blank=True, null=True)

    def __unicode__(self):
        return _(u"%s") % self.name

class WebUser(User):

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    recipients = models.ForeignKey('Recipients')

