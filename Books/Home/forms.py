#! -*- coding: UTF-8 -*-
__author__ = 'varnavis'

from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(required=False, max_length=100)
    email = forms.EmailField(min_length=6)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message