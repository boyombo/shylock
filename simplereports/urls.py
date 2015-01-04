#!/usr/bin/env python
from django.conf.urls.defaults import *

urlpatterns = patterns('simplereports.views',
    url(r'(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<date_field>\w*)[/]*$', 'simple_list', name='simplereport_simple_list'),
)