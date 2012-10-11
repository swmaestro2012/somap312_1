from django.conf.urls import include, patterns, url

urlpatterns = patterns('accounts.views',
    #url(r'^(?P<email>\w+)/$', 'index'),
    url(r'^$', 'index'),
)
