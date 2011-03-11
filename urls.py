from django.conf.urls.defaults import *
from django.contrib import admin
import settings
import os

admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^accounts/login/$', 'login', name='site_login'),
    url(r'^accounts/logout/$', 'logout', {'next_page': '/'}, name='site_logout'),
    (r'^accounts/password-reset/$', 'password_reset'),
    (r'^accounts/password-reset/done/$', 'password_reset_done'),
    (r'^accounts/password-change/$', 'password_change'),
    (r'^accounts/password-change/done/$', 'password_change_done'),
)

urlpatterns += patterns('',
    # Example:
    # (r'^payroll/', include('payroll.foo.urls')),

	#Uncomment this for admin:
	(r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
	(r'^suppliers/', include('supplier.urls')),
	(r'^stock/', include('stock.urls')),
	(r'^movement/', include('movement.urls')),
	(r'^sale/', include('sale.urls')),
	(r'^expenses/', include('expenses.urls')),
	(r'^simplereports/', include('simplereports.urls')),
	(r'^accounting/', include('accounting.urls')),
	(r'^$', 'django.views.generic.simple.direct_to_template',{'template':'default.html'}),
)

# Static content serving, for development only!
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__),'site_media')}),
	)
