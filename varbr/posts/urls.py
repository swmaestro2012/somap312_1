from django.conf.urls import include, patterns, url

urlpatterns = patterns('posts.views',
    url(r'^create_book/$', 'create_book'),
    
    url(r'^recommend_list/$', 'recommend_list'),
    url(r'^show_newlist/$', 'show_newlist'),


    url(r'^get_bookinfo/(?P<book_id>\d+)/$', 'get_bookinfo'),
    url(r'^show_mywork/$', 'show_mywork'),
    
    url(r'^write_branch/(?P<book_info>\d+)/(?P<parent_branch>\d+)/$', 'write_branch'),
    url(r'^read_branch/(?P<branch_id>\d+)/', 'read_branch'),
)