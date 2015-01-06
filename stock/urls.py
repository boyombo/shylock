from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'stock.views',
    url(r'list/$', 'stock_list', name='stock_list'),
    url(r'categories/$', 'stock_categories', name='stock_categories'),
    url(r'locations/$', 'stock_locations', name='stock_locations'),
    url(r'item/$', 'get_item', name='stock_get_item'),
    url(r'new/$', 'newitem', name='stock_newitem'),
    url(r'edititem/(?P<id>\d+)/$', 'newitem',
        {'next': 'stock_list'}, name='stock_edititem'),
    url(r'newcategory/$', 'newcategory', name='stock_newcategory'),
    url(r'editcategory/(?P<id>\d+)/$',
        'newcategory', name='stock_editcategory'),
    url(r'newlocation/$', 'newlocation', name='stock_newlocation'),
    url(r'editlocation/(?P<pk>\d+)/$',
        'newlocation', name='stock_editlocation'),
    url(r'row/$', 'get_row', name='stock_get_row'),
)
