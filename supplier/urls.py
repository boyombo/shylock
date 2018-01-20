from django.conf.urls import url

from supplier import views

urlpatterns = [
    url(r'list/$', views.SupplierListView.as_view(), name='supplier_list'),
]
