#!/usr/bin/env python
# encoding=utf-8

from django import forms
from groupmessaging.views.common import webuser_required
from groupmessaging.models import Group
from groupmessaging.models import Site
from groupmessaging.models import Recipient
from groupmessaging.models import WebUser
from rapidsms.webui.utils import render_to_response
from django.http import HttpResponse


class GroupForm(forms.Form):
    code = forms.CharField(max_length='15', required=True)
    name = forms.CharField(max_length='50', required=True)
   # site = forms.ForeignKey('Site')
    active = forms.BooleanField(required=False)
    recipients = forms.ModelMultipleChoiceField(\
    queryset=Recipient.objects.filter(active=True), required=True)
    managers = forms.ModelMultipleChoiceField(\
    queryset=WebUser.objects.all(), required=True)


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


@webuser_required
def add(request, context):

    ''' add function '''

    if request.method == 'POST':  # If the form has been submitted...
        form = GroupForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            code = form.cleaned_data['code']
            name = form.cleaned_data['name']
            active = form.cleaned_data['active']
            recipients = form.cleaned_data['recipients']
            managers = form.cleaned_data['managers']

            try:
                ins = Group(code=code, name=name,\
                site=context['user'].site, active=active)
                ins.save()
                for recipient in recipients:
                    ins.recipients.add(recipient)
                for manager in managers:
                    ins.recipients.add(manager)

            except Exception, e:
                return HttpResponse("Error 2 : %s" % e)

            return render_to_response(request, 'groups.html', context)

    else:
        form = GroupForm()  # An unbound form
        mycontext = {'form': form}
        context.update(mycontext)

    return render_to_response(request, 'new_group.html', context)


@webuser_required
def delete(request, context, group_id):

    ''' add function '''

    try:
        Groups_obj = Group.objects.get(id=group_id)
        Groups_obj.delete()
    except Exception, e:
        return HttpResponse("Error 2 : %s" % e)

    return render_to_response(request, 'groups.html', context)


@webuser_required
def update(request, context, group_id):

    ''' add function '''

    return HttpResponse("Under Construction")
