#!/usr/bin/env python
from django.conf.urls.defaults import *

urlpatterns = patterns('accounting.views',
    url(r'pandl/$', 'pandl', name='accounting_pandl'),
    url(r'graph/$', 'graph', name='accounting_graph'),
)