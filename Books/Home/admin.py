#! -*- coding: UTF-8 -*-

__author__ = 'varnavis'
from django.contrib import admin
from Books.Home.models import *


class AuthorAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name', 'email',)
	search_fields = ('first_name', 'last_name', 'email',)
	raw_id_fields = ('publisher',)


class PublisherAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'country', 'city',)
	list_filter = ('name',)
	search_fields = ('name', 'country', 'city', 'address', 'state_province', )
	raw_id_fields = ('publisher',)


class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'bk_isbn', 'AuthorsUnicode', 'book_publisher', 'publication_date', 'getTagsUnicode',)
	list_filter = ('publication_date',)
	date_hierarchy = 'publication_date'
	ordering = ('-publication_date',)
	search_fields = ('title', 'bk_isbn')
	#fields = ('title', 'authors', 'book_publisher', 'publication_date')
	#filter_horizontal = ('authors', 'tags',)
	raw_id_fields = ('publisher', 'parent', 'tbImage', 'book_publisher',)


class BooksCategoriesAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'parent', 'add_date', 'is_root', 'is_secret', )
	list_filter = ('id',)
	ordering = ('-add_date', )
	search_fields = ('title', )
	raw_id_fields = ('publisher', 'parent')


class BooksNewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'BooksUnicode', 'breif_descr', 'add_date', 'expire_date')
	date_hierarchy = 'expire_date'
	ordering = ('expire_date', '-add_date', )
	raw_id_fields = ('nws_image', 'publisher',)


class TypesAdmin(admin.ModelAdmin):
	list_filter = ('id',)
	raw_id_fields = ('publisher',)


class TagAdmin(admin.ModelAdmin):
	list_filter = ('id',)
	raw_id_fields = ('publisher',)


class FileAdmin(admin.ModelAdmin):
	list_filter = ('id',)
	raw_id_fields = ('publisher', 'content_type',)


class ImageAdmin(admin.ModelAdmin):
	list_filter = ('id',)
	raw_id_fields = ('publisher', 'content_type',)


admin.site.register(Types, TypesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Publishers, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookCategories, BooksCategoriesAdmin)
admin.site.register(Books, BookAdmin)
admin.site.register(BooksNews, BooksNewsAdmin)
