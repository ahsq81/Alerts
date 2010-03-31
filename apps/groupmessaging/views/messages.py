#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response
from groupmessaging.views.common import webuser_required
from django import forms
from django.shortcuts import redirect
from groupmessaging.models import Message
from groupmessaging.models import Site

@webuser_required
def list(request, context):
    
    messages = Message.objects.all()
    count = Message.objects.count()
    mycontext = {'messages':messages, 'count':count}
    context.update(mycontext)

    return render_to_response(request, 'messages.html', context)

@webuser_required
def messageform(request, context, messageid=None):
    '''form for Add/Edit messages'''
    
    if not messageid or int(messageid) == 0:
        mess = None
    else :
        mess = Message.objects.get(id=messageid)
        
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            if mess :
                mess.code =  form.cleaned_data['code']
                mess.name =  form.cleaned_data['name']
                mess.text =  form.cleaned_data['text']
                mess.site =  context['user'].site
                mess.save()
                
            else :
                mess = Message(code = form.cleaned_data['code'] , name = form.cleaned_data['name'], \
                                           text = form.cleaned_data['text'], \
                                           site = context['user'].site)  
                mess.save()
                
                mess = Message.objects.all()
                mycontext = {'mess':mess}
                context.update(mycontext)
                return redirect(list)
           
    else:
        if mess :
            data = {'name': mess.name, 'text': mess.text, 'code':mess.code}          
        else:
            data = {'code': 'code','name':'name','test':'text'}
        form = MessageForm(data) 
            
    if not messageid:
        messageid=0
    
    mycontext = {'mess':mess, 'form':form , 'messageid':messageid}
    context.update(mycontext)
    return render_to_response(request,"messages_form.html",context)


@webuser_required    
def delete(request, context, messageid):
    
    message = Message.objects.get(id=messageid)
    message.delete()
    mycontext = {'message':message}
    context.update(mycontext)
       
    return redirect(list)

    
class MessageForm(forms.Form):

  
    code = forms.CharField(max_length=20)
    name = forms.CharField(max_length=50)
    text = forms.CharField(widget=forms.Textarea(),initial="Please enter your message here")


    
