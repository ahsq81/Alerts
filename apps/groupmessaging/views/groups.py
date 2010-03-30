#!/usr/bin/env python
# encoding=utf-8

from django import forms
from groupmessaging.views.common import webuser_required
from groupmessaging.models import Group
from groupmessaging.models import Site
from rapidsms.webui.utils import render_to_response
from django.http import HttpResponse


class GroupForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


@webuser_required
def list(request, context):

    ''' List Group '''

    try:
        Site_obj = Site.objects.get(id=context['user'].site.id)
    except Exception, e:
        return HttpResponse("Error 1 : %s" % e)

    try:
        Groups_obj = Group.objects.filter(site=Site_obj)
    except Exception, e:
        return HttpResponse("Error 2 : %s" % e)

    mycontext = {'title': 'regyo', 'Glist': Groups_obj}
    context.update(mycontext)

    return render_to_response(request, 'groups.html', context)


def add(request, context):

    ''' add function '''

    form = GroupForm()  # An unbound form
    mycontext = {'title': 'regyo', 'form': form}
    context.update(mycontext)

    return render_to_response(request, 'newgroups.html', context)
