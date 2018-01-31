from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.views import login, logout_then_login
import os

#admin.autodiscover()

#urlpatterns = patterns('django.contrib.auth.views',
#    url(r'^accounts/login/$', 'login', name='site_login'),
#    url(r'^accounts/logout/$', 'logout', {'next_page': '/'}, name='site_logout'),
#    (r'^accounts/password-reset/$', 'password_reset'),
#    (r'^accounts/password-reset/done/$', 'password_reset_done'),
#    (r'^accounts/password-change/$', 'password_change'),
#    (r'^accounts/password-change/done/$', 'password_change_done'),
#)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^suppliers/', include('supplier.urls')),
    #(r'^api/$', 'sale.views.json_api'),
    url(r'^stock/', include('stock.urls')),
    url(r'^movement/', include('movement.urls')),
    url(r'^sale/', include('sale.urls')),
    url(r'^expenses/', include('expenses.urls')),
    url(r'^simplereports/', include('simplereports.urls')),
    url(r'^accounting/', include('accounting.urls')),
    url(r'^$', TemplateView.as_view(template_name='default.html'), name='home'),
    url(r'^accounts/login/$', login, name='site_login'),
    url(r'^accounts/logout/$', logout_then_login, name='site_logout'),
]

# Static content serving, for development only!
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
