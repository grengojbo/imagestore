# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import imagestore.utils
import django.db.models.deletion
from django.conf import settings
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('is_public', models.BooleanField(default=True, verbose_name='Is public')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
            ],
            options={
                'ordering': ('order', 'created', 'name'),
                'abstract': False,
                'verbose_name_plural': 'Albums',
                'verbose_name': 'Album',
                'swappable': 'IMAGESTORE_ALBUM_MODEL',
                'permissions': (('moderate_albums', 'View, update and delete any album'),),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('tags', tagging.fields.TagField(max_length=255, verbose_name='Tags', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=imagestore.utils.FilePathGenerator(to='imagestore/'), max_length=255, verbose_name='File')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created', null=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated', null=True)),
                ('links', models.CharField(max_length=80, null=True, verbose_name='link name', blank=True)),
                ('views', models.IntegerField(default=0, null=True, verbose_name='views', blank=True)),
                ('album', models.ForeignKey(related_name='images', verbose_name='Album', blank=True, to=settings.IMAGESTORE_ALBUM_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='images', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('order', 'id'),
                'abstract': False,
                'verbose_name_plural': 'Images',
                'verbose_name': 'Image',
                'swappable': 'IMAGESTORE_IMAGE_MODEL',
                'permissions': (('moderate_images', 'View, update and delete any image'),),
            },
        ),
        migrations.CreateModel(
            name='AlbumUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zip_file', models.FileField(help_text='Select a .zip file of images to upload into a new Gallery.', upload_to='temp/', verbose_name='images file (.zip)')),
                ('new_album_name', models.CharField(help_text='If not empty new album with this name will be created and images will be upload to this album', max_length=255, verbose_name='New album name', blank=True)),
                ('tags', models.CharField(max_length=255, verbose_name='tags', blank=True)),
                ('album', models.ForeignKey(blank=True, to=settings.IMAGESTORE_ALBUM_MODEL, help_text='Select an album to add these images to. leave this empty to create a new album from the supplied title.', null=True)),
            ],
            options={
                'verbose_name': 'Album upload',
                'verbose_name_plural': 'Album uploads',
            },
        ),
        migrations.AddField(
            model_name='album',
            name='head',
            field=models.ForeignKey(related_name='head_of', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Head', blank=True, to=settings.IMAGESTORE_IMAGE_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(related_name='albums', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
