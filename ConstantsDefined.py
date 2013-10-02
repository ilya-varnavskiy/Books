# -*- coding: UTF-8 -*-
__author__ = 'varnavis'
import os

BASE_ROOT = os.path.dirname(__file__)
BASE_PREF = "/"  #"http://{0}/".format(Req.get_host())

MEDIA_DIR_ROOT = os.path.join(BASE_ROOT, 'media/').replace('\\','/')


def get_csrf_metadata(request, **kwds):
    from django.core.context_processors import csrf
    kwds.update(csrf(request))
    return kwds


def get_metadata():
    import django
    return dict({
                    "title": 'BOOKS | Маленькая библиотека',
                    "distribution": 'GLOBAL',
                    "resource_type": 'DOCUMENT',
                    "document_state": 'DYNAMIC',
                    "url": 'ABSOLUTE_URL',
                    "robots" : 'NONE,NOARCHIVE',
                    "revisit_after": 'NEVER',
                    "rating": 'GENERAL',
                    "generator" : 'MARSEL CMS on [Django] ver {0}.{1}.{2}.{4} - {3}'.format(*django.VERSION),
                    "author": 'MIRZAKULOV M.B.',
                    "meta_title": 'Books library',
                    "copyright": 'Copyright by Marsel',
                    "description": 'Сайт библиотеки книг',
                    "keywords": 'Books, library',
                })


def gen_head_tags(title = "Unknown page", charset = "utf-8"):
    tag = "<head><meta charset=\"{0}\">".format(charset)
    tag += "<title>{0}</title>".format(title)
    tag += "<meta name=\"{0}\" content=\"{1}\"></head>".format("robots","NONE,NOARCHIVE")
    return tag


def gen_head_tpl(title = "Unknown page"):
    from django.template.loader import get_template
    from django.template import Context
    t = get_template('_tpl_head.html')
    html = t.render(Context({'title': title}))
    return html


def gen_style_tpl():
    from django.template.loader import get_template
    from django.template import Context
    t = get_template('_tpl_style.html')
    html = t.render(Context())
    return html


def current_datetime(request):
    import datetime
    from django.http import HttpResponse
    now = datetime.datetime.now()
    html = "<html>"
    html += gen_head_tags("Page current datetime")
    html += "<body>It is now {0}.</body>".format(now)
    html += "</html>"
    return HttpResponse(html)


def current_datetime2(request):
    import django
    from django.http import HttpResponse
    from django.template.loader import get_template
    from django.template import Context
    #from django.shortcuts import render_to_response
    import datetime
    now = datetime.datetime.now()
    title = BASE_ROOT #"Page current datetime ver 2"
    #head_meta = gen_head_tags(title)
    #head_style = gen_style_tpl()
    dct = {'title_content': title,
           'http_equiv': "content-type",
           'content_type' : "text/html",
           'charset' : "utf-8",
           'robots_content' : "NONE,NOARCHIVE",
           'generator_content' : "[Django] ver {0}.{1}.{2}.{4} - {3}".format(*django.VERSION) ,
           #'head_meta': str(head_meta),
           #'head_style': str(head_style),
           'out_date_string': now}
    #return render_to_response('_tpl_current_date.html', dct)
    t = get_template('_tpl_current_date2.html') #'_tpl_current_date.html'
    html = t.render(Context(dct))
    #html += str(request)
    return HttpResponse(html)


def display_meta(request):
    from django.http import HttpResponse
    values = request.META.items()
    values += request.COOKIES.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def translit_srt(str_r):
    symbols = ( u"абвгдеёзийклмнопрстуфхъыьэАБВГДЕЁЗИЙКЛМНОПРСТУФХЪЫЬЭ",
                u"abvgdeezijklmnoprstufh-y_eABVGDEEZIJKLMNOPRSTUFH-Y_E")

    tr = {ord(a):ord(b) for a, b in zip(*symbols)}

    return str_r.translate(tr)


def exclude_bad_symbols(str_r):
    import re

    chars = [',', '!', '\"', ';', '?', '$', '@', '%', '#', '&', '+', '\\', '/', '*']

    return re.sub('[%s]' % ''.join(chars), '', str_r)