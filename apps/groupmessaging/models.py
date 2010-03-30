#!/usr/bin/env python
# encoding=utf8

''' Group Messaging Models '''

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext as _, ugettext_lazy


class Site(models.Model):
    ''' Site Model

    Stores Top Level Entity
    Sites holds groups and users and recipients '''

    name = models.CharField(verbose_name=ugettext_lazy(u"Name"), max_length=50)
    active = models.BooleanField(default=True)
    credit = models.PositiveIntegerField(default=0)
    manager = models.ForeignKey('WebUser', blank=True, null=True, \
                                related_name='managing')

    def __unicode__(self):
        return _(u"%(name)s") % {'name': self.name}


class WebUser(User):
    ''' WebUser Model

    System User which connects to web interface '''

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    recipient = models.ForeignKey('Recipient', blank=True, null=True)
    site = models.ForeignKey('Site', related_name='managing')

    comment = models.CharField(max_length=100, blank=True)


class Group(models.Model):
    ''' Group Model

    Group holds recipients and Messages '''

    class Meta:

        unique_together = ('code', 'site')

    code = models.CharField(max_length='15')
    name = models.CharField(max_length='50')
    site = models.ForeignKey('Site')
    active = models.BooleanField(default=True)
    recipients = models.ManyToManyField('Recipient', blank=True)
    managers = models.ManyToManyField('WebUser')

    def __unicode__(self):
        return _(u"%(name)s") % {'name': self.name}


class Recipient(models.Model):
    ''' Recipient Model

    A person with phone number and backend '''

    class Meta:
        unique_together = ('identity', 'backend')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    identity = models.CharField(max_length=30)
    backend = models.CharField(max_length=15, default='dataentry')

    active = models.BooleanField(default=True)

    site = models.ForeignKey('Site')

    def __unicode__(self):
        return _(u"%(full_name)s") % {'full_name': self.full_name}

    @property
    def full_name(self):
        return _(u"%(first)s %(last)s") % {'first': self.first_name.title(), \
                                        'last': self.last_name.upper()}


class Message(models.Model):
    ''' Message Model '''

    name = models.CharField(max_length=50)
    text = models.TextField()
    code = models.CharField(max_length=20, blank=True, null=True)
    site = models.ForeignKey('Site')

    def __unicode__(self):
        return _(u"%(name)s") % {'name': self.name}


class SendingLog(models.Model):
    ''' Messages Log '''

    sender = models.ForeignKey('WebUser')
    groups = models.ManyToManyField('Group')
    recipients = models.ManyToManyField('Recipient')
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    @property
    def short_text(self):
        if self.text.__len__() > 50:
            return _(u"%(striptext)s...") % {'striptext': self.text}
        else:
            return _(u"%(text)s") % {'text': self.text}

    def groups_list(self):
        glist = []
        for group in self.groups.all():
            glist.append(group.name)
        return _(u", ").join(glist)

    def __unicode__(self):
        return _(u"From %(from)s to %(groups)s on %(date)s: %(text)s") % \
               {'text': self.short_text, 'groups': self.groups_list(),
                'date': self.date.strftime('%x'), 'from': self.sender}


class OutgoingLog(models.Model):
    ''' Outgoing messages Log

    Stores every single SMS sent
    Status to be updated by gateway '''

    PENDING = 0
    DELIVERED = 1
    TIMEOUT = 2
    FAILED = 3

    VERBOSE_PENDING = _(u"Pending")
    VERBOSE_DELIVERED = _(u"Delivered")
    VERBOSE_TIMEOUT = _(u"Timed Out")
    VERBOSE_FAILED = _(u"Failed")

    STATUSES = (
        (PENDING, ugettext_lazy(VERBOSE_PENDING)),
        (DELIVERED, ugettext_lazy(VERBOSE_DELIVERED)),
        (TIMEOUT, ugettext_lazy(VERBOSE_TIMEOUT)),
        (FAILED, ugettext_lazy(VERBOSE_FAILED)),
    )

    RAW_STATUSES = [VERBOSE_PENDING, VERBOSE_DELIVERED, \
                    VERBOSE_TIMEOUT, VERBOSE_FAILED]

    sender = models.ForeignKey('WebUser')
    identity = models.CharField(max_length=30)
    backend = models.CharField(max_length=15)
    text = models.TextField()
    status = models.CharField(max_length=1, choices=STATUSES, default=PENDING)
    sent_on = models.DateTimeField()
    received_on = models.DateTimeField(blank=True, null=True)

    def text_length(self):
        return self.text.__len__()

    @property
    def status_text(self):
        try:
            return self.RAW_STATUSES[int(self.status)]
        except:
            return self.status

    def __unicode__(self):
        return _(u"%(text)s to %(identity)s: %(status)s") % \
               {'text': self.text, 'identity': self.identity, \
                'status': self.status_text}
