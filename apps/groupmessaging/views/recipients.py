#!/usr/bin/env python
# encoding=utf-8

from django.http import HttpResponseRedirect
from rapidsms.webui.utils import render_to_response
from groupmessaging.models import Recipient
from groupmessaging.models import Site
from groupmessaging.views.common import webuser_required
from django import forms
from django.shortcuts import redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage


@webuser_required
def list(request, context):

    recipients = Recipient.objects.all()
    paginator = Paginator(recipients,10)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        recipient_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        recipient_list = paginator.page(paginator.num_pages)


    mycontext = {'recipients': recipient_list,'count':recipients.count()}
    context.update(mycontext)
    return render_to_response(request, 'recipients_list.html', context)

@webuser_required
def recipient(request, context, recipientid=None):
    validationMsg =""
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
                validationMsg = "You have successfully updated the recipient"
            else:
                try:
                    recipient = Recipient(first_name=form.cleaned_data['firstName'] ,\
                                           last_name=form.cleaned_data['lastName'],\
                                           identity=form.cleaned_data['identity'],\
                                           active=form.cleaned_data['active'],\
                                           site = context['user'].site)
                    recipient.save()
                    validationMsg = "You have successfully inserted a recipient %s." % form.cleaned_data['firstName']
                except Exception, e :
                    validationMsg = "Failed to add new recipient %s." % e

                #recipients = Recipient.objects.all()
                mycontext = {'validationMsg':validationMsg}
                context.update(mycontext)
                #return render_to_response(request, 'recipients_list.html', context)
                return redirect(list)
                
                
    else:
        if recipient:
            data = {'firstName': recipient.first_name,'lastName':recipient.last_name,'identity':recipient.identity,'active':recipient.active}
        else:
            data = {'active': True}
        form = RecipientForm(data) 
    
    if not recipientid:
        recipientid = 0

    mycontext = {'recipient':recipient,'form':form, 'recipientid': recipientid,'validationMsg':validationMsg}
    context.update(mycontext)
    return render_to_response(request, 'recipient.html', context)

@webuser_required
def delete(request,context,recipientid):
    validationMsg =""
    recipient = Recipient.objects.get(id=recipientid)
                
    try:
        recipient.delete()
        validationMsg = "You have successfully deleted this record"
    except Exception, e :
        validationMsg = "Failed to delete %s." % e

    mycontext = {'validationMsg':validationMsg}
    context.update(mycontext)
    return redirect(list)

class RecipientForm(forms.Form):
    firstName = forms.CharField(label=(u"First Name"), max_length=50)
    lastName  = forms.CharField(label=(u"Last Name"),max_length=50)
    identity  = forms.CharField(label=(u"Identity"),max_length=30)
    active    = forms.BooleanField(label=(u"Active"),required=False)
    #site      = forms.ModelMultipleChoiceField(queryset= Site.objects.all(), required=True)


   
