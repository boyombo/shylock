#!/usr/bin/env python
from django.conf.urls import url

from expenses import views


urlpatterns = [
    url(r'^$', views.new_expense, name='expense_new'),
    url(r'categories/$', views.CategoryList.as_view(), name='category_list'),
    url(r'list/$', views.ExpensesList.as_view(), name='expense_list'),
]

#urlpatterns += patterns('simplereports.views',
#        url(r'list/$', 'simple_list',
#            {
#                'app_label': 'expenses',
#                'model_name': 'expense',
#                'date_field': 'date',
#                'template_name': 'expenses/expense_list.html'
#            }, name='expense_list'),
#        )
