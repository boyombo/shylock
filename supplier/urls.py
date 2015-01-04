from django.conf.urls.defaults import *

urlpatterns = patterns('simplereports.views',
        url(r'list/$', 'simple_list',
            {
                'app_label': 'supplier',
                'model_name': 'supplier',
                'template_name': 'supplier/supplier_list.html'
            }, name='supplier_list'),
        )