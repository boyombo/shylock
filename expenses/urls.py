#!/usr/bin/env python
from django.conf.urls.defaults import *

urlpatterns = patterns('expenses.views',
    url(r'^$', 'new_expense', name='expense_new'),
    url(r'categories/$', 'list_categories', name='category_list'),
)

urlpatterns += patterns('simplereports.views',
        url(r'list/$', 'simple_list',
            {
                'app_label': 'expenses',
                'model_name': 'expense',
                'date_field': 'date',
                'template_name': 'expenses/expense_list.html'
            }, name='expense_list'),
        )