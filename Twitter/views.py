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

class StartView(View):

    def get(self, request):
        # if request.user.is_authenticated:
            # user = User.objects.get(id=id)
            # return HttpResponseRedirect('/home/' + str(user.id))
        return TemplateResponse(request, 'start.html')


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = AddTwitForm()
        twits = Twit.objects.all().order_by('-creation_date')
        ctx = {'form': form, 'twits': twits}
        return TemplateResponse(request, 'home.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = AddTwitForm(request.POST)
        twits = Twit.objects.all().order_by('-creation_date')
        if form.is_valid():
            author_twit = self.request.user
            content_twit = form.cleaned_data['content_twit']
            twit = Twit(author_twit=self.request.user, content_twit=content_twit)
            twit.save()
            return HttpResponseRedirect('/home/' + str(user.id))
        else:
            ctx = {'form': form, 'twits': twits}
            return TemplateResponse(request, 'home.html', ctx)


class UserTwitsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        user = User.objects.get(id=id)
        twits = Twit.objects.filter(author_twit=user).order_by('-creation_date')
        sender = self.request.user
        receiver = user
        ctx = {'user': user, 'twits': twits, 'sender': sender, 'receiver':receiver}
        return TemplateResponse(request, 'user_twits.html', ctx)


class TwitView(LoginRequiredMixin, View):
    login_url = '/login/'

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
            author_comment = self.request.user
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
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/' + str(user.id))
            else:
                ctx = {'form': form, 'msg': 'Dane się nie zgadzają!'}
                return TemplateResponse(request, 'login.html', ctx)
        else:
            ctx = {'form': form, 'msg': 'Błąd logowania!'}
            return TemplateResponse(request, 'login.html', ctx)


class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        logout(request)
        ctx = {'msg': 'Zostałeś wylogowany'}
        return TemplateResponse(request, 'logout.html', ctx)



class RegisterView(View):

    def get(self, request):
        form = UserForm()
        ctx = {'form': form}
        return TemplateResponse(request, 'register.html', ctx)

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
            return TemplateResponse(request, 'register.html', ctx)



class ResetPasswordView(LoginRequiredMixin, View):
    login_url = '/login/'

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
                user.set_password(form.cleaned_data['password'])
                user.save()
                ctx = {'msg': 'Hasło zostało zmienione!'}
                return TemplateResponse(request, 'reset_password.html', ctx)


class NewMessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        user = User.objects.get(id=id)
        form = NewMessageForm()
        ctx = {'form': form, 'user': user}
        return TemplateResponse(request, 'new_message.html', ctx)

    def post(self, request, id):
        user = User.objects.get(id=id)
        form = NewMessageForm(request.POST)
        if form.is_valid():
            sender = self.request.user
            receiver = user
            content = form.cleaned_data['content']
            msg = Message(sender=sender, receiver=receiver, content=content)
            msg.save()
            ctx = {'msg': 'Wysłałeś wiadomość!', 'user': user}
            return TemplateResponse(request, 'new_message.html', ctx)
        else:
            ctx = {'form': form, 'user': user}
            return TemplateResponse(request, 'new_message.html', ctx)


class MessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        message = Message.objects.get(id=id)
        if message.receiver == self.request.user:
            message.is_read = True
            message.save()
        ctx = {'message': message}
        return TemplateResponse(request, 'details_message.html', ctx)



class UserMessagesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        user = User.objects.get(id=id)
        messages_sent = Message.objects.filter(sender=user).order_by('-creation_date')
        messages_received = Message.objects.filter(receiver=user).order_by('-creation_date')
        ctx = {'user': user, 'messages_sent': messages_sent, 'messages_received': messages_received}
        return TemplateResponse(request, 'user_messages.html', ctx)




