from django.conf.urls import url

from sale import views
from simplereports import views as report_views

urlpatterns = [
    url(r'new/$', views.sale_new, name='sale_new'),
    url(r'complete/customer/$', views.customer_complete,
        name='sale_customer_complete'),
    url(r'complete/item/$', views.item_complete, name='sale_item_complete'),
    url(r'price/$', views.get_price, name='sale_get_price'),
    #url(r'getitem/$', 'get_item_detail', name='sale_get_item_detail'),

    url(r'list/$', report_views.simple_list,
        {
            'app_label': 'sale',
            'model_name': 'sale',
            'date_field': 'invoice__date',
            'template_name': 'sale/sale_list.html'
        }, name='sale_list'),
    url(r'customers/$', report_views.simple_list,
        {
            'app_label': 'sale',
            'model_name': 'customer',
            'template_name': 'sale/customer_list.html'
        }, name='sale_customer_list'),
]
