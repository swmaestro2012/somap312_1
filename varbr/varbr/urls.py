from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'accounts.views.index'),
    url(r'^$', 'posts.views.recommend_list'),
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

if settings.DEBUG is True:
    urlpatterns += patterns('',
        url(r'^static(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),

        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
