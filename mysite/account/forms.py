from django import forms
from django.contrib.auth.forms import (UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.forms import UsernameField
from . import models
from django.core.mail import send_mail


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ('email','first_name','last_name')
        fields_classes = {'email':UsernameField}

    def send_mail(self):
        message = "welcome{}".format(self.cleaned_data['email'])
        send_mail('welcome to booktime', message, "site@booktime.domain",[self.cleaned_data['email']], fail_silently=True)
