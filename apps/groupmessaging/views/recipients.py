#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response
from groupmessaging.models import Recipient

def list(request):
    
    recipients = Recipient.objects.all()
    
    return render_to_response(request, 'recipients_list.html', {'recipients':recipients})

def recipient(request,recipientid):
    
    recipient = Recipient.objects.get(id=recipientid)

    return render_to_response(request, 'recipient.html', {'recipient':recipient})