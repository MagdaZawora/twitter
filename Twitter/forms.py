from django import forms
from .models import Twit, Comment, Message
from django.core.validators import validate_email, URLValidator, ValidationError, EmailValidator
from django.forms import ModelForm
from django.forms import widgets
from django.contrib.auth.models import User


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

    email = forms.EmailField(label='e-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='password')


    def validate_email(email):
        db_emails = User.objects.filter(email=email)
        for db_email in db_emails:
            if db_email == email:
                raise ValidationError('%s Jest już taki użytkownik w bazie!' % email)

"""
class AddUserForm(forms.Form):

    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.CharField(label='e-mail', validators=[EmailValidator, validate_email])
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Potwierdź hasło')

"""

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Wprowadź nowe hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Wprowadź ponownie hasło')



class NewMessageForm(ModelForm):

    class Meta:
        model = Message
        exclude = ['creation_date', 'is_read', 'sender', 'receiver']
        labels = {'content': 'wiadomość'}