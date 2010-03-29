#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response

from groupmessaging.views.common import webuser_required


@webuser_required
def index(request, context):

    mycontext = {'title': 'regyo'}
    context.update(mycontext)
    return render_to_response(request, 'index.html', context)
