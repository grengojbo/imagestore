# -*- mode: python; coding: utf-8; -*-
from django.contrib import admin
from imagestore.models import Image, Album, AlbumUpload
from sorl.thumbnail.admin import AdminImageMixin, AdminInlineImageMixin
from django.conf import settings

class InlineImageAdmin(AdminInlineImageMixin, admin.TabularInline):
    model = Image
    fieldsets = ((None, {'fields': ['image', 'user', 'title', 'order', 'tags', 'album']}),)
    raw_id_fields = ('user', )
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    # TODO: добавить действие публиковать, отменить публикацию
    fieldsets = ((None, {'fields': ['name', 'user', 'is_public', 'order']}),)
    list_display = ('name', 'admin_thumbnail', 'user', 'created', 'updated', 'is_public', 'order')
    list_editable = ('order', )
    list_filter = ('is_public', )
    inlines = [InlineImageAdmin]

admin.site.register(Album, AlbumAdmin)


class ImageAdmin(admin.ModelAdmin):
    search_fields = ('title', 'album',)
    fieldsets = ((None,
                  {'fields': ['user', 'title', 'image', 'description', 'order', 'tags', 'album', 'views', 'links']}),)
    list_display = ('admin_thumbnail', 'user', 'order', 'album', 'title')
    raw_id_fields = ('user', )
    list_filter = ('album', )


class AlbumUploadAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


IMAGE_MODEL = getattr(settings, 'IMAGESTORE_IMAGE_MODEL', None)
if not IMAGE_MODEL:
    admin.site.register(Image, ImageAdmin)

ALBUM_MODEL = getattr(settings, 'IMAGESTORE_ALBUM_MODEL', None)
if not ALBUM_MODEL:
    admin.site.register(AlbumUpload, AlbumUploadAdmin)
