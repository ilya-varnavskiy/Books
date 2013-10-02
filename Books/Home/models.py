#! -*- coding: UTF-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
import ConstantsDefined as cds


class Types(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    #parent = models.ForeignKey('self', blank=True, verbose_name="Родитель")
    title = models.CharField(max_length=255, verbose_name="Название")
    prefix = models.CharField(max_length=125, unique=True, verbose_name="Префикс поиска")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Types'
        ordering = ["publisher", "add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Типы"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"[{1}] {0}".format(self.title, self.prefix)


class Tag(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    tag_name = models.CharField(max_length=255, unique=True, verbose_name="Тэговое слово")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Tags'
        ordering = ["publisher", "add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Поисковые теги"
        verbose_name_plural = "Поисковые теги"

    def __str__(self):
        return self.tag_name

    def __unicode__(self):
        return self.tag_name


class File(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    file_name = models.CharField(max_length=255, verbose_name="Название")
    file_data = models.FileField(upload_to="file_base/%Y/%m/%d", verbose_name="Данные файла")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")
    content_type = models.ForeignKey(Types, verbose_name="Тип файла")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Files'
        ordering = ["publisher", "add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Файлы"
        verbose_name_plural = "Файлы"

    def extract_ext(self):
        ext = "{0}".format(self.content_type.prefix)
        #ext = ext.split("_").reverse()
        return ext

    def __str__(self):
        return self.file_name

    def __unicode__(self):
        return self.file_name


class Image(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    image_name = models.CharField(max_length=255, verbose_name="Название")
    img_data = models.ImageField(upload_to="image_base/%Y/%m/%d", verbose_name="Данные изображения")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")
    content_type = models.ForeignKey(Types, verbose_name="Тип изображения")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Images'
        ordering = ["publisher", "add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Изображения"
        verbose_name_plural = "Изображения"

    def extract_ext(self):
        ext = "{0}".format(self.content_type.prefix)
        #ext = ext.split("_").reverse()
        return ext

    def __str__(self):
        return self.image_name

    def __unicode__(self):
        return self.image_name


class Publishers(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    city = models.CharField(max_length=60, verbose_name="Город")
    state_province = models.CharField(max_length=30, verbose_name="Область")
    country = models.CharField(max_length=50, verbose_name="Страна")
    website = models.URLField(max_length=255, blank=True, verbose_name="Адрес Сайта")

    class Meta(object):
        def __init__(self):
            pass

        ordering = ["city", "name"]

    class Admin(object):
        def __init__(self):
            pass

    def countA(self):
        return Books.objects.filter(book_publisher=self.id).count()

    def countV(self):
        return Books.objects.filter(book_publisher=self.id, is_on=True).count()

    def __unicode__(self):
        return self.name


class Author(models.Model):
    salutation = models.CharField(max_length=10, blank=True, verbose_name="Приветсвие")
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=40, verbose_name="Фамилия")
    email = models.EmailField(max_length=125, blank=True, verbose_name="E-Mail")
    headshot = models.ImageField(upload_to="image_base/authors/%Y/%m/%d", blank=True, verbose_name="Фото")

    class Meta(object):
        def __init__(self):
            pass

        ordering = ["email"]

    class Admin(object):
        def __init__(self):
            pass

    def countA(self):
        return Books.objects.filter(book_publisher=self.id).count()

    def countV(self):
        return Books.objects.filter(book_publisher=self.id, is_on=True).count()

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s %s' % (self.salutation, self.first_name, self.last_name)
    full_name = property(_get_full_name)


class BookCategories(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    childs = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="потомки")
    title = models.CharField(max_length=255, verbose_name="Название")
    descr = models.TextField(blank=True, verbose_name="Описание")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")	#default=datetime.date.today,
    is_secret = models.BooleanField(verbose_name="Не отображать пользователям")
    is_root = models.BooleanField(blank=True, verbose_name="В корне")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Category'
        ordering = ["publisher", "add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Категории Книг"
        verbose_name_plural = "Категории Книг"

    def countA(self):
        return Books.objects.filter(parent=self.id).count()

    def countV(self):
        return Books.objects.filter(parent=self.id, is_on=True).count()

    def countVNS(self):
        return Books.objects.filter(parent=self.id, is_on=True, is_secret=False).count()

    def countS(self):
        return Books.objects.filter(parent=self.id, is_secret=True).count()

    def countSV(self):
        return Books.objects.filter(parent=self.id, is_on=True, is_secret=True).count()

    def __str__(self):
        return self.title

    def __unicode__(self):
        stat = u"root" if self.is_root else u"child"
        stat += u"-usr_hide" if self.is_secret else u""
        return u"[{1}] {0} (id:{2})".format(self.title, stat, self.id)


class Books(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    parent = models.ForeignKey(BookCategories, verbose_name="Родитель")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")
    title = models.CharField(max_length=255, verbose_name="Название")
    authors = models.ManyToManyField(Author, symmetrical=False, verbose_name="Авторы")
    book_publisher = models.ForeignKey(Publishers, verbose_name="Издатель")
    publication_date = models.DateField(verbose_name="Дата публикации книги")
    breif_descr = models.CharField(max_length=255, verbose_name="Сокращённое описание")
    descr = models.TextField(blank=True, verbose_name="Описание")
    tags = models.ManyToManyField(Tag, symmetrical=False, verbose_name="Поисковые теги")
    bk_isbn = models.CharField(max_length=25, verbose_name="ISBN код")
    bk_lang = models.CharField(max_length=60, verbose_name="Язык книги")
    bk_pages = models.PositiveIntegerField(verbose_name="Количество страниц")
    bk_format = models.CharField(max_length=120, verbose_name="Формат")
    bk_printed_ex = models.PositiveIntegerField(verbose_name="Тираж, количество экземпляров")
    bk_type = models.CharField(max_length=100, verbose_name="Переплёт")
    is_secret = models.BooleanField(verbose_name="Не отображать пользователям")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Records'
        ordering = ["publisher", "add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Записи Книг"
        verbose_name_plural = "Записи Книг"

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"[{1}] {0}".format(self.title, self.id)


class BooksImages(models.Model):
    parent = models.ForeignKey(Books, unique=True, verbose_name="Связь с записями книг")
    images = models.ManyToManyField(Image, symmetrical=False, verbose_name="Изображения")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Records_Images'
        ordering = ["parent"]
        get_latest_by = "-parent"
        verbose_name = "Изображения к записям книг"
        verbose_name_plural = "Изображения к записям книг"

    def __unicode__(self):
        return u"[{1}] Изображения к книге #{0}".format(self.parent, self.id)


class BooksFiles(models.Model):
    parent = models.ForeignKey(Books, unique=True, verbose_name="Связь с FAQ")
    files = models.ManyToManyField(File, symmetrical=False, verbose_name="Файлы")
    is_on = models.BooleanField(verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_Records_Files'
        ordering = ["parent"]
        get_latest_by = "-parent"
        verbose_name = "Файлы к записям книг"
        verbose_name_plural = "Файлы к записям книг"

    def __unicode__(self):
        return u"[{1}] Файлы к книге #{0}".format(self.parent, self.id)


class BooksNews(models.Model):
    publisher = models.ForeignKey(User, verbose_name="Создатель")
    title = models.CharField(max_length=255, verbose_name="Название")
    verb_title = models.CharField(max_length=255, blank=True, verbose_name="Code Page")
    nws_image = models.OneToOneField(Image, blank=True, verbose_name="Изображение")
    nws_file = models.OneToOneField(File, blank=True, verbose_name="Файл")
    bk_object = models.OneToOneField(Books, blank=True, verbose_name="Книга")
    add_date = models.DateField(default=datetime.date.today, verbose_name="Дата создания")
    expire_date = models.DateField(blank=True, verbose_name="Дата завершения показа")
    breif_descr = models.CharField(max_length=255, verbose_name="Сокращённое описание")
    descr = models.TextField(blank=True, verbose_name="Описание")
    tags = models.ManyToManyField(Tag, symmetrical=False, blank=True, verbose_name="Поисковые теги")
    is_on = models.BooleanField(default=True, verbose_name="Вкл.")

    class Meta(object):
        def __init__(self):
            pass

        db_table = 'BK_News'
        ordering = ["add_date"]
        get_latest_by = "-add_date"
        verbose_name = "Новости библиотеки"
        verbose_name_plural = "Новости библиотеки"

    def __init__(self, *args, **kwargs):
        super(BooksNews, self).__init__(*args, **kwargs)
        self.verb_title = cds.exclude_bad_symbols(cds.translit_srt(self.title))

    def save(self, *args, **kwargs):
        if (self.verb_title is None):
            pass
        super(BooksNews, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"[{1}] Новость #{0}".format(self.id, self.verb_title)