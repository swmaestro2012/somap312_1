from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'accounts.views.index'),
    url(r'^$', 'main.views.main_page'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^posts/', include('posts.urls')),
    url(r'^main/', include('main.urls')),
    # Examples:
    # url(r'^$', 'varbr.views.home', name='home'),
    # url(r'^varbr/', include('varbr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
