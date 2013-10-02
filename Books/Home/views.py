# Create your views here.
# -*- coding: UTF-8 -*-
__author__ = 'varnavis'
from django.http import HttpResponse
import ConstantsDefined as Cds


def load_home(request):
    """

    :param request:
    :return:
    """
    return HttpResponse("Домашняя страница Books \r\n %s" % str(request))


def thanks(request):
    from django.shortcuts import render_to_response
    dt_meta = Cds.get_metadata()
    dt_meta.update({"title":'Контакты - Сообщение успешно отправлено', "keywords": 'FAQ, написать сообщение администратору.'})
    dct = {
            "meta_data": dt_meta,
            "is_contact" : True,
            "title_content": 'Благодарим за обращениек нашему ресурсу FAQTHEME by IT. <br><br>Ваше сообщение успешно отпрвлено.',
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
           'charset' : "utf-8",
           'robots_content' : "NONE,NOARCHIVE",
           'generator_content' : "[Django] ver {0}.{1}.{2}.{4} - {3}".format(*django.VERSION) ,
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
