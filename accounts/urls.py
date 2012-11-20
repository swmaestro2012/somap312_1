from django.conf.urls import include, patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('accounts.views',
    #url(r'^(?P<email>\w+)/$', 'index'),
    url(r'^userinfo/(?P<author_id>\w+)/$', 'get_userinfo'),
    url(r'^profile/$', 'redirect_to_login'),
    url(r'^signup/$', 'signup_page'),
    url(r'^signup_confirmed/$', 'signup_confirmed'),
    url(r'^add_favauthor/(?P<favauthor>\d+)/(?P<addornot>\d+)/$', 'add_favauthor'),
    url(r'^show_favauthor/$', 'show_favauthor'),
    url(r'^update_usermessage/$', 'update_usermessage'),
    url(r'^update_userprofileimg/$', 'update_userprofileimg'),
    url(r'^show_usercomment/(?P<user_id>\w+)/$', 'show_usercomment'),
    url(r'^set_password/$', 'set_password'),
    url(r'^authenticate_user/$', 'authenticate_user'),
    url(r'^dropout/$', 'dropout'),
    url(r'^settings/$', 'settings'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
