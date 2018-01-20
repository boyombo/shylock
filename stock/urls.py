from django.conf.urls import url

from stock import views

urlpatterns = [
    url(r'list/$', views.stock_list, name='stock_list'),
    url(r'new/$', views.newitem, name='stock_newitem'),
    url(r'edititem/(?P<id>\d+)/$', views.newitem,
        {'next': 'stock_list'}, name='stock_edititem'),

    url(r'serials/$', views.serial_list, name='serial_list'),
    url(r'newserial/$', views.newserial, name='serial_newitem'),
    url(r'serial_cat/$', views.SerialCategoriesList.as_view(),
        name='serial_categories'),
    url(r'new_serial_category/$', views.newcategory,
        {
            'next': 'serial_categories',
            'template_name': 'stock/new_serial_category.html'
        },
        name='serial_newcategory'),

    url(r'suppliers/$', views.StockSupplierList.as_view(),
        name='stock_suppliers'),
    url(r'newsupplier/$', views.newsupplier, name='stock_newsupplier'),
    url(r'editsupplier/(?P<id>\d+)/$',
        views.newsupplier, name='stock_editsupplier'),

    url(r'users/$', views.StockUsersList.as_view(), name='user_list'),
    url(r'newuser/$', views.newuser, name='stock_newuser'),
    url(r'edituser/(?P<pk>\d+)/$', views.edituser, name='stock_edituser'),

    url(r'categories/$', views.StockCategoriesList.as_view(),
        name='stock_categories'),
    url(r'locations/$', views.StockLocView.as_view(), name='stock_locations'),
    url(r'item/$', views.get_item, name='stock_get_item'),
    url(r'newcategory/$', views.newcategory, name='stock_newcategory'),
    url(r'editcategory/(?P<id>\d+)/$',
        views.newcategory, name='stock_editcategory'),
    url(r'newlocation/$', views.newlocation, name='stock_newlocation'),
    url(r'editlocation/(?P<pk>\d+)/$',
        views.newlocation, name='stock_editlocation'),
    url(r'row/$', views.get_row, name='stock_get_row'),
]
