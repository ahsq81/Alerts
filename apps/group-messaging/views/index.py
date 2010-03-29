#!/usr/bin/env python
# encoding=utf-8

from rapidsms.webui.utils import render_to_response

def index(request):

    return render_to_response(request, 'index.html', {})
