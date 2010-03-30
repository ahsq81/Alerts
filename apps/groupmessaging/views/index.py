#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response

from groupmessaging.views.common import webuser_required
from groupmessaging.models import SendingLog


@webuser_required
def index(request, context):

    latest_messages = SendingLog.objects.all()[:5]

    mycontext = {'latest_messages': latest_messages}
    context.update(mycontext)
    return render_to_response(request, 'index.html', context)
