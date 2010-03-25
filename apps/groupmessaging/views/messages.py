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

@webuser_required
def messageform(request, context, messageid):
    '''form for Add/Edit messages'''
    
    if request.method == 'POST':
    
        form = MessageForm(request.POST)
        if form.is_valid(): 
            
            return HttpResponseRedirect('/thanks/') 
    else:
        mess = Message.objects.get(id=messageid)
        data = {'name': mess.name, 'text': mess.text, 'code':mess.code}
        form = MessageForm(data) 
        
    mycontext = {'mess':mess, 'form':form}
    context.update(mycontext)
    return render_to_response(request,"messages_form.html",context)
    
class MessageForm(forms.Form):

  
    code = forms.CharField(max_length=20)
    name = forms.CharField(max_length=50)
    text = forms.CharField()
    
