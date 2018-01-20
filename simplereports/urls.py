from django.conf.urls import url

from simplereports import views


urlpatterns = [
    url(r'(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<date_field>\w*)[/]*$',
        views.simple_list, name='simplereport_simple_list'),
]
