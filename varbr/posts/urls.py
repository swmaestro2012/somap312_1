from django.conf.urls import include, patterns, url

urlpatterns = patterns('posts.views',
    url(r'^create_book/$', 'create_book'),
    url(r'^recommend_list/$', 'recommend_list'),
)

