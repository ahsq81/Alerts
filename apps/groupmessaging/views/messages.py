#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response
from groupmessaging.views.common import webuser_required
from django import forms
from groupmessaging.models import Message


@webuser_required
def list(request, context):
    
    messages = Message.objects.all()
    mycontext = {'messages':messages}
    context.update(mycontext)
    return render_to_response(request, 'messages.html', context)

    
def messageform(request, messageid):
    '''form for Add/Edit messages'''
    
    mess = Message.objects.get(id=messageid)
    return render_to_response(request,"messages_form.html",{"mess":mess})
    
