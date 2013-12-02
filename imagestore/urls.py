# -*- mode: python; coding: utf-8; -*-
from django.conf.urls import patterns, url, include
from tagging.models import Tag
from .views import AlbumListView, ImageListView, UpdateImage, UpdateAlbum, CreateImage, CreateAlbum, DeleteImage
from .views import ImageView, AlbumList, DeleteAlbum, ImageList

#from fancy_autocomplete.views import AutocompleteSite
#autocomletes = AutocompleteSite()

#autocomletes.register(
#    'tag',
#    queryset=Tag.objects.all(),
#    search_fields=('name',),
#    limit=10,
#    lookup='istartswith',
#)

album_urls = patterns('',
                      #url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(), name='photo-detail'),
                      url(r'^(?P<pk>\d+)/size/(?P<size>\d+)/$', ImageList.as_view(), name='api-album-images'),
                      url(r'^$', AlbumList.as_view(), name='api-album-list')
                      )

#image_urls = patterns('',
#                      #url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(), name='photo-detail'),
#                      url(r'^(?P<pk>\d+)/$', ImageList.as_view(), name='api-image-list')
#)

urlpatterns = patterns('imagestore.views',
                       url(r'^$', AlbumListView.as_view(), name='index'),
                       url(r'^api/album/', include(album_urls)),
                       #url(r'^api/image/', include(image_urls)),

                       url(r'^album/add/$', CreateAlbum.as_view(), name='create-album'),
                       url(r'^album/(?P<album_id>\d+)/$', ImageListView.as_view(), name='album'),
                       url(r'^album/(?P<pk>\d+)/edit/$', UpdateAlbum.as_view(), name='update-album'),
                       url(r'^album/(?P<pk>\d+)/delete/$', DeleteAlbum.as_view(), name='delete-album'),

                       url(r'^tag/(?P<tag>[^/]+)/$', ImageListView.as_view(), name='tag'),

                       url(r'^user/(?P<username>\w+)/albums/', AlbumListView.as_view(), name='user'),
                       url(r'^user/(?P<username>\w+)/$', ImageListView.as_view(), name='user-images'),

                       url(r'^upload/$', CreateImage.as_view(), name='upload'),

                       url(r'^image/(?P<pk>\d+)/$', ImageView.as_view(), name='image'),
                       url(r'^album/(?P<album_id>\d+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-album'),
                       url(r'^tag/(?P<tag>[^/]+)/image/(?P<pk>\d+)/$', ImageView.as_view(), name='image-tag'),
                       url(r'^image/(?P<pk>\d+)/delete/$', DeleteImage.as_view(), name='delete-image'),
                       url(r'^image/(?P<pk>\d+)/update/$', UpdateImage.as_view(), name='update-image'),

                       #url(r'^autocomplete/(.*)/$', autocomletes, name='autocomplete')
                       )



