from django.urls import path

from services.views import (
    share,TagListView, 
    SearchBundleListView,AutoSuggestions,
    ReadingsListView,ReadingsDetailView,
    ReadingsCreateView,ReadingsUpdateView,
    ReadingsDeleteView, download_bundle
)

#rss feed generator
from .feeds import PublishedBundleFeed

urlpatterns=[

    # shareform
    path('share/<slug:slug>/',share,name='share_by_email'),

    #rss url
    path('bundle/published/all/feed.xml', PublishedBundleFeed(), name='bundle_feed'),

    #public topics by tag
    path('bundle/topics/<slug:tag_slug>/',TagListView.as_view(), name='list_tag'),

    #search public bundles
    path('bundle/public/search/',SearchBundleListView.as_view(), name='search_bundle_results'),

    #ajax autosuggestions
    path('bundle/search/auto/',AutoSuggestions.as_view(),name='auto_suggestions'),

    #readinglist urls
    path('readinglists/list/',ReadingsListView.as_view(), name='readinglists_list'),
    path('readinglists/<pk>/<uuid>/detail/',ReadingsDetailView.as_view(), name='readinglists_detail'),
    path('readinglists/create/',ReadingsCreateView.as_view(), name='readinglists_create'),
    path('readinglists/<pk>/<uuid>/update/',ReadingsUpdateView.as_view(), name='readinglists_update'),
    path('readinglists/<pk>/<uuid>/delete/',ReadingsDeleteView.as_view(), name='readinglists_delete'),

    #download bundle
    path('download/<id>',download_bundle, name='download_bundle'),



]