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
    fields = ('title', 'authors', 'book_publisher', 'publication_date')
    filter_horizontal = ('authors',)
    #raw_id_fields = ('publisher',)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Publishers, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Books, BookAdmin)
