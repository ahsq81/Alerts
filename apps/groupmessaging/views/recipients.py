#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response
from groupmessaging.models import Recipient
from groupmessaging.views.common import webuser_required
from django import forms

@webuser_required
def list(request,context):
    
    recipients = Recipient.objects.all()
    mycontext = {'recipients': recipients}
    context.update(mycontext)
    return render_to_response(request, 'recipients_list.html', context)

@webuser_required
def recipient(request,context,recipientid=None):
    print recipientid
    if not recipientid or int(recipientid) == 0:
        recipient = None
    else:
        recipient = Recipient.objects.get(id=recipientid)
    
    if request.method == 'POST':
        form = RecipientForm(request.POST) 
        if form.is_valid():
            if recipient:
                recipient.first_name = form.cleaned_data['firstName']
                recipient.last_name = form.cleaned_data['lastName']
                recipient.identity = form.cleaned_data['identity']
                recipient.active = form.cleaned_data['active']
                recipient.save()
            else:
                recipient = Recipient(first_name=form.cleaned_data['firstName'] , last_name=form.cleaned_data['lastName'], identity=form.cleaned_data['identity'],active=form.cleaned_data['active'] )
                recipient.save()
    else:
        if recipient:
            data = {'firstName': recipient.first_name,'lastName':recipient.last_name,'identity':recipient.identity,'active':recipient.active}
        else:
            data = {'firstName': 'First name','lastName':'Last name','identity':'0599 '}
        form = RecipientForm(data) 
    
    if not recipientid:
        recipientid = 0

    mycontext = {'recipient':recipient,'form':form, 'recipientid': recipientid}
    context.update(mycontext)
    return render_to_response(request, 'recipient.html', context)

class RecipientForm(forms.Form):
    firstName = forms.CharField(max_length=50)
    lastName  = forms.CharField(max_length=50)
    identity  = forms.CharField(max_length=30)
    active    = forms.BooleanField(required=False)

   
