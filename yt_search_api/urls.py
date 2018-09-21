from django.conf.urls import url

from yt_search_api import views

urlpatterns = [
    url(r'^words/$', views.SearchKeywordList.as_view()),
    url(r'^words/(?P<pk>[0-9]+)/$', views.SearchKeywordDetail.as_view()),
    url(r'^words/(?P<key_word__pk>[0-9]+)/video/$', views.YTVideoList.as_view()),
]
