from django.conf.urls import include, patterns, url

urlpatterns = patterns('accounts.views',
    #url(r'^(?P<email>\w+)/$', 'index'),

    url(r'^profile/$', 'redirect_to_login'),
    url(r'^signup/$', 'signup_page'),
    url(r'^signup_confirmed/$', 'signup_confirmed'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
