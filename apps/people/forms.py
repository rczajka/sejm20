# -*- coding: utf-8 -*-
from django import forms
from people.models import UserProfile


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label=u'Imię')
    last_name = forms.CharField(required=False, label=u'Nazwisko', help_text="Nazwisko osoby lub nazwa organizacji")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'description', 'url']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()
