#! -*- coding: UTF-8 -*-

__author__ = 'varnavis'
from django.contrib import admin
from Books.Home.models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'book_publisher', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    #ordering = ('-publication_date',)
    #fields = ('title', 'authors', 'book_publisher', 'publication_date')
    #filter_horizontal = ('authors',)
    #raw_id_fields = ('publisher',)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class BooksCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'add_date', 'is_root', 'is_secret')
    list_filter = ('id',)


class BooksNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'bk_object', 'breif_descr', 'add_date', 'expire_date')
    date_hierarchy = 'expire_date'


class TypesAdmin(admin.ModelAdmin):
    list_filter = ('id',)


class TagAdmin(admin.ModelAdmin):
    list_filter = ('id',)


class FileAdmin(admin.ModelAdmin):
    list_filter = ('id',)


class ImageAdmin(admin.ModelAdmin):
    list_filter = ('id',)


class BooksImagesAdmin(admin.ModelAdmin):
    list_filter = ('id',)


class BooksFilesAdmin(admin.ModelAdmin):
    list_filter = ('id',)


admin.site.register(Types, TypesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Publishers, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookCategories, BooksCategoriesAdmin)
admin.site.register(Books, BookAdmin)
admin.site.register(BooksImages, BooksImagesAdmin)
admin.site.register(BooksFiles, BooksFilesAdmin)
admin.site.register(BooksNews, BooksNewsAdmin)
