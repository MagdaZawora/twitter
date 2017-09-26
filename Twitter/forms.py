from django import forms
from .models import Twit, Comment, Message
from django.core.validators import validate_email, URLValidator, ValidationError, EmailValidator
from django.forms import ModelForm
from django.forms import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AddTwitForm(ModelForm):

    class Meta:
        model = Twit
        exclude = ['creation_date', 'author_twit']
        labels = {'content_twit': 'Twit'}
        help_text = {'content_twit': 'Napisz twita',}


class AddCommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ['creation_date', 'author_comment', 'relating_to']
        labels = {'content_comment': 'Skomentuj'}


class LoginForm(forms.Form):

    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='hasło')



    def validate_email(email):
        db_emails = User.objects.filter(email=email)
        for db_email in db_emails:
            if db_email == email:
                raise ValidationError('%s - jest już taki użytkownik w bazie!' % email)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Wprowadź nowe hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Wprowadź ponownie hasło')



class NewMessageForm(ModelForm):

    class Meta:
        model = Message
        exclude = ['creation_date', 'is_read', 'sender', 'receiver']
        labels = {'content': 'wiadomość'}