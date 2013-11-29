# -*- mode: python; coding: utf-8; -*-
__author__ = 'jbo'

from rest_framework import serializers
from .models.album import Album
from .models.image import Image
from profiles.serializers import UserSerializer
from sorl.thumbnail import get_thumbnail
#from django.contrib.auth.models import User


class AlbumSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    head = serializers.HyperlinkedIdentityField('images', view_name='api-image-list', lookup_field='album')
    #posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
    #gender = serializers.Field('profile.gender')

    class Meta:
        model = Album
        #fields = ('id', 'username', 'first_name', 'last_name', 'posts', )
        fields = ('id', 'name', 'created', 'updated', 'is_public', 'user', 'head')


class ImageSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    image_small = serializers.Field(source='image_small')
    #posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
    #gender = serializers.Field('profile.gender')

    class Meta:
        model = Image
        #fields = ('id', 'username', 'first_name', 'last_name', 'posts', )
        fields = ('id', 'title', 'image', 'image_small', 'created', 'updated', 'album', 'views', 'description', 'user')