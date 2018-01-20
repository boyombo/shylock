from django.conf.urls import url

from movement import views
from simplereports import views as report_views


urlpatterns = [
    #url(r'receptions/$', 'reception_list', name='movement_reception_list'),
    url(r'receive/$', views.receive, name='movement_receive'),
    #url(r'returns/$', 'return_list', name='movement_return_list'),
    url(r'return_item/$', views.return_items, name='movement_return'),
    url(r'transfers/$', views.TransferList.as_view(),
        name='movement_transfers'),
    url(r'transfer_item/$', views.transfer_items, name='movement_transfer'),
    url(r'receptions/$', report_views.simple_list,
        {
            'app_label': 'movement',
            'model_name': 'reception',
            'template_name': 'movement/reception_list.html',
            'date_field': 'date'
        }, name='movement_reception_list'),
    url(r'returns/$', report_views.simple_list,
        {
            'app_label': 'movement',
            'model_name': 'return',
            'template_name': 'movement/return_list.html',
            'date_field': 'date'
        }, name='movement_return_list'),
]
