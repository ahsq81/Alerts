#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8

from django.conf import settings

INSTALLED_APPS.extend(['django.contrib.humanize'])

settings.configure(**locals())
