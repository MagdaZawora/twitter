from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Twit, Comment, Message
from django.template.response import TemplateResponse
from .forms import AddTwitForm, AddCommentForm, LoginForm, ResetPasswordForm, NewMessageForm, UserForm
from django .http import HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, FormView
from django.core.validators import EmailValidator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse

# Create your views here.

class HomeView(View):
    # login_url = '/login/'

    def get(self, request, id):
        twits = Twit.objects.all().order_by('-creation_date')
        user = User.objects.get(id=id)
        form = AddTwitForm()
        ctx = {'twits': twits, 'form': form}
        return TemplateResponse(request, 'home.html', ctx)

    def post(self, request, id):
        twits = Twit.objects.all().order_by('-creation_date')
        user = User.objects.get(id=id)
        form = AddTwitForm(request.POST)
        if form.is_valid():
            author_twit = user
            content_twit = form.cleaned_data['content_twit']
            twit = Twit(author_twit=user, content_twit=content_twit)
            twit.save()
            return HttpResponseRedirect('/home/' + str(user.id))
        else:
            ctx = {'form': form}
            return TemplateResponse(request, 'home.html', ctx)



"""
class AddTwitView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)

        ctx = {'form': form}
        return TemplateResponse(request, 'add_twit.html', ctx)

"""


class UserTwitsView(View):

    def get(self, request, id):
        user = User.objects.get(id=int(id))
        twits = Twit.objects.filter(author_twit=user).order_by('-creation_date')
        ctx = {'user': user, 'twits': twits}
        return TemplateResponse(request, 'user_twits.html', ctx)


class TwitView(View):

    def get(self, request, id):
        twit = Twit.objects.get(id=id)
        comments = Comment.objects.filter(relating_to=twit).order_by('-creation_date')
        form = AddCommentForm()
        ctx = {'twit': twit, 'form': form, 'comments': comments}
        return TemplateResponse(request, 'details_twit.html', ctx)

    def post(self, request, id):
        form = AddCommentForm(request.POST)
        twit = Twit.objects.get(id=id)
        comments = Comment.objects.filter(relating_to=twit).order_by('-creation_date')
        if form.is_valid():
            author_comment = request.user
            content_comment = form.cleaned_data['content_comment']
            relating_to = twit
            comment = Comment(author_comment=author_comment, content_comment=content_comment, relating_to = relating_to)
            comment.save()
            ctx = {'form': form, 'twit': twit, 'comments': comments}
            return HttpResponseRedirect('/details_twit/' + str(twit.id), ctx)
        else:
            ctx = {'form': form}
            return TemplateResponse(request, 'details_twit.html', ctx)


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return TemplateResponse(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home/' + str(user.id))
        else:
            ctx = {'msg': 'Dane się nie zgadazają!'}
            return TemplateResponse(request, 'login.html', ctx)



class LogoutView(View):

    def get(self, request, id):
        logout(request)
        ctx = {'msg': 'Zostałeś wylogowany'}
        return TemplateResponse(request, 'logout.html', ctx)

"""
class AddUserCreate(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'user_form.html'
    success_url = '/all_twits/' + str(user.id))
"""

class AddUserView(View):

    def get(self, request):
        form = UserForm()
        ctx = {'form': form}
        return TemplateResponse(request, 'user_form.html', ctx)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/' + str(user.id))
        else:
            ctx = {"form": form, 'msg': 'Dane się nie zgadazają!'}
            return TemplateResponse(request, 'user_form.html', ctx)

class ResetPasswordView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = ResetPasswordForm()
        ctx = {'form': form}
        return TemplateResponse(request, 'reset_password.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password != password2:
                ctx={'msg': 'Hasła są różne!'}
                return TemplateResponse(request, 'reset_password.html', ctx)
            else:
                user.save()
                ctx = {'msg': 'Hasło zmienione poprawnie!'}
                return TemplateResponse(request, 'reset_password.html', ctx)


class NewMessageView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = NewMessageForm()
        ctx = {'form': form, 'user': user}
        return TemplateResponse(request, 'new_message.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = NewMessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            receiver = user
            content = form.cleaned_data['content']
            msg = Message(sender=sender, receiver=receiver, content=content)
            msg.save()
            ctx = {'msg': 'Wysłałeś wiadomość!', 'user': user}
            return TemplateResponse(request, 'new_message.html', ctx)
        else:
            ctx = {'form': form, 'user': user}
            return TemplateResponse(request, 'new_message.html', ctx)



class MessageView(View):

    def get(self, request, id):
        message = Message.objects.get(id=id)
        if message.receiver == self.request.user:
            message.is_read = True
            message.save()
        ctx = {'message': message}
        return TemplateResponse(request, 'details_message.html', ctx)



class UserMessagesView(View):

    def get(self, request, id):
        user = User.objects.get(id=id)
        messages_sent = Message.objects.filter(sender=user).order_by('-creation_date')
        messages_received = Message.objects.filter(receiver=user).order_by('-creation_date')
        ctx = {'user': user, 'messages_sent': messages_sent, 'messages_received': messages_received}
        return TemplateResponse(request, 'user_messages.html', ctx)




