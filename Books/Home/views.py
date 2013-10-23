# Create your views here.
# -*- coding: UTF-8 -*-
__author__ = 'varnavis'
import ConstantsDefined as Cds


def getLatesNews(**kwargs):
	from Books.Home.models import BooksNews
	from datetime import datetime

	_maxCnt = 3
	_dateExpire = datetime.today()
	if kwargs.__contains__("maxCnt"):
		_maxCnt = int(kwargs.__getitem__("maxCnt"))
	if kwargs.__contains__("dateExpire"):
		_dateExpire = datetime.strptime(kwargs.__getitem__("dateExpire"), "%Y-%m-%d %H:%M:%S.%f")

	ret = BooksNews.objects.filter(is_on=True).exclude(expire_date__lte=_dateExpire).order_by('-add_date')[:_maxCnt]

	return {"data": ret, "cnt": ret.__len__()}


def getChildsCategories(parent_cat=None):
	from Books.Home.models import BookCategories

	data = BookCategories.objects.exclude(is_on=False, is_secret=True)

	if parent_cat is not None:
		data.filter(parent=int(parent_cat)).all()
	else:
		data.filter(parent=None).all()

	return data


def getCategoriesPath(sel_cat=None):
	from Books.Home.models import BookCategories
	import collections

	item = collections.namedtuple("item", "id name")

	fname = lambda x: 'Корень' if x is None else x.title
	fid = lambda x: 0 if x is None else x.parent_id

	if sel_cat is None or sel_cat is 0:
		return []

	cur = sel_cat

	path = [item(cur, '')]

	while cur is not 0:
		dt = BookCategories.objects.get(pk=cur)
		cur = fid(dt)
		name = fname(dt)
		path.append(item(cur, name))

	path.reverse()

	return {"data": path, "cnt": path.__len__()}


def getCategoriesTree(path=None, sel=None, level=0):
	from Books.Home.models import BookCategories
	import collections

	item = collections.namedtuple("item", "id name parent level is_sel")
	f_is_sel = lambda x, y: True if x is y or y is not None else False

	if path is None or path.__len__() is 0:
		return {"data": [], "cnt": 0}

	tree = []
	cats = BookCategories.objects.filter(is_on=True, is_secret=False).order_by('parent_id').values('pk', 'parent_id', 'title', 'is_root').all()

	while level < path.cnt:
		for cat in cats:
			if path.data[level].id is 0 and cat.is_root is True:
				tree.append(item(cat.pk, cat.parent_id, cat.title, level, f_is_sel(cat.pk, sel)))
				continue
			if f_is_sel(cat.parent_id, path.data[level].id):
				tree.append(item(cat.pk, cat.parent_id, cat.title, level, f_is_sel(cat.pk, sel)))
		level += 1

	return {"data": tree, "cnt": tree.__len__()}


def load_home(request):
	from django.shortcuts import render_to_response
	from datetime import datetime

	dt_meta = Cds.get_metadata()
	path = getCategoriesPath()
	content_data = {"lNews": getLatesNews(maxCnt='5', dateExpire=datetime.now().__str__()),
					"catPath": path,
					"pageNav": getCategoriesTree(path), }

	dct = {"meta_data": dt_meta, "content_data": content_data, }
	dct = Cds.get_csrf_metadata(request, **dct)
	return render_to_response('index.html', dct)


def thanks(request):
	from django.shortcuts import render_to_response

	dt_meta = Cds.get_metadata()
	dt_meta.update(
		{"title": 'Контакты - Сообщение успешно отправлено', "keywords": 'FAQ, написать сообщение администратору.'})
	dct = {
	"meta_data": dt_meta,
	"is_contact": True,
	"title_content": 'Благодарим за обращениек нашему ресурсу FAQTHEME by IT. <br><br>Ваше сообщение успешно '
					 'отпрвлено.',
	}
	dct = Cds.get_csrf_metadata(request, **dct)
	return render_to_response('contact_thanks.html', dct)


def contact(request):
	import django
	from django.core.mail import send_mail
	from django.http import HttpResponseRedirect
	from django.shortcuts import render_to_response
	from Books.Home.forms import ContactForm

	dct = {'title_content': "Обратная связь",
		   'charset': "utf-8",
		   'robots_content': "NONE,NOARCHIVE",
		   'generator_content': "[Django] ver {0}.{1}.{2}.{4} - {3}".format(*django.VERSION),
	}
	dct = Cds.get_csrf_metadata(request, **dct)
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
			)
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm(
			initial={'subject': 'Я люблю вашу библиотеку!'}
		)
	dct.update({'form': form})
	return render_to_response('contact_form.html', dct)
