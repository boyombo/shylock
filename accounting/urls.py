from django.conf.urls import url

from accounting import views

urlpatterns = [
    url(r'pandl/$', views.pandl, name='accounting_pandl'),
    url(r'graph/$', views.graph, name='accounting_graph'),
]
