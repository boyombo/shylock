from django.conf.urls.defaults import *

urlpatterns = patterns('sale.views',
        url(r'new/$', 'sale_new', name='sale_new'),
        url(r'complete/customer/$', 'customer_complete', name='sale_customer_complete'),
        url(r'complete/item/$', 'item_complete', name='sale_item_complete'),
        url(r'price/$', 'get_price', name='sale_get_price'),
        #url(r'getitem/$', 'get_item_detail', name='sale_get_item_detail'),
    )

urlpatterns += patterns('simplereports.views',
        url(r'list/$', 'simple_list',
            {
                'app_label': 'sale',
                'model_name': 'sale',
                'date_field': 'invoice__date',
                'template_name': 'sale/sale_list.html'
            }, name='sale_list'),
        )

urlpatterns += patterns('simplereports.views',
        url(r'customers/$', 'simple_list',
            {
                'app_label': 'sale',
                'model_name': 'customer',
                'template_name': 'sale/customer_list.html'
            }, name='sale_customer_list'),
        )