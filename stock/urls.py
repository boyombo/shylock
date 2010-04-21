from django.conf.urls.defaults import *
from stock.models import Item
from django.conf import settings

info_dict = {
    'queryset': Item.objects.all(),
    'paginate_by': settings.ITEMS_PER_PAGE,
    'template_name': 'stock/stock_list.html',
    'template_object_name': 'stock',
}

urlpatterns = patterns('',
        url(r'list/$', 'django.views.generic.list_detail.object_list', info_dict, name='stock_list'),
        url(r'item/$', 'stock.views.get_item', name='stock_get_item'),
        url(r'row/$', 'stock.views.get_row', name='stock_get_row'),
        #url(r'locationstock/(?P<loc_id>\d+)/$', 'location_stock_list', name='location_stock_list'),
        #url(r'locations/$', 'locations', name='location_list'),
    )
