#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response

def list(request):

    return render_to_response(request, 'recipients_list.html', {})