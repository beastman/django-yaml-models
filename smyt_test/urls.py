from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'smyt_test.views.home', name='home'),
    url(r'^load-model-data$', 'smyt_test.views.load_model_data', name='load_model_data'),
    url(r'^add$', 'smyt_test.views.add_record', name='add_record'),
    url(r'^edit', 'smyt_test.views.edit_record', name='edit_record'),
    # url(r'^smyt_test/', include('smyt_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}),
                            )
