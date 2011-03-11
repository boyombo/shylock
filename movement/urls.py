from django.conf.urls.defaults import *
from movement.models import Reception, Return
from django.conf import settings

urlpatterns = patterns('movement.views',
        #url(r'receptions/$', 'reception_list', name='movement_reception_list'),
        url(r'receive/$', 'receive', name='movement_receive'),
        #url(r'returns/$', 'return_list', name='movement_return_list'),
        url(r'return_item/$', 'return_items', name='movement_return'),
        )

urlpatterns += patterns('simplereports.views',
        url(r'receptions/$', 'simple_list',
            {
                'app_label': 'movement',
                'model_name': 'reception',
                'template_name': 'movement/reception_list.html',
                'date_field': 'date'
            }, name='movement_reception_list'),
        url(r'returns/$', 'simple_list',
            {
                'app_label': 'movement',
                'model_name': 'return',
                'template_name': 'movement/return_list.html',
                'date_field': 'date'
            }, name='movement_return_list'),
        )

